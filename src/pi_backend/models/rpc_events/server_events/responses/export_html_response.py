from ..base_response	import BaseResponse
from typing		import Literal


class ExportHtmlResponse(BaseResponse):
	
	"""ExportHtmlResponse 响应模型"""
	
	command: Literal["export_html"] = "export_html"
