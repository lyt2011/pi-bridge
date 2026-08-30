from ..base_response	import BaseResponse


class BashResponse(BaseResponse):
	
	"""BashResponse 响应模型"""
	
	command: str = "bash"
