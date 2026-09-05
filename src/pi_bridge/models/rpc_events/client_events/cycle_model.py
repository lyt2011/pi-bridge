from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class CycleModelCommand(BaseCommand):
	
	"""CycleModelCommand RPC 指令"""
	
	type: Literal["cycle_model"] = Field(default="cycle_model", description="指令类型")
