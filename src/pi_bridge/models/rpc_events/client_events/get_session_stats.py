from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class GetSessionStatsCommand(BaseCommand):
	
	"""GetSessionStatsCommand RPC 指令"""
	
	type: Literal["get_session_stats"] = Field(default="get_session_stats", description="指令类型")
