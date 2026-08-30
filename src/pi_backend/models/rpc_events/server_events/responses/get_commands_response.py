from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class GetCommandsResponse(BaseResponse):
	
	"""GetCommandsResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_COMMANDS] = CommandEnum.GET_COMMANDS
