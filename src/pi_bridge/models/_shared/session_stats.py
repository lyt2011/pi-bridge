from typing	import Optional

from pydantic	import BaseModel, Field


class SessionStatsTokens(BaseModel):
	
	"""会话统计 token 分布"""
	
	input		: int	= Field(default=0, description="输入 token 数")
	output		: int	= Field(default=0, description="输出 token 数")
	cacheRead	: int	= Field(default=0, description="缓存读取 token 数")
	cacheWrite	: int	= Field(default=0, description="缓存写入 token 数")
	total		: int	= Field(default=0, description="总 token 数")


class SessionStatsContextUsage(BaseModel):
	
	"""会话上下文占用"""
	
	tokens			: Optional[int] = Field(default=None, description="token 数")
	contextWindow	: Optional[int] = Field(default=None, description="上下文窗口大小")
	percent			: Optional[float] = Field(default=None, description="占用百分比")


class SessionStatsData(BaseModel):
	
	"""会话统计响应 data"""
	
	sessionFile			: str	= Field(default="", description="会话文件路径")
	sessionId			: str	= Field(default="", description="会话ID")
	userMessages		: int	= Field(default=0, description="用户消息数")
	assistantMessages	: int	= Field(default=0, description="助手消息数")
	toolCalls			: int	= Field(default=0, description="工具调用数")
	toolResults			: int	= Field(default=0, description="工具结果数")
	totalMessages		: int	= Field(default=0, description="总消息数")
	tokens				: Optional[SessionStatsTokens] = Field(default=None, description="token 统计")
	cost				: float	= Field(default=0.0, description="总成本")
	contextUsage		: Optional[SessionStatsContextUsage] = Field(default=None, description="上下文占用")