from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class GetSessionStatsResponse(BaseResponse):
	
	"""GetSessionStatsResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_SESSION_STATS] = CommandEnum.GET_SESSION_STATS
