from .base_command	import BaseCommand

from typing		import Literal, Optional
from pydantic	import Field


class CompactCommand(BaseCommand):
	
	"""CompactCommand RPC 指令"""
	
	type: Literal["compact"] = "compact"
	
	customInstructions: Optional[str]	= Field(default=None, description="自定义压缩指令")
