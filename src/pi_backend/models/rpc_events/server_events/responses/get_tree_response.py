from ..base_response	import BaseResponse


class GetTreeResponse(BaseResponse):
	
	"""GetTreeResponse 响应模型"""
	
	command: str = "get_tree"
