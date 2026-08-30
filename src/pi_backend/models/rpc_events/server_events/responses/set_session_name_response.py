from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class SetSessionNameResponse(BaseResponse):
	
	"""SetSessionNameResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_SESSION_NAME] = CommandEnum.SET_SESSION_NAME
