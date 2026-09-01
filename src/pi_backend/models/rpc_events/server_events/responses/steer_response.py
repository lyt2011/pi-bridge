from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class SteerResponse(BaseResponse):
	
	"""SteerResponse 响应模型"""
	
	command: Literal[CommandEnum.STEER] = Field(default=CommandEnum.STEER, description="响应指令类型")
