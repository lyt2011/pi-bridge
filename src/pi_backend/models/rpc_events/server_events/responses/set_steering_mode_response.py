from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class SetSteeringModeResponse(BaseResponse):
	
	"""SetSteeringModeResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_STEERING_MODE] = CommandEnum.SET_STEERING_MODE
