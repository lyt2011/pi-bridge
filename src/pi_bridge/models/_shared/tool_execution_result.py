from typing	import Any, Dict, List, Optional

from pydantic	import BaseModel, Field

from .content_block	import ContentBlock


class ToolExecutionResult(BaseModel):
	
	"""工具执行结果"""
	
	content	: List[ContentBlock] = Field(default_factory=list, description="结果内容块")
	details	: Optional[Dict[str, Any]] = Field(default=None, description="工具特定元数据")