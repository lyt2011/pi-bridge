from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class SetThinkingLevelResponse(BaseResponse):
	
	"""SetThinkingLevelResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_THINKING_LEVEL] = CommandEnum.SET_THINKING_LEVEL
