from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class FollowUpResponse(BaseResponse):
	
	"""FollowUpResponse 响应模型"""
	
	command: Literal[CommandEnum.FOLLOW_UP] = CommandEnum.FOLLOW_UP
