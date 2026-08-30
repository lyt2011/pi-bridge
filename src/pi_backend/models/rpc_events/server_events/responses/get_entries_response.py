from ..base_response	import BaseResponse


class GetEntriesResponse(BaseResponse):
	
	"""GetEntriesResponse 响应模型"""
	
	command: str = "get_entries"
