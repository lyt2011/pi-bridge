from ...base_rpc_event	import BaseRPCEvent
from ...._shared	import ToolExecutionResult

from typing		import Literal, Optional
from pydantic	import Field



class ToolExecutionEndEvent(BaseRPCEvent):
	
	"""ToolExecutionEndEvent 事件模型"""
	
	type: Literal["tool_execution_end"] = Field(default="tool_execution_end", description="事件类型")
	toolCallId: str = Field(default="", description="工具调用 ID")
	toolName: str = Field(default="", description="工具名")
	result: Optional[ToolExecutionResult] = Field(default=None, description="最终执行结果")
	isError: bool = Field(default=False, description="是否出错")
