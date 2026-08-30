from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class CloneResponse(BaseResponse):
	
	"""CloneResponse 响应模型"""
	
	command: Literal[CommandEnum.CLONE] = CommandEnum.CLONE
