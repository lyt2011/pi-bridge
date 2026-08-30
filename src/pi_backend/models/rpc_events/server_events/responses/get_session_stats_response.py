from ..base_response	import BaseResponse


class GetSessionStatsResponse(BaseResponse):
	
	"""GetSessionStatsResponse 响应模型"""
	
	command: str = "get_session_stats"
