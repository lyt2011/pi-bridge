from ..base_response	import BaseResponse
from typing		import Literal


class GetEntriesResponse(BaseResponse):
	
	"""GetEntriesResponse 响应模型"""
	
	command: Literal["get_entries"] = "get_entries"
