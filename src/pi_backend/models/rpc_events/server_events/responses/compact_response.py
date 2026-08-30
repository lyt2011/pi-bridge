from ..base_response	import BaseResponse
from typing		import Literal


class CompactResponse(BaseResponse):
	
	"""CompactResponse 响应模型"""
	
	command: Literal["compact"] = "compact"
