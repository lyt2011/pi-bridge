from .base_command	import BaseCommand

from typing		import Literal, Optional, List, Dict, Any
from pydantic	import Field


class PromptCommand(BaseCommand):
	
	"""PromptCommand RPC 指令"""
	
	type: Literal["prompt"] = "prompt"
	
	message: str	= Field(..., description="用户提示内容")
	images: Optional[List[Dict[str, Any]]]	= Field(default=None, description="可选的图片内容列表")
	streamingBehavior: Optional[Literal["steer", "followUp"]]	= Field(default=None, description="流式期间的行为")
