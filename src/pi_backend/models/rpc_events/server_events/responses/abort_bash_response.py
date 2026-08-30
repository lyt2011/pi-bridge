from ..base_response	import BaseResponse


class AbortBashResponse(BaseResponse):
	
	"""AbortBashResponse 响应模型"""
	
	command: str = "abort_bash"
