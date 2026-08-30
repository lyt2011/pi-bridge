from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class SetModelResponse(BaseResponse):
	
	"""SetModelResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_MODEL] = CommandEnum.SET_MODEL
