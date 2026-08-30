from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class GetTreeResponse(BaseResponse):
	
	"""GetTreeResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_TREE] = CommandEnum.GET_TREE
