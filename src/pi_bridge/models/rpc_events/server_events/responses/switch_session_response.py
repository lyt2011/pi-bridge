from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import CancelledData
from typing		import Literal, Optional
from pydantic	import Field


class SwitchSessionResponse(BaseResponse):
	
	"""SwitchSessionResponse 响应模型"""
	
	command: Literal[CommandEnum.SWITCH_SESSION] = Field(default=CommandEnum.SWITCH_SESSION, description="响应指令类型")
	data: Optional[CancelledData]	= Field(default=None, description="switch session 响应数据")

