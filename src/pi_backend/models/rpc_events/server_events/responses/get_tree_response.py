from ..base_response	import BaseResponse
from typing		import Literal


class GetTreeResponse(BaseResponse):
	
	"""GetTreeResponse 响应模型"""
	
	command: Literal["get_tree"] = "get_tree"
