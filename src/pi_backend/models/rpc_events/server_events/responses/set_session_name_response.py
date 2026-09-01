from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class SetSessionNameResponse(BaseResponse):
	
	"""SetSessionNameResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_SESSION_NAME] = Field(default=CommandEnum.SET_SESSION_NAME, description="响应指令类型")
