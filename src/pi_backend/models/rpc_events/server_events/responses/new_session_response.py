from ..base_response	import BaseResponse


class NewSessionResponse(BaseResponse):
	
	"""NewSessionResponse 响应模型"""
	
	command: str = "new_session"
