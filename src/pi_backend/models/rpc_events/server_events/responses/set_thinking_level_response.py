from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class SetThinkingLevelResponse(BaseResponse):
	
	"""SetThinkingLevelResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_THINKING_LEVEL] = Field(default=CommandEnum.SET_THINKING_LEVEL, description="响应指令类型")
