from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import MessagesData
from typing		import Literal, Optional
from pydantic	import Field


class GetMessagesResponse(BaseResponse):
	
	"""GetMessagesResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_MESSAGES] = Field(default=CommandEnum.GET_MESSAGES, description="响应指令类型")
	data: Optional[MessagesData]	= Field(default=None, description="get messages 响应数据")

