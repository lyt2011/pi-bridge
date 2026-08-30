from .base_command	import BaseCommand

from typing		import Literal


class CycleThinkingLevelCommand(BaseCommand):
	
	"""CycleThinkingLevelCommand RPC 指令"""
	
	type: Literal["cycle_thinking_level"] = "cycle_thinking_level"
