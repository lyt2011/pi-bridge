from ..base_response	import BaseResponse
from typing		import Literal


class AbortResponse(BaseResponse):
	
	"""AbortResponse 响应模型"""
	
	command: Literal["abort"] = "abort"
