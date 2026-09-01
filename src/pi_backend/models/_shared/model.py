from typing	import List, Optional

from pydantic	import BaseModel, Field


class ModelCost(BaseModel):
	
	"""模型成本"""
	
	input		: float	= Field(default=0.0, description="输入成本")
	output		: float	= Field(default=0.0, description="输出成本")
	cacheRead	: float	= Field(default=0.0, description="缓存读取成本")
	cacheWrite	: float	= Field(default=0.0, description="缓存写入成本")


class Model(BaseModel):
	
	"""模型信息"""
	
	id			: str	= Field(default="", description="模型ID")
	name		: str	= Field(default="", description="模型名称")
	api			: str	= Field(default="", description="API 标识")
	provider	: str	= Field(default="", description="提供商")
	baseUrl		: str	= Field(default="", description="基础地址")
	reasoning	: bool	= Field(default=False, description="是否支持推理")
	input		: List[str]	= Field(default_factory=list, description="支持的输入类型 (text/image)")
	contextWindow	: int	= Field(default=0, description="上下文窗口大小")
	maxTokens	: int	= Field(default=0, description="最大 token 数")
	cost		: Optional[ModelCost] = Field(default=None, description="模型成本")