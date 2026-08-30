from .base_command	import BaseCommand

from typing		import Literal


class GetCommandsCommand(BaseCommand):
	
	"""GetCommandsCommand RPC 指令"""
	
	type: Literal["get_commands"] = "get_commands"
