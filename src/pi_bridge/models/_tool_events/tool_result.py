from .base_tool_event	import PrivateToolEvent

from pydantic	import Field


class PrivateToolResult(PrivateToolEvent):
	
	type: str = Field(default="tool_result", description="事件类型")
	
	result: str	= Field(..., description="工具输出")