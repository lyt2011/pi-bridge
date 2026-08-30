from .base_tool_event	import PrivateToolEvent

from pydantic	import Field


class PrivateToolResult(PrivateToolEvent):
	
	type: str = "tool_result"
	
	result: str	= Field(..., description="工具输出")