from .base_tool_event	import BaseToolEvent

from pydantic	import Field
from typing		import Optional


class ToolExecutionEnd(BaseToolEvent):
	
	type: str = "tool_execution_end"
	
	reason: Optional[str]	= Field(default=None, description="工具结束原因")