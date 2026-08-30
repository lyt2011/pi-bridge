from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class GetAvailableModelsResponse(BaseResponse):
	
	"""GetAvailableModelsResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_AVAILABLE_MODELS] = CommandEnum.GET_AVAILABLE_MODELS
