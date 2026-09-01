from ...base_rpc_event	import BaseRPCEvent
from ...._shared	import AgentMessage, ToolExecutionResult

from typing		import Literal, List, Optional
from pydantic	import Field



class TurnEndEvent(BaseRPCEvent):
	
	"""TurnEndEvent 事件模型"""
	
	type: Literal["turn_end"] = Field(default="turn_end", description="事件类型")
	message: Optional[AgentMessage] = Field(default=None, description="助手消息")
	toolResults: List[ToolExecutionResult] = Field(default_factory=list, description="工具执行结果列表")
