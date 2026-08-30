from ..base_response	import BaseResponse
from typing		import Literal


class BashResponse(BaseResponse):
	
	"""BashResponse 响应模型"""
	
	command: Literal["bash"] = "bash"
