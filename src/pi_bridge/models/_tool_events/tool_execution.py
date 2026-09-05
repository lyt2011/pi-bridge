from .base_tool_event	import PrivateToolEvent

from pydantic	import Field
from typing		import Dict, Any


class PrivateToolExecution(PrivateToolEvent):
	
	type: str = Field(default="tool_execution", description="事件类型")

	tool_name	: str				= Field(..., description="工具名")
	tool_params	: Dict[str, Any]	= Field(..., description="工具参数")