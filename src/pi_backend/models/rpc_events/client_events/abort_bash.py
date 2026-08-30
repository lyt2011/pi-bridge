from .base_command	import BaseCommand

from typing		import Literal


class AbortBashCommand(BaseCommand):
	
	"""AbortBashCommand RPC 指令"""
	
	type: Literal["abort_bash"] = "abort_bash"
