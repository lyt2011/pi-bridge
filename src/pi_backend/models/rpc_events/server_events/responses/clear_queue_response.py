from ..base_response	import BaseResponse
from typing		import Literal


class ClearQueueResponse(BaseResponse):
	
	"""ClearQueueResponse 响应模型"""
	
	command: Literal["clear_queue"] = "clear_queue"
