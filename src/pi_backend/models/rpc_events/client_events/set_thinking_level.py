from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class SetThinkingLevelCommand(BaseCommand):
	
	"""SetThinkingLevelCommand RPC 指令"""
	
	type: Literal["set_thinking_level"] = "set_thinking_level"
	
	level: Literal["off", "minimal", "low", "medium", "high", "xhigh", "max"]	= Field(..., description="思考级别")
