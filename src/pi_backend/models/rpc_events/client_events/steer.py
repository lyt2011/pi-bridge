from .base_command	import BaseCommand

from typing		import Literal, Optional, List, Dict, Any
from pydantic	import Field


class SteerCommand(BaseCommand):
	
	"""SteerCommand RPC 指令"""
	
	type: Literal["steer"] = "steer"
	
	message: str	= Field(..., description="steering消息内容")
	images: Optional[List[Dict[str, Any]]]	= Field(default=None, description="可选的图片内容列表")
