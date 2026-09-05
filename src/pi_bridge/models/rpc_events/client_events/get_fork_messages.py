from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class GetForkMessagesCommand(BaseCommand):
	
	"""GetForkMessagesCommand RPC 指令"""
	
	type: Literal["get_fork_messages"] = Field(default="get_fork_messages", description="指令类型")
