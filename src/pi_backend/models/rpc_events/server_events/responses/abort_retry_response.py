from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class AbortRetryResponse(BaseResponse):
	
	"""AbortRetryResponse 响应模型"""
	
	command: Literal[CommandEnum.ABORT_RETRY] = CommandEnum.ABORT_RETRY
