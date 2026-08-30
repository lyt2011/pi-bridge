from ..base_response	import BaseResponse


class ForkResponse(BaseResponse):
	
	"""ForkResponse 响应模型"""
	
	command: str = "fork"
