from ..base_response	import BaseResponse
from typing		import Literal


class SwitchSessionResponse(BaseResponse):
	
	"""SwitchSessionResponse 响应模型"""
	
	command: Literal["switch_session"] = "switch_session"
