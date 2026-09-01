from typing	import Optional

from pydantic	import BaseModel, Field


class Cost(BaseModel):
	
	"""成本统计"""
	
	input		: float	= Field(default=0.0, description="输入成本")
	output		: float	= Field(default=0.0, description="输出成本")
	cacheRead	: float	= Field(default=0.0, description="缓存读取成本")
	cacheWrite	: float	= Field(default=0.0, description="缓存写入成本")
	total		: float	= Field(default=0.0, description="总成本")


class Usage(BaseModel):
	
	"""用量统计"""
	
	input		: int	= Field(default=0, description="输入 token 数")
	output		: int	= Field(default=0, description="输出 token 数")
	cacheRead	: int	= Field(default=0, description="缓存读取 token 数")
	cacheWrite	: int	= Field(default=0, description="缓存写入 token 数")
	totalTokens	: int	= Field(default=0, description="总 token 数")
	cost		: Optional[Cost] = Field(default=None, description="成本统计")