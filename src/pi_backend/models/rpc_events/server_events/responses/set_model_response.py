from ..base_response	import BaseResponse


class SetModelResponse(BaseResponse):
	
	"""SetModelResponse 响应模型"""
	
	command: str = "set_model"
