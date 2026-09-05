from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import CancelledData
from typing		import Literal, Optional
from pydantic	import Field


class CloneResponse(BaseResponse):
	
	"""CloneResponse 响应模型"""
	
	command: Literal[CommandEnum.CLONE] = Field(default=CommandEnum.CLONE, description="响应指令类型")
	data: Optional[CancelledData]	= Field(default=None, description="clone 响应数据")

