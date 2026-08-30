from ..base_response	import BaseResponse
from typing		import Literal


class NewSessionResponse(BaseResponse):
	
	"""NewSessionResponse 响应模型"""
	
	command: Literal["new_session"] = "new_session"
