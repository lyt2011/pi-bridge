from ..base_response	import BaseResponse


class SetAutoCompactionResponse(BaseResponse):
	
	"""SetAutoCompactionResponse 响应模型"""
	
	command: str = "set_auto_compaction"
