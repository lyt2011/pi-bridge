from ..base_response	import BaseResponse
from typing		import Literal


class SetAutoRetryResponse(BaseResponse):
	
	"""SetAutoRetryResponse 响应模型"""
	
	command: Literal["set_auto_retry"] = "set_auto_retry"
