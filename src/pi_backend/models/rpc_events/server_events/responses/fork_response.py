from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import ForkData
from typing		import Literal, Optional
from pydantic	import Field


class ForkResponse(BaseResponse):
	
	"""ForkResponse 响应模型"""
	
	command: Literal[CommandEnum.FORK] = Field(default=CommandEnum.FORK, description="响应指令类型")
	data: Optional[ForkData]	= Field(default=None, description="fork 响应数据")

