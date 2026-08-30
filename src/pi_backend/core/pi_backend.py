from .pi_tool_backend	import PIToolBackend
from .pi_process		import PIProcess

from ..factory		import responses_factory, events_factory

from ..models	import (
	BaseCommand,
	BaseRPCEvent,
	BaseResponse,
	BaseEvent,
	# Prompting
	PromptCommand,
	SteerCommand,
	FollowUpCommand,
	AbortCommand,
	ClearQueueCommand,
	NewSessionCommand,
	# State
	GetStateCommand,
	GetMessagesCommand,
	# Model
	SetModelCommand,
	CycleModelCommand,
	GetAvailableModelsCommand,
	# Thinking
	SetThinkingLevelCommand,
	CycleThinkingLevelCommand,
	GetAvailableThinkingLevelsCommand,
	# Queue Modes
	SetSteeringModeCommand,
	SetFollowUpModeCommand,
	# Compaction
	CompactCommand,
	SetAutoCompactionCommand,
	# Retry
	SetAutoRetryCommand,
	AbortRetryCommand,
	# Bash
	BashCommand,
	AbortBashCommand,
	# Session
	GetSessionStatsCommand,
	ExportHtmlCommand,
	SwitchSessionCommand,
	ForkCommand,
	CloneCommand,
	GetForkMessagesCommand,
	GetEntriesCommand,
	GetTreeCommand,
	GetLastAssistantTextCommand,
	SetSessionNameCommand,
	# Commands
	GetCommandsCommand,
)

from typing	import Dict, Any, Optional, List, Literal

from easy_factory	import DispatchFailed

import orjson


