from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class ClearQueueResponse(BaseResponse):
	
	"""ClearQueueResponse 响应模型"""
	
	command: Literal[CommandEnum.CLEAR_QUEUE] = CommandEnum.CLEAR_QUEUE
