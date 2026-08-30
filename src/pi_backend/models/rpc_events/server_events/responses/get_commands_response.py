from ..base_response	import BaseResponse


class GetCommandsResponse(BaseResponse):
	
	"""GetCommandsResponse 响应模型"""
	
	command: str = "get_commands"
