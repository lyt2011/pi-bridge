from ..base_response	import BaseResponse
from typing		import Literal


class ForkResponse(BaseResponse):
	
	"""ForkResponse 响应模型"""
	
	command: Literal["fork"] = "fork"
