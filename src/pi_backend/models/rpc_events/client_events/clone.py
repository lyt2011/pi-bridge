from .base_command	import BaseCommand

from typing		import Literal


class CloneCommand(BaseCommand):
	
	"""CloneCommand RPC 指令"""
	
	type: Literal["clone"] = "clone"
