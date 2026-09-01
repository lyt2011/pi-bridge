from .base_command	import BaseCommand
from ..._shared	import ImageContent

from typing		import Literal, Optional, List
from pydantic	import Field


class FollowUpCommand(BaseCommand):
	
	"""FollowUpCommand RPC 指令"""
	
	type: Literal["follow_up"] = Field(default="follow_up", description="指令类型")
	
	message: str	= Field(..., description="follow-up消息内容")
	images: Optional[List[ImageContent]]	= Field(default=None, description="可选的图片内容列表")
