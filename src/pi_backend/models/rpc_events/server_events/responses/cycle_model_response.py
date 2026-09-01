from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import CycleModelData
from typing		import Literal, Optional
from pydantic	import Field


class CycleModelResponse(BaseResponse):
	
	"""CycleModelResponse 响应模型"""
	
	command: Literal[CommandEnum.CYCLE_MODEL] = Field(default=CommandEnum.CYCLE_MODEL, description="响应指令类型")
	data: Optional[CycleModelData]	= Field(default=None, description="cycle model 响应数据")

