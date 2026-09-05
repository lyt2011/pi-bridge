from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class GetTreeCommand(BaseCommand):
	
	"""GetTreeCommand RPC 指令"""
	
	type: Literal["get_tree"] = Field(default="get_tree", description="指令类型")
