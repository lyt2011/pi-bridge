from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class PromptResponse(BaseResponse):
	
	"""PromptResponse 响应模型"""
	
	command: Literal[CommandEnum.PROMPT] = CommandEnum.PROMPT
