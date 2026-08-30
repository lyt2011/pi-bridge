from ..base_response	import BaseResponse


class StateResponse(BaseResponse):
	
	"""StateResponse 响应模型"""
	
	command: str = "get_state"
