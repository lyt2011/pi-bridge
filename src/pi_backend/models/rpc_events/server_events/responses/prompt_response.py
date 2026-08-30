from ..base_response	import BaseResponse


class PromptResponse(BaseResponse):
	
	"""PromptResponse 响应模型"""
	
	command: str = "prompt"
