from typing	import Any, Dict, Optional

from pydantic	import BaseModel, Field

from .usage	import Usage


class CompactionResult(BaseModel):
	
	"""压缩结果"""
	
	summary				: str	= Field(default="", description="压缩摘要")
	firstKeptEntryId	: Optional[str] = Field(default=None, description="保留的第一条条目ID")
	tokensBefore		: int	= Field(default=0, description="压缩前 token 数")
	estimatedTokensAfter	: int	= Field(default=0, description="估算压缩后 token 数")
	usage				: Optional[Usage] = Field(default=None, description="压缩用量")
	details				: Optional[Dict[str, Any]] = Field(default=None, description="附加详情")