from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import CommandsData
from typing		import Literal, Optional
from pydantic	import Field


class GetCommandsResponse(BaseResponse):
	
	"""GetCommandsResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_COMMANDS] = Field(default=CommandEnum.GET_COMMANDS, description="响应指令类型")
	data: Optional[CommandsData]	= Field(default=None, description="get commands 响应数据")

