from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import TreeData
from typing		import Literal, Optional
from pydantic	import Field


class GetTreeResponse(BaseResponse):
	
	"""GetTreeResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_TREE] = Field(default=CommandEnum.GET_TREE, description="响应指令类型")
	data: Optional[TreeData]	= Field(default=None, description="get tree 响应数据")

