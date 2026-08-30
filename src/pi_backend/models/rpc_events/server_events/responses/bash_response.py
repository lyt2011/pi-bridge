from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class BashResponse(BaseResponse):
	
	"""BashResponse 响应模型"""
	
	command: Literal[CommandEnum.BASH] = CommandEnum.BASH
