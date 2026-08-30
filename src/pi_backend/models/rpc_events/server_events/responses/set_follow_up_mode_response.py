from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class SetFollowUpModeResponse(BaseResponse):
	
	"""SetFollowUpModeResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_FOLLOW_UP_MODE] = CommandEnum.SET_FOLLOW_UP_MODE
