from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class AbortResponse(BaseResponse):
	
	"""AbortResponse 响应模型"""
	
	command: Literal[CommandEnum.ABORT] = CommandEnum.ABORT
