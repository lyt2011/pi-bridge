from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class ForkCommand(BaseCommand):
	
	"""ForkCommand RPC 指令"""
	
	type: Literal["fork"] = "fork"
	
	entryId: str	= Field(..., description="要分叉的用户消息entry ID")
