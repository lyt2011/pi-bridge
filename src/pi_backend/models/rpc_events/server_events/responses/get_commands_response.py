from ..base_response	import BaseResponse
from typing		import Literal


class GetCommandsResponse(BaseResponse):
	
	"""GetCommandsResponse 响应模型"""
	
	command: Literal["get_commands"] = "get_commands"
