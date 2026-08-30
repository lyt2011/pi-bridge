from ..base_response	import BaseResponse


class FollowUpResponse(BaseResponse):
	
	"""FollowUpResponse 响应模型"""
	
	command: str = "follow_up"
