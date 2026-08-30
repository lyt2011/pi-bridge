from .base_command	import BaseCommand

from typing		import Literal


class ClearQueueCommand(BaseCommand):
	
	"""ClearQueueCommand RPC 指令"""
	
	type: Literal["clear_queue"] = "clear_queue"
