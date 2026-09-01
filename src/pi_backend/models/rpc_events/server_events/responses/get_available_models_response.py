from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import ModelsData
from typing		import Literal, Optional
from pydantic	import Field


class GetAvailableModelsResponse(BaseResponse):
	
	"""GetAvailableModelsResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_AVAILABLE_MODELS] = Field(default=CommandEnum.GET_AVAILABLE_MODELS, description="响应指令类型")
	data: Optional[ModelsData]	= Field(default=None, description="get available models 响应数据")

