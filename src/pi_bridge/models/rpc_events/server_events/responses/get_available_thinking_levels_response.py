from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import LevelsData
from typing		import Literal, Optional
from pydantic	import Field


class GetAvailableThinkingLevelsResponse(BaseResponse):
	
	"""GetAvailableThinkingLevelsResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_AVAILABLE_THINKING_LEVELS] = Field(default=CommandEnum.GET_AVAILABLE_THINKING_LEVELS, description="响应指令类型")
	data: Optional[LevelsData]	= Field(default=None, description="get available thinking levels 响应数据")

