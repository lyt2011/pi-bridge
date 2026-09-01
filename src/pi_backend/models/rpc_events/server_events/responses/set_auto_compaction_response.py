from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class SetAutoCompactionResponse(BaseResponse):
	
	"""SetAutoCompactionResponse 响应模型"""
	
	command: Literal[CommandEnum.SET_AUTO_COMPACTION] = Field(default=CommandEnum.SET_AUTO_COMPACTION, description="响应指令类型")
