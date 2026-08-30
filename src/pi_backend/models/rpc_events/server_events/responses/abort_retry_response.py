from ..base_response	import BaseResponse


class AbortRetryResponse(BaseResponse):
	
	"""AbortRetryResponse 响应模型"""
	
	command: str = "abort_retry"
