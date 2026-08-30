from ..base_response	import BaseResponse


class GetAvailableModelsResponse(BaseResponse):
	
	"""GetAvailableModelsResponse 响应模型"""
	
	command: str = "get_available_models"
