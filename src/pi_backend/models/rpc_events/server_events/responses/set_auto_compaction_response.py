from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class SetAutoCompactionResponse(BaseResponse):
	
	"""SetAutoCompactionResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_AUTO_COMPACTION] = CommandEnum.SET_AUTO_COMPACTION
