from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class GetForkMessagesResponse(BaseResponse):
	
	"""GetForkMessagesResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_FORK_MESSAGES] = CommandEnum.GET_FORK_MESSAGES
