from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class GetMessagesCommand(BaseCommand):
	
	"""GetMessagesCommand RPC 指令"""
	
	type: Literal["get_messages"] = Field(default="get_messages", description="指令类型")
