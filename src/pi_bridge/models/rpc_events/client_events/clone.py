from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class CloneCommand(BaseCommand):
	
	"""CloneCommand RPC 指令"""
	
	type: Literal["clone"] = Field(default="clone", description="指令类型")
