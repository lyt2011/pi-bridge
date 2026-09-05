from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class SetSteeringModeResponse(BaseResponse):
	
	"""SetSteeringModeResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_STEERING_MODE] = Field(default=CommandEnum.SET_STEERING_MODE, description="响应指令类型")
