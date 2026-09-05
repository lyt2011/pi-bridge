from ..base_response	import BaseResponse
from .....enums	import CommandEnum
from ...._shared	import ExportHtmlData
from typing		import Literal, Optional
from pydantic	import Field


class ExportHtmlResponse(BaseResponse):
	
	"""ExportHtmlResponse 响应模型"""
	
	command: Literal[CommandEnum.EXPORT_HTML] = Field(default=CommandEnum.EXPORT_HTML, description="响应指令类型")
	data: Optional[ExportHtmlData]	= Field(default=None, description="export html 响应数据")

