from ..base_response	import BaseResponse


class SetSessionNameResponse(BaseResponse):
	
	"""SetSessionNameResponse 响应模型"""
	
	command: str = "set_session_name"
