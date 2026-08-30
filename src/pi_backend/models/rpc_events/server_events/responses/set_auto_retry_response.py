from ..base_response	import BaseResponse


class SetAutoRetryResponse(BaseResponse):
	
	"""SetAutoRetryResponse 响应模型"""
	
	command: str = "set_auto_retry"
