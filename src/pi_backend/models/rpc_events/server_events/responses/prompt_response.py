from ..base_response	import BaseResponse
from typing		import Literal


class PromptResponse(BaseResponse):
	
	"""PromptResponse 响应模型"""
	
	command: Literal["prompt"] = "prompt"
