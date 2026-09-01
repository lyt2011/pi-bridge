from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class PromptResponse(BaseResponse):
	
	"""PromptResponse 响应模型"""
	
	command: Literal[CommandEnum.PROMPT] = Field(default=CommandEnum.PROMPT, description="响应指令类型")
