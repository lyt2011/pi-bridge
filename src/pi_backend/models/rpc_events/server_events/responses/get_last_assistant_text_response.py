from ..base_response	import BaseResponse


class GetLastAssistantTextResponse(BaseResponse):
	
	"""GetLastAssistantTextResponse 响应模型"""
	
	command: str = "get_last_assistant_text"
