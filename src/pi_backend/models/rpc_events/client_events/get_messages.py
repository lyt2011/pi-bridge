from .base_command	import BaseCommand

from typing		import Literal


class GetMessagesCommand(BaseCommand):
	
	"""GetMessagesCommand RPC 指令"""
	
	type: Literal["get_messages"] = "get_messages"
