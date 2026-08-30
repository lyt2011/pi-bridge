from .base_command	import BaseCommand

from typing		import Literal


class AbortRetryCommand(BaseCommand):
	
	"""AbortRetryCommand RPC 指令"""
	
	type: Literal["abort_retry"] = "abort_retry"
