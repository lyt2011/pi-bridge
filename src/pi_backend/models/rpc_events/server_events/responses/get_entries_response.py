from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class GetEntriesResponse(BaseResponse):
	
	"""GetEntriesResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_ENTRIES] = CommandEnum.GET_ENTRIES
