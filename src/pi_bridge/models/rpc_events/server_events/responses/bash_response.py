from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import BashData
from typing		import Literal, Optional
from pydantic	import Field


class BashResponse(BaseResponse):
	
	"""BashResponse 响应模型"""
	
	command: Literal[CommandEnum.BASH] = Field(default=CommandEnum.BASH, description="响应指令类型")
	data: Optional[BashData]	= Field(default=None, description="bash 响应数据")

