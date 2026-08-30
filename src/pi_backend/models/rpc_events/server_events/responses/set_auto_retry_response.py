from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class SetAutoRetryResponse(BaseResponse):
	
	"""SetAutoRetryResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_AUTO_RETRY] = CommandEnum.SET_AUTO_RETRY
