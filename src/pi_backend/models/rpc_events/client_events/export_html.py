from .base_command	import BaseCommand

from typing		import Literal, Optional
from pydantic	import Field


class ExportHtmlCommand(BaseCommand):
	
	"""ExportHtmlCommand RPC 指令"""
	
	type: Literal["export_html"] = Field(default="export_html", description="指令类型")
	
	outputPath: Optional[str]	= Field(default=None, description="输出文件路径")
