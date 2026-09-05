from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class SetAutoRetryResponse(BaseResponse):
	
	"""SetAutoRetryResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_AUTO_RETRY] = Field(default=CommandEnum.SET_AUTO_RETRY, description="响应指令类型")
