"""共享模型 (_shared) 单元测试 —— 判别联合解析与往返序列化"""

import json
import pytest
from pydantic	import ValidationError

from pydantic	import TypeAdapter

from pi_bridge.models._shared	import (
	Usage,
	Cost,
	Model,
	ModelCost,
	TextContent,
	ImageContent,
	ThinkingContent,
	ToolCall,
	ContentBlock,
	TextStartEvent,
	TextDeltaEvent,
	TextEndEvent,
	ThinkingStartEvent,
	ThinkingDeltaEvent,
	ThinkingEndEvent,
	ToolcallStartEvent,
	ToolcallDeltaEvent,
	ToolcallEndEvent,
	AssistantMessageEvent,
	ToolExecutionResult,
	CompactionResult,
	UserMessage,
	AssistantMessage,
	ToolResultMessage,
	BashExecutionMessage,
	CustomMessage,
	BranchSummaryMessage,
	CompactionSummaryMessage,
	AgentMessage,
	SessionStatsTokens,
	SessionStatsContextUsage,
	SessionStatsData,
	SessionEntry,
	TreeEntry,
	StateData,
	BashData,
	ModelsData,
	LevelsData,
	ForkMessage,
	ForkMessagesData,
	EntriesData,
	TreeData,
	LastAssistantTextData,
	ExportHtmlData,
	CancelledData,
	ForkData,
	CommandInfo,
	CommandsData,
	MessagesData,
	CycleModelData,
)


# 判别联合类型别名只能用 TypeAdapter 解析,不能直接 .model_validate()
_content_block_adapter = TypeAdapter(ContentBlock)
_assistant_message_event_adapter = TypeAdapter(AssistantMessageEvent)
_agent_message_adapter = TypeAdapter(AgentMessage)


class TestUsage:
	
	def test_usage_defaults(self):
		u = Usage()
		assert u.input == 0
		assert u.output == 0
		assert u.totalTokens == 0
		assert u.cost is None
	
	def test_usage_with_cost(self):
		u = Usage(input=10, output=20, totalTokens=30, cost={"input": 1.0, "output": 2.0, "total": 3.0})
		assert u.cost is not None
		assert u.cost.total == 3.0
	
	def test_usage_roundtrip(self):
		u = Usage(input=10, output=20, cacheRead=5, cacheWrite=3, totalTokens=38)
		u2 = Usage.model_validate_json(u.model_dump_json())
		assert u2 == u


class TestModel:
	
	def test_model_defaults(self):
		m = Model()
		assert m.id == ""
		assert m.input == []
		assert m.cost is None
	
	def test_model_roundtrip(self):
		m = Model(id="test-model", name="Test Model", provider="test", cost={"input": 0.1, "output": 0.2})
		m2 = Model.model_validate_json(m.model_dump_json())
		assert m2 == m


class TestContentBlock:
	
	def test_text_content(self):
		cb = _content_block_adapter.validate_python({"type": "text", "text": "hello"})
		assert isinstance(cb, TextContent)
		assert cb.text == "hello"
	
	def test_image_content(self):
		cb = _content_block_adapter.validate_python({"type": "image", "data": "base64...", "mimeType": "image/png"})
		assert isinstance(cb, ImageContent)
		assert cb.mimeType == "image/png"
	
	def test_thinking_content(self):
		cb = _content_block_adapter.validate_python({"type": "thinking", "thinking": "hmm"})
		assert isinstance(cb, ThinkingContent)
		assert cb.thinking == "hmm"
	
	def test_tool_call(self):
		cb = _content_block_adapter.validate_python({"type": "toolCall", "id": "t1", "name": "bash", "arguments": {"cmd": "ls"}})
		assert isinstance(cb, ToolCall)
		assert cb.arguments == {"cmd": "ls"}
	
	def test_roundtrip(self):
		for raw in [
			{"type": "text", "text": "hi"},
			{"type": "image", "data": "abc", "mimeType": "image/jpeg"},
			{"type": "thinking", "thinking": "..."},
			{"type": "toolCall", "id": "t1", "name": "x", "arguments": {}},
		]:
			cb = _content_block_adapter.validate_python(raw)
			js = _content_block_adapter.dump_json(cb)
			cb2 = _content_block_adapter.validate_json(js)
			assert cb2 == cb


class TestAssistantMessageEvent:
	
	def test_text_delta(self):
		ev = _assistant_message_event_adapter.validate_python({"type": "text_delta", "contentIndex": 1, "delta": "hello"})
		assert isinstance(ev, TextDeltaEvent)
		assert ev.delta == "hello"
		assert ev.contentIndex == 1
	
	def test_toolcall_end(self):
		ev = _assistant_message_event_adapter.validate_python({
			"type": "toolcall_end", "contentIndex": 0,
			"toolCall": {"type": "toolCall", "id": "t1", "name": "bash", "arguments": {"cmd": "ls"}}
		})
		assert isinstance(ev, ToolcallEndEvent)
		assert ev.toolCall.name == "bash"
	
	def test_roundtrip(self):
		raw = {"type": "thinking_delta", "contentIndex": 0, "delta": "thinking..."}
		ev = _assistant_message_event_adapter.validate_python(raw)
		js = _assistant_message_event_adapter.dump_json(ev)
		ev2 = _assistant_message_event_adapter.validate_json(js)
		assert ev2 == ev


