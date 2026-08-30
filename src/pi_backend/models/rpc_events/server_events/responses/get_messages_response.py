from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class GetMessagesResponse(BaseResponse):
	
	"""GetMessagesResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_MESSAGES] = CommandEnum.GET_MESSAGES
