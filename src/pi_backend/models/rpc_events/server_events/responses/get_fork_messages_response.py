from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import ForkMessagesData
from typing		import Literal, Optional
from pydantic	import Field


class GetForkMessagesResponse(BaseResponse):
	
	"""GetForkMessagesResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_FORK_MESSAGES] = Field(default=CommandEnum.GET_FORK_MESSAGES, description="响应指令类型")
	data: Optional[ForkMessagesData]	= Field(default=None, description="get fork messages 响应数据")

