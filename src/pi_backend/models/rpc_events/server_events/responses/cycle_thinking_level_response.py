from ..base_response	import BaseResponse
from typing		import Literal


class CycleThinkingLevelResponse(BaseResponse):
	
	"""CycleThinkingLevelResponse 响应模型"""
	
	command: Literal["cycle_thinking_level"] = "cycle_thinking_level"