class TestAgentMessage:
	
	def test_user_message(self):
		m = _agent_message_adapter.validate_python({"role": "user", "content": "hello"})
		assert isinstance(m, UserMessage)
		assert m.content == "hello"
	
	def test_assistant_message(self):
		m = _agent_message_adapter.validate_python({
			"role": "assistant", "content": [{"type": "text", "text": "hi"}],
			"model": "claude", "usage": {"input": 10, "output": 20, "totalTokens": 30}
		})
		assert isinstance(m, AssistantMessage)
		assert len(m.content) == 1
		assert isinstance(m.content[0], TextContent)
		assert m.usage is not None and m.usage.totalTokens == 30
	
	def test_tool_result(self):
		m = _agent_message_adapter.validate_python({
			"role": "toolResult", "toolCallId": "tc1", "toolName": "bash",
			"content": [{"type": "text", "text": "done"}]
		})
		assert isinstance(m, ToolResultMessage)
		assert m.toolName == "bash"
	
	def test_bash_execution(self):
		m = _agent_message_adapter.validate_python({"role": "bashExecution", "command": "ls", "output": "file1"})
		assert isinstance(m, BashExecutionMessage)
		assert m.command == "ls"
		assert m.exitCode is None
	
	def test_roundtrip(self):
		for raw in [
			{"role": "user", "content": "hi"},
			{"role": "assistant", "content": [{"type": "text", "text": "ok"}]},
			{"role": "toolResult", "toolCallId": "t1", "toolName": "bash", "content": []},
			{"role": "bashExecution", "command": "pwd", "output": "/home"},
			{"role": "custom", "customType": "echo", "content": "hello"},
			{"role": "branchSummary", "summary": "branch", "fromId": "f1"},
			{"role": "compactionSummary", "summary": "compacted", "tokensBefore": 1000},
		]:
			m = _agent_message_adapter.validate_python(raw)
			js = _agent_message_adapter.dump_json(m)
			m2 = _agent_message_adapter.validate_json(js)
			assert m2 == m, f"Failed roundtrip for {raw['role']}"


class TestToolExecutionResult:
	
	def test_defaults(self):
		r = ToolExecutionResult()
		assert r.content == []
		assert r.details is None
	
	def test_roundtrip(self):
		r = ToolExecutionResult(content=[{"type": "text", "text": "result"}])
		r2 = ToolExecutionResult.model_validate_json(r.model_dump_json())
		assert r2 == r


class TestCompactionResult:
	
	def test_roundtrip(self):
		r = CompactionResult(summary="compacted", tokensBefore=2000, estimatedTokensAfter=500)
		r2 = CompactionResult.model_validate_json(r.model_dump_json())
		assert r2 == r


class TestSessionStats:
	
	def test_roundtrip(self):
		s = SessionStatsData(sessionFile="/tmp/s", sessionId="s1", tokens={"input": 10, "output": 20, "total": 30})
		s2 = SessionStatsData.model_validate_json(s.model_dump_json())
		assert s2 == s


class TestSessionEntry:
	
	def test_roundtrip(self):
		e = SessionEntry(type="message", id="e1", timestamp="2024-01-01T00:00:00Z",
			message={"role": "user", "content": "hi"})
		e2 = SessionEntry.model_validate_json(e.model_dump_json())
		assert e2 == e


class TestTreeEntry:
	
	def test_roundtrip(self):
		t = TreeEntry(entry={"type": "message", "id": "e1", "timestamp": "..."}, label="root")
		t2 = TreeEntry.model_validate_json(t.model_dump_json())
		assert t2 == t


class TestResponseData:
	
	def test_state_data(self):
		d = StateData(isStreaming=True, messageCount=5, autoCompactionEnabled=True)
		assert d.isStreaming
		assert d.model is None
	
	def test_bash_data(self):
		d = BashData(output="hello", exitCode=0)
		assert d.output == "hello"
	
	def test_models_data(self):
		d = ModelsData(models=[{"id": "m1", "name": "Model 1", "provider": "test"}])
		assert len(d.models) == 1
		assert d.models[0].id == "m1"
	
	def test_levels_data(self):
		d = LevelsData(levels=["low", "medium", "high"])
		assert len(d.levels) == 3
	
	def test_fork_messages_data(self):
		d = ForkMessagesData(messages=[{"entryId": "e1", "text": "hi"}])
		assert d.messages[0].entryId == "e1"
	
	def test_entries_data(self):
		d = EntriesData(entries=[{"type": "message", "id": "e1", "timestamp": "..."}], leafId="e1")
		assert d.leafId == "e1"
	
	def test_tree_data(self):
		d = TreeData(tree=[{"entry": {"type": "message", "id": "e1", "timestamp": "..."}}])
		assert len(d.tree) == 1
	
	def test_last_assistant_text_data(self):
		d = LastAssistantTextData(text="hello")
		assert d.text == "hello"
		d2 = LastAssistantTextData()
		assert d2.text is None
	
	def test_export_html_data(self):
		d = ExportHtmlData(path="/tmp/report.html")
		assert d.path == "/tmp/report.html"
	
	def test_cancelled_data(self):
		d = CancelledData(cancelled=True)
		assert d.cancelled
	
	def test_fork_data(self):
		d = ForkData(text="forked", cancelled=False)
		assert d.text == "forked"
	
	def test_command_info(self):
		ci = CommandInfo(name="prompt", source="builtin")
		assert ci.name == "prompt"
		d = CommandsData(commands=[{"name": "prompt", "source": "builtin", "description": "Send a prompt"}])
		assert d.commands[0].description == "Send a prompt"
	
	def test_messages_data(self):
		d = MessagesData(messages=[{"role": "user", "content": "hi"}])
		assert len(d.messages) == 1
		assert isinstance(d.messages[0], UserMessage)
	
	def test_cycle_model_data(self):
		d = CycleModelData(model={"id": "m1", "name": "M1", "provider": "test"}, thinkingLevel="high", isScoped=True)
		assert d.model is not None and d.model.id == "m1"
		assert d.isScoped