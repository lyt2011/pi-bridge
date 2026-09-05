from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal
from pydantic	import Field


class NewSessionResponse(BaseResponse):
	
	"""NewSessionResponse 响应模型"""
	
	command: Literal[CommandEnum.NEW_SESSION] = Field(default=CommandEnum.NEW_SESSION, description="响应指令类型")
