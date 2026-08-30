from ..base_response	import BaseResponse
from typing		import Literal


class FollowUpResponse(BaseResponse):
	
	"""FollowUpResponse 响应模型"""
	
	command: Literal["follow_up"] = "follow_up"
