from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class SteerResponse(BaseResponse):
	
	"""SteerResponse 响应模型"""
	
	command: Literal[CommandEnum.STEER] = CommandEnum.STEER