class PIBackend:
	
	"""
	PI 后端最高层封装
	"""

	def __init__(
		self, *,
		pi_process	: PIProcess,
		tool_backend: Optional[PIToolBackend] = None,
	) -> None:
		
		self.tool_backend	= tool_backend
		self.pi_process		= pi_process
	
	async def read_raw(self) -> Dict[str, Any]:
		
		"""读取一行 JSON 并返回原始字典"""
		
		line = await self.pi_process.read_line()
		
		return orjson.loads(line)
	
	async def read_pydantic(self) -> BaseRPCEvent:
		
		"""读取一行 JSON 并解析为对应的响应/事件模型"""
		
		data = await self.read_raw()
		
		# 优先匹配响应模型; 非响应行 (事件/扩展UI请求等) 回退到事件工厂
		try:
			return responses_factory.dispatcher(data)
		except DispatchFailed:
			return events_factory.dispatcher(data)
	
	async def write_jsonl(self, msg: str) -> None:
		
		"""通过 PIProcess.write_line 写入一行 JSON"""
		
		if not isinstance(msg, str):
			raise TypeError(f"msg must be str, not {type(msg).__name__}")
		
		await self.pi_process.write_line(msg)
	
	async def prompt(
		self,
		message: str,
		images: Optional[List[Dict[str, Any]]] = None,
		streaming_behavior: Optional[Literal["steer", "followUp"]] = None,
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 prompt 指令"""
		
		prompt_msg = PromptCommand(id=request_id, message=message, images=images, streamingBehavior=streaming_behavior,)
		
		await self._send_command(prompt_msg)
	
	async def steer(
		self,
		message: str,
		images: Optional[List[Dict[str, Any]]] = None,
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 steer 指令"""
		
		await self._send_command(SteerCommand(message=message, images=images, id=request_id))
	
	async def follow_up(
		self,
		message: str,
		images: Optional[List[Dict[str, Any]]] = None,
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 follow_up 指令(排队投递)
		
		⚠️ pi 的 follow_up 是"排队"语义:消息进入队列,但**空闲时不触发新处理**。
		只有在 agent 正在运行时(流式中)或后续 prompt 启动新 run 时,才会被消费。
		实证:agent_settled 后发 follow_up,只会收到 queue_update + response,
		不会有任何 agent_start/turn_start/message_start;需再发一条 prompt 才会
		连带消费队列里的 follow_up(表现为第二次 turn)。
		因此:若 agent 已空闲,请改用 prompt() 而非 follow_up()。
		"""
		
		await self._send_command(FollowUpCommand(message=message, images=images, id=request_id))
	
	async def abort(self, request_id: Optional[str] = None) -> None:
		
		"""发送 abort 指令"""
		
		await self._send_command(AbortCommand(id=request_id))
	
	async def clear_queue(self, request_id: Optional[str] = None) -> None:
		
		"""发送 clear_queue 指令"""
		
		await self._send_command(ClearQueueCommand(id=request_id))
	
	async def new_session(
		self,
		parent_session: Optional[str] = None,
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 new_session 指令"""
		
		await self._send_command(NewSessionCommand(parentSession=parent_session, id=request_id))
	
	async def get_state(self, request_id: Optional[str] = None) -> None:
		
		"""发送 get_state 指令"""
		
		await self._send_command(GetStateCommand(id=request_id))
	
	async def get_messages(self, request_id: Optional[str] = None) -> None:
		
		"""发送 get_messages 指令"""
		
		await self._send_command(GetMessagesCommand(id=request_id))
	
	async def set_model(
		self,
		provider: str,
		model_id: str,
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 set_model 指令"""
		
		await self._send_command(SetModelCommand(provider=provider, modelId=model_id, id=request_id))
	
	async def cycle_model(self, request_id: Optional[str] = None) -> None:
		
		"""发送 cycle_model 指令"""
		
		await self._send_command(CycleModelCommand(id=request_id))
	
	async def get_available_models(self, request_id: Optional[str] = None) -> None:
		
		"""发送 get_available_models 指令"""
		
		await self._send_command(GetAvailableModelsCommand(id=request_id))
	
	async def set_thinking_level(
		self,
		level	: str,
		request_id	: Optional[str] = None
	) -> None:
		
		"""发送 set_thinking_level 指令"""
		
		await self._send_command(SetThinkingLevelCommand(level=level, id=request_id))
	
	async def cycle_thinking_level(self, request_id: Optional[str] = None) -> None:
		
		"""发送 cycle_thinking_level 指令"""
		
		await self._send_command(CycleThinkingLevelCommand(id=request_id))
	
	async def get_available_thinking_levels(self, request_id: Optional[str] = None) -> None:
		
		"""发送 get_available_thinking_levels 指令"""
		
		await self._send_command(GetAvailableThinkingLevelsCommand(id=request_id))
	
	async def set_steering_mode(
		self,
		mode: Literal["all", "one-at-a-time"],
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 set_steering_mode 指令"""
		
		await self._send_command(SetSteeringModeCommand(mode=mode, id=request_id))
	
	async def set_follow_up_mode(
		self,
		mode: Literal["all", "one-at-a-time"],
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 set_follow_up_mode 指令"""
		
		await self._send_command(SetFollowUpModeCommand(mode=mode, id=request_id))
	
	async def compact(
		self,
		custom_instructions: Optional[str] = None,
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 compact 指令"""
		
		await self._send_command(CompactCommand(customInstructions=custom_instructions, id=request_id))
	
	async def set_auto_compaction(self, enabled: bool, request_id: Optional[str] = None) -> None:
		
		"""发送 set_auto_compaction 指令"""
		
		await self._send_command(SetAutoCompactionCommand(enabled=enabled, id=request_id))
	
	async def set_auto_retry(self, enabled: bool, request_id: Optional[str] = None) -> None:
		
		"""发送 set_auto_retry 指令"""
		
		await self._send_command(SetAutoRetryCommand(enabled=enabled, id=request_id))
	
	async def abort_retry(self, request_id: Optional[str] = None) -> None:
		
		"""发送 abort_retry 指令"""
		
		await self._send_command(AbortRetryCommand(id=request_id))
	
	async def bash(
		self,
		command: str,
		exclude_from_context: Optional[bool] = None,
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 bash 指令"""
		
		await self._send_command(BashCommand(command=command, excludeFromContext=exclude_from_context, id=request_id))
	
	async def abort_bash(self, request_id: Optional[str] = None) -> None:
		
		"""发送 abort_bash 指令"""
		
		await self._send_command(AbortBashCommand(id=request_id))
	
	async def get_session_stats(self, request_id: Optional[str] = None) -> None:
		
		"""发送 get_session_stats 指令"""
		
		await self._send_command(GetSessionStatsCommand(id=request_id))
	
	async def export_html(
		self,
		output_path: Optional[str] = None,
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 export_html 指令"""
		
		await self._send_command(ExportHtmlCommand(outputPath=output_path, id=request_id))
	
	async def switch_session(
		self,
		session_path: str,
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 switch_session 指令"""
		
		await self._send_command(SwitchSessionCommand(sessionPath=session_path, id=request_id))
	
	async def fork(self, entry_id: str, request_id: Optional[str] = None) -> None:
		
		"""发送 fork 指令"""
		
		await self._send_command(ForkCommand(entryId=entry_id, id=request_id))
	
	async def clone(self, request_id: Optional[str] = None) -> None:
		
		"""发送 clone 指令"""
		
		await self._send_command(CloneCommand(id=request_id))
	
	async def get_fork_messages(self, request_id: Optional[str] = None) -> None:
		
		"""发送 get_fork_messages 指令"""
		
		await self._send_command(GetForkMessagesCommand(id=request_id))
	
	async def get_entries(
		self,
		since: Optional[str] = None,
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 get_entries 指令"""
		
		await self._send_command(GetEntriesCommand(since=since, id=request_id))
	
	async def get_tree(self, request_id: Optional[str] = None) -> None:
		
		"""发送 get_tree 指令"""
		
		await self._send_command(GetTreeCommand(id=request_id))
	
	async def get_last_assistant_text(self, request_id: Optional[str] = None) -> None:
		
		"""发送 get_last_assistant_text 指令"""
		
		await self._send_command(GetLastAssistantTextCommand(id=request_id))
	
	async def set_session_name(
		self,
		name: str,
		request_id: Optional[str] = None
	) -> None:
		
		"""发送 set_session_name 指令"""
		
		await self._send_command(SetSessionNameCommand(name=name, id=request_id))
	
	async def get_commands(self, request_id: Optional[str] = None) -> None:
		
		"""发送 get_commands 指令"""
		
		await self._send_command(GetCommandsCommand(id=request_id))
	
	async def _send_command(self, command: BaseCommand) -> None:
		
		"""将指令模型序列化为 JSONL 并写入子进程 stdin"""
		
		await self.write_jsonl(command.model_dump_json(exclude_none=True))
