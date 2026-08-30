from ..base_response	import BaseResponse
from typing		import Literal


class AbortRetryResponse(BaseResponse):
	
	"""AbortRetryResponse 响应模型"""
	
	command: Literal["abort_retry"] = "abort_retry"
