from ..base_response	import BaseResponse
from typing		import Literal


class SetSessionNameResponse(BaseResponse):
	
	"""SetSessionNameResponse 响应模型"""
	
	command: Literal["set_session_name"] = "set_session_name"
