from ..base_response	import BaseResponse
from typing		import Literal


class GetAvailableModelsResponse(BaseResponse):
	
	"""GetAvailableModelsResponse 响应模型"""
	
	command: Literal["get_available_models"] = "get_available_models"
