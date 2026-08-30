from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class CycleModelResponse(BaseResponse):
	
	"""CycleModelResponse 响应模型"""
	
	command: Literal[CommandEnum.CYCLE_MODEL] = CommandEnum.CYCLE_MODEL
