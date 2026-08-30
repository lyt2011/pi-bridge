from .base_command	import BaseCommand

from typing		import Literal


class AbortCommand(BaseCommand):
	
	"""AbortCommand RPC 指令"""
	
	type: Literal["abort"] = "abort"
