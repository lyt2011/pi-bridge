from ..base_response	import BaseResponse


class ExportHtmlResponse(BaseResponse):
	
	"""ExportHtmlResponse 响应模型"""
	
	command: str = "export_html"
