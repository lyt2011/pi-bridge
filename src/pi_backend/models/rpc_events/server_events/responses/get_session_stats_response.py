from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import SessionStatsData
from typing		import Literal, Optional
from pydantic	import Field


class GetSessionStatsResponse(BaseResponse):
	
	"""GetSessionStatsResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_SESSION_STATS] = Field(default=CommandEnum.GET_SESSION_STATS, description="响应指令类型")
	data: Optional[SessionStatsData]	= Field(default=None, description="get session stats 响应数据")

