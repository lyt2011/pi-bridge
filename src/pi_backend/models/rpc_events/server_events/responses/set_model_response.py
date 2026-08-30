from ..base_response	import BaseResponse
from typing		import Literal


class SetModelResponse(BaseResponse):
	
	"""SetModelResponse 响应模型"""
	
	command: Literal["set_model"] = "set_model"
