from .base_command	import BaseCommand

from typing		import Literal


class CycleModelCommand(BaseCommand):
	
	"""CycleModelCommand RPC 指令"""
	
	type: Literal["cycle_model"] = "cycle_model"
