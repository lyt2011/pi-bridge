from ..base_response	import BaseResponse


class CloneResponse(BaseResponse):
	
	"""CloneResponse 响应模型"""
	
	command: str = "clone"
