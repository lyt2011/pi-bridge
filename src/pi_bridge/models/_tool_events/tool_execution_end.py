from .base_tool_event	import PrivateToolEvent

from pydantic	import Field
from typing		import Optional


class PrivateToolExecutionEnd(PrivateToolEvent):
	
	type: str = Field(default="tool_execution_end", description="事件类型")
	
	reason: Optional[str]	= Field(default=None, description="工具结束原因")