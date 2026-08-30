from ..base_response	import BaseResponse
from typing		import Literal


class AbortBashResponse(BaseResponse):
	
	"""AbortBashResponse 响应模型"""
	
	command: Literal["abort_bash"] = "abort_bash"
