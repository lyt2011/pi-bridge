from .base_command	import BaseCommand

from typing		import Literal


class GetTreeCommand(BaseCommand):
	
	"""GetTreeCommand RPC 指令"""
	
	type: Literal["get_tree"] = "get_tree"
