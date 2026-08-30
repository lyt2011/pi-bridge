from ..base_response	import BaseResponse


class SetSteeringModeResponse(BaseResponse):
	
	"""SetSteeringModeResponse 响应模型"""
	
	command: str = "set_steering_mode"
