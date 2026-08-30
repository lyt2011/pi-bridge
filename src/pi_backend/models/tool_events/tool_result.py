from .base_tool_event	import BaseToolEvent

from pydantic	import Field


class ToolResult(BaseToolEvent):
	
	type: str = "tool_result"
	
	result: str	= Field(..., description="工具输出")