from .base_tool_event	import PrivateToolEvent

from pydantic	import Field
from typing		import Optional


class PrivateToolExecutionEnd(PrivateToolEvent):
	
	type: str = "tool_execution_end"
	
	reason: Optional[str]	= Field(default=None, description="工具结束原因")