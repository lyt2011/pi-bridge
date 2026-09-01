from .base_command	import BaseCommand
from ..._shared	import ImageContent

from typing		import Literal, Optional, List
from pydantic	import Field


class SteerCommand(BaseCommand):
	
	"""SteerCommand RPC 指令"""
	
	type: Literal["steer"] = Field(default="steer", description="指令类型")
	
	message: str	= Field(..., description="steering消息内容")
	images: Optional[List[ImageContent]]	= Field(default=None, description="可选的图片内容列表")
