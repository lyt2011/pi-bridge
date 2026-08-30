from ..base_response	import BaseResponse


class SwitchSessionResponse(BaseResponse):
	
	"""SwitchSessionResponse 响应模型"""
	
	command: str = "switch_session"
