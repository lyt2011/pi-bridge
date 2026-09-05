from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class CycleThinkingLevelCommand(BaseCommand):
	
	"""CycleThinkingLevelCommand RPC 指令"""
	
	type: Literal["cycle_thinking_level"] = Field(default="cycle_thinking_level", description="指令类型")
