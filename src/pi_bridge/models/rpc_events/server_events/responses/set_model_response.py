from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import Model
from typing		import Literal, Optional
from pydantic	import Field


class SetModelResponse(BaseResponse):
	
	"""SetModelResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_MODEL] = Field(default=CommandEnum.SET_MODEL, description="响应指令类型")
	data: Optional[Model]	= Field(default=None, description="set_model (切换模型) 响应数据")

