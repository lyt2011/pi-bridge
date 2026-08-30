from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class AbortBashResponse(BaseResponse):
	
	"""AbortBashResponse 响应模型"""
	
	command: Literal[CommandEnum.ABORT_BASH] = CommandEnum.ABORT_BASH
