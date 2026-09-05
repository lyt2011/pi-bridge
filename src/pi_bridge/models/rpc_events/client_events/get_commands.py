from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class GetCommandsCommand(BaseCommand):
	
	"""GetCommandsCommand RPC 指令"""
	
	type: Literal["get_commands"] = Field(default="get_commands", description="指令类型")
