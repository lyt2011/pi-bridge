from ..base_response	import BaseResponse
from typing		import Literal


class SetFollowUpModeResponse(BaseResponse):
	
	"""SetFollowUpModeResponse 响应模型"""
	
	command: Literal["set_follow_up_mode"] = "set_follow_up_mode"
