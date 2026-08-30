from .base_command	import BaseCommand

from typing		import Literal


class GetAvailableModelsCommand(BaseCommand):
	
	"""GetAvailableModelsCommand RPC 指令"""
	
	type: Literal["get_available_models"] = "get_available_models"
