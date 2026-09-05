from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class AbortBashResponse(BaseResponse):
	
	"""AbortBashResponse 响应模型"""
	
	command: Literal[CommandEnum.ABORT_BASH] = Field(default=CommandEnum.ABORT_BASH, description="响应指令类型")
