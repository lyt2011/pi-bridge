from ..base_response	import BaseResponse
from typing		import Literal


class GetLastAssistantTextResponse(BaseResponse):
	
	"""GetLastAssistantTextResponse 响应模型"""
	
	command: Literal["get_last_assistant_text"] = "get_last_assistant_text"
