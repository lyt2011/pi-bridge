from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class AbortResponse(BaseResponse):
	
	"""AbortResponse 响应模型"""
	
	command: Literal[CommandEnum.ABORT] = Field(default=CommandEnum.ABORT, description="响应指令类型")
