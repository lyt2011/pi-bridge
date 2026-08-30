from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class ToolExecutionStartEvent(BaseRPCEvent):
	
	"""ToolExecutionStartEvent 事件模型"""
	
	type: Literal["tool_execution_start"] = "tool_execution_start"
	toolCallId: str = Field(default="", description="工具调用 ID")
	toolName: str = Field(default="", description="工具名")
	args: Dict[str, Any] = Field(default_factory=dict, description="工具参数")
