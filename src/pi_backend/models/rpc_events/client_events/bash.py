from .base_command	import BaseCommand

from typing		import Literal, Optional
from pydantic	import Field


class BashCommand(BaseCommand):
	
	"""BashCommand RPC 指令"""
	
	type: Literal["bash"] = "bash"
	
	command: str	= Field(..., description="要执行的shell命令")
	excludeFromContext: Optional[bool]	= Field(default=None, description="是否排除出上下文")
