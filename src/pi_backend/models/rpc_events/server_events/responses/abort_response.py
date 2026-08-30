from ..base_response	import BaseResponse


class AbortResponse(BaseResponse):
	
	"""AbortResponse 响应模型"""
	
	command: str = "abort"
