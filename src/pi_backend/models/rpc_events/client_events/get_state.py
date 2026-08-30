from .base_command	import BaseCommand

from typing		import Literal


class GetStateCommand(BaseCommand):
	
	"""GetStateCommand RPC 指令"""
	
	type: Literal["get_state"] = "get_state"
