from ..base_response	import BaseResponse
from typing		import Literal


class SetAutoCompactionResponse(BaseResponse):
	
	"""SetAutoCompactionResponse 响应模型"""
	
	command: Literal["set_auto_compaction"] = "set_auto_compaction"
