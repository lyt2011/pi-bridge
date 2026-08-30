from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class SwitchSessionResponse(BaseResponse):
	
	"""SwitchSessionResponse 响应模型"""
	
	command: Literal[CommandEnum.SWITCH_SESSION] = CommandEnum.SWITCH_SESSION
