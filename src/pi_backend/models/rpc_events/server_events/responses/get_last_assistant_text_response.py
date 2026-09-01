from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import LastAssistantTextData
from typing		import Literal, Optional
from pydantic	import Field


class GetLastAssistantTextResponse(BaseResponse):
	
	"""GetLastAssistantTextResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_LAST_ASSISTANT_TEXT] = Field(default=CommandEnum.GET_LAST_ASSISTANT_TEXT, description="响应指令类型")
	data: Optional[LastAssistantTextData]	= Field(default=None, description="get last assistant text 响应数据")

