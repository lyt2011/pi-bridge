from ..base_response	import BaseResponse
from typing		import Literal


class CycleModelResponse(BaseResponse):
	
	"""CycleModelResponse 响应模型"""
	
	command: Literal["cycle_model"] = "cycle_model"
