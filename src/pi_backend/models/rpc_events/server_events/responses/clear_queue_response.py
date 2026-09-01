from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class ClearQueueResponse(BaseResponse):
	
	"""ClearQueueResponse 响应模型"""
	
	command: Literal[CommandEnum.CLEAR_QUEUE] = Field(default=CommandEnum.CLEAR_QUEUE, description="响应指令类型")
