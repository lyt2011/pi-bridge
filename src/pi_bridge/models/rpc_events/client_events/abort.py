from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class AbortCommand(BaseCommand):
	
	"""AbortCommand RPC 指令"""
	
	type: Literal["abort"] = Field(default="abort", description="指令类型")
