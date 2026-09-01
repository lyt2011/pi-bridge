from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class SetThinkingLevelCommand(BaseCommand):
	
	"""SetThinkingLevelCommand RPC 指令"""
	
	type: Literal["set_thinking_level"] = Field(default="set_thinking_level", description="指令类型")
	
	level: Literal["off", "minimal", "low", "medium", "high", "xhigh", "max"]	= Field(..., description="思考级别")
