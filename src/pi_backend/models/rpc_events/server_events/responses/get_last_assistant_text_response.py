from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class GetLastAssistantTextResponse(BaseResponse):
	
	"""GetLastAssistantTextResponse 响应模型"""
	
	command: Literal[CommandEnum.GET_LAST_ASSISTANT_TEXT] = CommandEnum.GET_LAST_ASSISTANT_TEXT
