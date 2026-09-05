from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class AbortBashCommand(BaseCommand):
	
	"""AbortBashCommand RPC 指令"""
	
	type: Literal["abort_bash"] = Field(default="abort_bash", description="指令类型")
