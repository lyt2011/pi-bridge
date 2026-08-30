from ..base_response	import BaseResponse


class SteerResponse(BaseResponse):
	
	"""SteerResponse 响应模型"""
	
	command: str = "steer"
