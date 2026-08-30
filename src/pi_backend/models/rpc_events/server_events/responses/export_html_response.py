from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from typing		import Literal


class ExportHtmlResponse(BaseResponse):
	
	"""ExportHtmlResponse 响应模型"""
	
	command: Literal[CommandEnum.EXPORT_HTML] = CommandEnum.EXPORT_HTML
