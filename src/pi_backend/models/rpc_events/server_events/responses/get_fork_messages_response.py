from ..base_response	import BaseResponse
from typing		import Literal


class GetForkMessagesResponse(BaseResponse):
	
	"""GetForkMessagesResponse 响应模型"""
	
	command: Literal["get_fork_messages"] = "get_fork_messages"
