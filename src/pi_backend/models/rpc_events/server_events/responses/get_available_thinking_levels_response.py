from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class GetAvailableThinkingLevelsResponse(BaseResponse):
	
	"""GetAvailableThinkingLevelsResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_AVAILABLE_THINKING_LEVELS] = CommandEnum.GET_AVAILABLE_THINKING_LEVELS
