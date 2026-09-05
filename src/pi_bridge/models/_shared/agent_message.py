from typing	import Any, Dict, List, Literal, Optional, Union, Annotated

from pydantic	import BaseModel, Field

from .usage			import Usage
from .content_block	import ContentBlock


class UserMessage(BaseModel):
	
	"""用户消息"""
	
	role		: Literal["user"]	= Field(default="user", description="消息角色")
	content		: Union[str, List[ContentBlock]]	= Field(default="", description="消息内容")
	timestamp	: int	= Field(default=0, description="消息时间戳")
	attachments	: Optional[List[Dict[str, Any]]] = Field(default=None, description="附件列表")


class AssistantMessage(BaseModel):
	
	"""助手消息"""
	
	role		: Literal["assistant"]	= Field(default="assistant", description="消息角色")
	content		: List[ContentBlock] = Field(default_factory=list, description="消息内容块")
	api			: str	= Field(default="", description="API 标识")
	provider	: str	= Field(default="", description="提供商")
	model		: str	= Field(default="", description="模型名")
	usage		: Optional[Usage] = Field(default=None, description="用量统计")
	stopReason	: Optional[Literal["stop", "length", "toolUse", "error", "aborted", "pending"]] = Field(default=None, description="停止原因")
	errorMessage: Optional[str] = Field(default=None, description="错误信息")
	timestamp	: int	= Field(default=0, description="消息时间戳")


class ToolResultMessage(BaseModel):
	
	"""工具结果消息"""
	
	role		: Literal["toolResult"]	= Field(default="toolResult", description="消息角色")
	toolCallId	: str	= Field(default="", description="工具调用ID")
	toolName	: str	= Field(default="", description="工具名称")
	content		: List[ContentBlock] = Field(default_factory=list, description="消息内容块")
	details		: Optional[Dict[str, Any]] = Field(default=None, description="工具结果详情")
	usage		: Optional[Usage] = Field(default=None, description="用量统计")
	isError		: bool	= Field(default=False, description="是否错误")
	timestamp	: int	= Field(default=0, description="消息时间戳")


class BashExecutionMessage(BaseModel):
	
	"""Bash 执行消息"""
	
	role			: Literal["bashExecution"]	= Field(default="bashExecution", description="消息角色")
	command			: str	= Field(default="", description="执行的命令")
	output			: str	= Field(default="", description="命令输出")
	exitCode		: Optional[int] = Field(default=None, description="退出码")
	cancelled		: bool	= Field(default=False, description="是否被取消")
	truncated		: bool	= Field(default=False, description="输出是否被截断")
	fullOutputPath	: Optional[str] = Field(default=None, description="完整输出文件路径")
	excludeFromContext	: Optional[bool] = Field(default=None, description="是否从上下文排除")
	timestamp		: int	= Field(default=0, description="消息时间戳")


class CustomMessage(BaseModel):
	
	"""自定义消息"""
	
	role		: Literal["custom"]	= Field(default="custom", description="消息角色")
	customType	: str	= Field(default="", description="自定义类型")
	content		: Union[str, List[ContentBlock]]	= Field(default="", description="消息内容")
	display		: bool	= Field(default=False, description="是否展示")
	details		: Optional[Dict[str, Any]] = Field(default=None, description="附加详情")
	timestamp	: int	= Field(default=0, description="消息时间戳")


class BranchSummaryMessage(BaseModel):
	
	"""分支摘要消息"""
	
	role		: Literal["branchSummary"]	= Field(default="branchSummary", description="消息角色")
	summary		: str	= Field(default="", description="分支摘要")
	fromId		: str	= Field(default="", description="来源条目ID")
	timestamp	: int	= Field(default=0, description="消息时间戳")


class CompactionSummaryMessage(BaseModel):
	
	"""压缩摘要消息"""
	
	role			: Literal["compactionSummary"]	= Field(default="compactionSummary", description="消息角色")
	summary			: str	= Field(default="", description="压缩摘要")
	tokensBefore	: int	= Field(default=0, description="压缩前 token 数")
	timestamp		: int	= Field(default=0, description="消息时间戳")


AgentMessage = Annotated[
	Union[
		UserMessage,
		AssistantMessage,
		ToolResultMessage,
		BashExecutionMessage,
		CustomMessage,
		BranchSummaryMessage,
		CompactionSummaryMessage,
	],
	Field(discriminator="role")
]