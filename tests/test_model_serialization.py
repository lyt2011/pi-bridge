"""模型序列化往返测试

覆盖范围：
1. model_dump_json() 后再 model_validate_json() 得到相等对象
2. 断言判别字段值（如 StateResponse 的 command 序列化后是字符串 "get_state"）
3. 事件模型序列化往返
"""

from pi_backend.models import (
    StateResponse,
    PromptResponse,
    SetModelResponse,
    GetAvailableModelsResponse,
    GetLastAssistantTextResponse,
    BashResponse,
    AgentStartEvent,
    MessageUpdateEvent,
    BashExecutionUpdateEvent,
    ToolExecutionStartEvent,
    QueueUpdateEvent,
    ExtensionUIRequestEvent,
    CompactionEndEvent,
    AutoRetryStartEvent,
)
from pi_backend.enums import CommandEnum


# ─── 响应模型序列化往返 ───

def test_state_response_roundtrip():
    obj = StateResponse(
        command="get_state", success=True, id="r1",
        data={"isStreaming": True, "messageCount": 5, "thinkingLevel": "medium"},
    )
    obj2 = StateResponse.model_validate_json(obj.model_dump_json())
    assert obj2 == obj
    assert obj2.data is not None
    assert obj2.data.isStreaming is True
    assert obj2.data.messageCount == 5
    assert obj2.data.thinkingLevel == "medium"


def test_state_response_command_serializes_to_string():
    """StateResponse.command 序列化后是字符串 'get_state'"""
    obj = StateResponse(command="get_state", success=True)
    dumped = obj.model_dump_json()
    assert '"get_state"' in dumped


def test_prompt_response_roundtrip():
    obj = PromptResponse(command="prompt", success=True)
    obj2 = PromptResponse.model_validate_json(obj.model_dump_json())
    assert obj2 == obj


def test_prompt_response_command_serializes_to_string():
    obj = PromptResponse(command="prompt", success=True)
    dumped = obj.model_dump_json()
    assert '"prompt"' in dumped


def test_set_model_response_roundtrip():
    obj = SetModelResponse(command="set_model", success=True)
    obj2 = SetModelResponse.model_validate_json(obj.model_dump_json())
    assert obj2 == obj


def test_get_available_models_response_roundtrip():
    obj = GetAvailableModelsResponse(command="get_available_models", success=True)
    obj2 = GetAvailableModelsResponse.model_validate_json(obj.model_dump_json())
    assert obj2 == obj


def test_get_last_assistant_text_response_roundtrip():
    obj = GetLastAssistantTextResponse(command="get_last_assistant_text", success=True)
    obj2 = GetLastAssistantTextResponse.model_validate_json(obj.model_dump_json())
    assert obj2 == obj


def test_bash_response_roundtrip_with_error():
    """带 error 字段的响应模型往返"""
    obj = BashResponse(command="bash", success=False, error="command not found")
    obj2 = BashResponse.model_validate_json(obj.model_dump_json())
    assert obj2 == obj
    assert obj2.error == "command not found"


def test_serialized_command_is_literal_string():
    """所有响应模型序列化后 command 是字符串而非枚举对象"""
    for cmd_name, cls in [
        ("get_state", StateResponse),
        ("prompt", PromptResponse),
        ("set_model", SetModelResponse),
        ("get_available_models", GetAvailableModelsResponse),
        ("get_last_assistant_text", GetLastAssistantTextResponse),
        ("bash", BashResponse),
    ]:
        obj = cls(command=cmd_name, success=True)
        j = obj.model_dump_json()
        # 确认 command 是 JSON 字符串值而非枚举对象
        assert f'"command":"{cmd_name}"' in j.replace(" ", "")


# ─── 事件模型序列化往返 ───

def test_agent_start_event_roundtrip():
    obj = AgentStartEvent()
    obj2 = AgentStartEvent.model_validate_json(obj.model_dump_json())
    assert obj2 == obj


def test_message_update_event_roundtrip():
    obj = MessageUpdateEvent(
        usage={"input": 10, "output": 20, "cacheRead": 0, "cacheWrite": 0, "totalTokens": 30},
        assistantMessageEvent={"type": "text_delta", "contentIndex": 0, "delta": "hi"},
    )
    obj2 = MessageUpdateEvent.model_validate_json(obj.model_dump_json())
    assert obj2 == obj
    assert obj2.usage is not None and obj2.usage.totalTokens == 30
    assert obj2.assistantMessageEvent is not None
    assert obj2.assistantMessageEvent.type == "text_delta"


def test_bash_execution_update_event_roundtrip():
    obj = BashExecutionUpdateEvent(id="b1", delta="hello\nworld")
    obj2 = BashExecutionUpdateEvent.model_validate_json(obj.model_dump_json())
    assert obj2 == obj


def test_tool_execution_start_event_roundtrip():
    obj = ToolExecutionStartEvent(toolCallId="tc1", toolName="bash", args={"command": "ls"})
    obj2 = ToolExecutionStartEvent.model_validate_json(obj.model_dump_json())
    assert obj2 == obj


def test_queue_update_event_roundtrip():
    obj = QueueUpdateEvent(steering=["s1"], followUp=["f1"])
    obj2 = QueueUpdateEvent.model_validate_json(obj.model_dump_json())
    assert obj2 == obj


def test_extension_ui_request_event_roundtrip():
    obj = ExtensionUIRequestEvent(method="select", options=["a", "b"], title="选择")
    obj2 = ExtensionUIRequestEvent.model_validate_json(obj.model_dump_json())
    assert obj2 == obj


def test_compaction_end_event_roundtrip():
    obj = CompactionEndEvent(reason="manual", aborted=False, willRetry=False)
    obj2 = CompactionEndEvent.model_validate_json(obj.model_dump_json())
    assert obj2 == obj


def test_auto_retry_start_event_roundtrip():
    obj = AutoRetryStartEvent(attempt=1, maxAttempts=3, delayMs=1000, errorMessage="timeout")
    obj2 = AutoRetryStartEvent.model_validate_json(obj.model_dump_json())
    assert obj2 == obj


def test_event_type_serializes_to_string():
    """事件模型序列化后 type 是字符串"""
    obj = AgentStartEvent()
    dumped = obj.model_dump_json()
    assert '"agent_start"' in dumped
    obj2 = BashExecutionUpdateEvent(delta="test")
    dumped2 = obj2.model_dump_json()
    assert '"bash_execution_update"' in dumped2