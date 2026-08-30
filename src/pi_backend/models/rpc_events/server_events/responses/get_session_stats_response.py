from ..base_response	import BaseResponse
from typing		import Literal


class GetSessionStatsResponse(BaseResponse):
	
	"""GetSessionStatsResponse 响应模型"""
	
	command: Literal["get_session_stats"] = "get_session_stats"
