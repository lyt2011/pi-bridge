from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class GetAvailableModelsCommand(BaseCommand):
	
	"""GetAvailableModelsCommand RPC 指令"""
	
	type: Literal["get_available_models"] = Field(default="get_available_models", description="指令类型")
