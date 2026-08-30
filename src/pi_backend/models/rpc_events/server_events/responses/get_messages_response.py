from ..base_response	import BaseResponse


class GetMessagesResponse(BaseResponse):
	
	"""GetMessagesResponse 响应模型"""
	
	command: str = "get_messages"
