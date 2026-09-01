from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class FollowUpResponse(BaseResponse):
	
	"""FollowUpResponse 响应模型"""
	
	command: Literal[CommandEnum.FOLLOW_UP] = Field(default=CommandEnum.FOLLOW_UP, description="响应指令类型")
