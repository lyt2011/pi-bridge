from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import EntriesData
from typing		import Literal, Optional
from pydantic	import Field


class GetEntriesResponse(BaseResponse):
	
	"""GetEntriesResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_ENTRIES] = Field(default=CommandEnum.GET_ENTRIES, description="响应指令类型")
	data: Optional[EntriesData]	= Field(default=None, description="get entries 响应数据")

