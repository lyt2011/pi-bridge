from ..base_response	import BaseResponse
from typing		import Literal


class SetThinkingLevelResponse(BaseResponse):
	
	"""SetThinkingLevelResponse 响应模型"""
	
	command: Literal["set_thinking_level"] = "set_thinking_level"
