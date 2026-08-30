from .base_command	import BaseCommand

from typing		import Literal


class GetSessionStatsCommand(BaseCommand):
	
	"""GetSessionStatsCommand RPC 指令"""
	
	type: Literal["get_session_stats"] = "get_session_stats"
