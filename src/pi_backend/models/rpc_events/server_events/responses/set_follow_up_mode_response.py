from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class SetFollowUpModeResponse(BaseResponse):
	
	"""SetFollowUpModeResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_FOLLOW_UP_MODE] = Field(default=CommandEnum.SET_FOLLOW_UP_MODE, description="响应指令类型")
