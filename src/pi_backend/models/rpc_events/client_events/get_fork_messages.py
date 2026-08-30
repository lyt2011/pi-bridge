from .base_command	import BaseCommand

from typing		import Literal


class GetForkMessagesCommand(BaseCommand):
	
	"""GetForkMessagesCommand RPC 指令"""
	
	type: Literal["get_fork_messages"] = "get_fork_messages"
