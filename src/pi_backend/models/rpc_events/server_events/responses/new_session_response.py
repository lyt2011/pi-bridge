from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class NewSessionResponse(BaseResponse):
	
	"""NewSessionResponse 响应模型"""
	
	command: Literal[CommandEnum.NEW_SESSION] = CommandEnum.NEW_SESSION
