from ..base_response	import BaseResponse


class ClearQueueResponse(BaseResponse):
	
	"""ClearQueueResponse 响应模型"""
	
	command: str = "clear_queue"
