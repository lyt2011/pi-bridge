from .base_command	import BaseCommand

from typing		import Literal, Optional
from pydantic	import Field


class GetEntriesCommand(BaseCommand):
	
	"""GetEntriesCommand RPC 指令"""
	
	type: Literal["get_entries"] = Field(default="get_entries", description="指令类型")
	
	since: Optional[str]	= Field(default=None, description="游标entry ID，仅返回其后的entries")
