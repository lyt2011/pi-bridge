from ..base_response	import BaseResponse
from typing		import Literal


class CloneResponse(BaseResponse):
	
	"""CloneResponse 响应模型"""
	
	command: Literal["clone"] = "clone"
