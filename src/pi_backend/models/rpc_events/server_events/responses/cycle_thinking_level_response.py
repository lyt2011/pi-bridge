from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class CycleThinkingLevelResponse(BaseResponse):
	
	"""CycleThinkingLevelResponse 响应模型"""
	
	command: Literal[CommandEnum.CYCLE_THINKING_LEVEL] = CommandEnum.CYCLE_THINKING_LEVEL
