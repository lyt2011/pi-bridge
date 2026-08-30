from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class ToolExecutionEndEvent(BaseRPCEvent):
	
	"""ToolExecutionEndEvent 事件模型"""
	
	type: Literal["tool_execution_end"] = "tool_execution_end"
	toolCallId: str = Field(default="", description="工具调用 ID")
	toolName: str = Field(default="", description="工具名")
	result: Dict[str, Any] = Field(default_factory=dict, description="最终执行结果")
	isError: bool = Field(default=False, description="是否出错")
