from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class ForkResponse(BaseResponse):
	
	"""ForkResponse 响应模型"""
	
	command: Literal[CommandEnum.FORK] = CommandEnum.FORK
