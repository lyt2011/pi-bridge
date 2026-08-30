from .base_command	import BaseCommand

from typing		import Literal


class GetAvailableThinkingLevelsCommand(BaseCommand):
	
	"""GetAvailableThinkingLevelsCommand RPC 指令"""
	
	type: Literal["get_available_thinking_levels"] = "get_available_thinking_levels"
