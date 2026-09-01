from .base_command	import BaseCommand
from ..._shared	import ImageContent

from typing		import Literal, Optional, List
from pydantic	import Field


class PromptCommand(BaseCommand):
	
	"""PromptCommand RPC 指令"""
	
	type: Literal["prompt"] = Field(default="prompt", description="指令类型")
	
	message: str	= Field(..., description="用户提示内容")
	images: Optional[List[ImageContent]]	= Field(default=None, description="可选的图片内容列表")
	streamingBehavior: Optional[Literal["steer", "followUp"]]	= Field(default=None, description="流式期间的行为")
