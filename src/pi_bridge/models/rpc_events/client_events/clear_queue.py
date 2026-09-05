from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class ClearQueueCommand(BaseCommand):
	
	"""ClearQueueCommand RPC 指令"""
	
	type: Literal["clear_queue"] = Field(default="clear_queue", description="指令类型")
