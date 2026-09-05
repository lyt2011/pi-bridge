from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import CompactionResult
from typing		import Literal, Optional
from pydantic	import Field


class CompactResponse(BaseResponse):
	
	"""CompactResponse 响应模型"""
	
	command: Literal[CommandEnum.COMPACT] = Field(default=CommandEnum.COMPACT, description="响应指令类型")
	data: Optional[CompactionResult]	= Field(default=None, description="compact (压缩) 响应数据")

