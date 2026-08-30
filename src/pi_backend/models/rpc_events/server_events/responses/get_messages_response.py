from ..base_response	import BaseResponse
from typing		import Literal


class GetMessagesResponse(BaseResponse):
	
	"""GetMessagesResponse 响应模型"""
	
	command: Literal["get_messages"] = "get_messages"
