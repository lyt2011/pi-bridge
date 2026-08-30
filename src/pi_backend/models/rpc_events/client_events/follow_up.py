from .base_command	import BaseCommand

from typing		import Literal, Optional, List, Dict, Any
from pydantic	import Field


class FollowUpCommand(BaseCommand):
	
	"""FollowUpCommand RPC 指令"""
	
	type: Literal["follow_up"] = "follow_up"
	
	message: str	= Field(..., description="follow-up消息内容")
	images: Optional[List[Dict[str, Any]]]	= Field(default=None, description="可选的图片内容列表")
