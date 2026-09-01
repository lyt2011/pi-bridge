from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class CycleThinkingLevelResponse(BaseResponse):
	
	"""CycleThinkingLevelResponse 响应模型"""
	
	command: Literal[CommandEnum.CYCLE_THINKING_LEVEL] = Field(default=CommandEnum.CYCLE_THINKING_LEVEL, description="响应指令类型")
