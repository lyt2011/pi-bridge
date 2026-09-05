from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class GetStateCommand(BaseCommand):
	
	"""GetStateCommand RPC 指令"""
	
	type: Literal["get_state"] = Field(default="get_state", description="指令类型")
