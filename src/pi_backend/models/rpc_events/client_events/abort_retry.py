from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class AbortRetryCommand(BaseCommand):
	
	"""AbortRetryCommand RPC 指令"""
	
	type: Literal["abort_retry"] = Field(default="abort_retry", description="指令类型")
