from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class CompactResponse(BaseResponse):
	
	"""CompactResponse 响应模型"""
	
	command: Literal[CommandEnum.COMPACT] = CommandEnum.COMPACT
