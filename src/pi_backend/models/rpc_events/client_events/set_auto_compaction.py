from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class SetAutoCompactionCommand(BaseCommand):
	
	"""SetAutoCompactionCommand RPC 指令"""
	
	type: Literal["set_auto_compaction"] = "set_auto_compaction"
	
	enabled: bool	= Field(..., description="是否启用自动压缩")
