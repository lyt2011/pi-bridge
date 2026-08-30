from ..base_response	import BaseResponse
from typing		import Literal


class SteerResponse(BaseResponse):
	
	"""SteerResponse 响应模型"""
	
	command: Literal["steer"] = "steer"
