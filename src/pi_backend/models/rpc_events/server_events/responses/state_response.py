from ..base_response	import BaseResponse
from typing		import Literal


class StateResponse(BaseResponse):
	
	"""StateResponse 响应模型"""
	
	command: Literal["get_state"] = "get_state"
