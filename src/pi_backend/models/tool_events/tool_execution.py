from .base_tool_event	import BaseToolEvent

from pydantic	import Field
from typing		import Dict, Any


class ToolExecution(BaseToolEvent):
	
	type: str = "tool_execution"

	tool_name	: str				= Field(..., description="工具名")
	tool_param	: Dict[str, Any]	= Field(..., description="工具参数")