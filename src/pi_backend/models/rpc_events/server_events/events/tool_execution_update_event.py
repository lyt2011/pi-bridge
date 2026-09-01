from ...base_rpc_event	import BaseRPCEvent
from ...._shared	import ToolExecutionResult

from typing		import Literal, Dict, Any, Optional
from pydantic	import Field



class ToolExecutionUpdateEvent(BaseRPCEvent):
	
	"""ToolExecutionUpdateEvent 事件模型"""
	
	type: Literal["tool_execution_update"] = Field(default="tool_execution_update", description="事件类型")
	toolCallId: str = Field(default="", description="工具调用 ID")
	toolName: str = Field(default="", description="工具名")
	args: Dict[str, Any] = Field(default_factory=dict, description="工具参数")
	partialResult: Optional[ToolExecutionResult] = Field(default=None, description="已累积的部分结果")
