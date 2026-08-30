from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class StateResponse(BaseResponse):
	
	"""StateResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_STATE] = CommandEnum.GET_STATE
