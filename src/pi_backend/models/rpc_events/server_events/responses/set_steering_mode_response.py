from ..base_response	import BaseResponse
from typing		import Literal


class SetSteeringModeResponse(BaseResponse):
	
	"""SetSteeringModeResponse 响应模型"""
	
	command: Literal["set_steering_mode"] = "set_steering_mode"
