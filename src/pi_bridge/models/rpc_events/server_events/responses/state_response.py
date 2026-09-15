from ..base_response	import BaseResponse
from .....enums			import CommandEnum
from ...._shared		import StateData

from typing		import Literal, Optional
from pydantic	import Field


class StateResponse(BaseResponse):
	
	"""StateResponse 响应模型"""
	
	command	: Literal[CommandEnum.GET_STATE]	= Field(default=CommandEnum.GET_STATE, description="响应指令类型")
	data	: Optional[StateData]				= Field(default=None, description="state 响应数据")

