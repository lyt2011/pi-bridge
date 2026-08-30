from ..base_response	import BaseResponse
from typing		import Literal


class GetAvailableThinkingLevelsResponse(BaseResponse):
	
	"""GetAvailableThinkingLevelsResponse 响应模型"""
	
	command: Literal["get_available_thinking_levels"] = "get_available_thinking_levels"
