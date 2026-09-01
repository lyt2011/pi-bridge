from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class AbortRetryResponse(BaseResponse):
	
	"""AbortRetryResponse 响应模型"""
	
	command: Literal[CommandEnum.ABORT_RETRY] = Field(default=CommandEnum.ABORT_RETRY, description="响应指令类型")
