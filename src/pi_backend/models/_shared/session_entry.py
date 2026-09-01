from typing	import List, Optional

from pydantic	import BaseModel, ConfigDict, Field

from .agent_message	import AgentMessage


class SessionEntry(BaseModel):
	
	"""会话条目 (get_entries 的元素)"""
	
	model_config = ConfigDict(extra="allow")
	
	type			: str	= Field(default="", description="条目类型")
	id				: str	= Field(default="", description="条目ID")
	parentId		: Optional[str] = Field(default=None, description="父条目ID")
	timestamp		: str	= Field(default="", description="时间戳")
	message			: Optional[AgentMessage] = Field(default=None, description="关联消息")
	summary			: Optional[str] = Field(default=None, description="摘要")
	tokensBefore	: Optional[int] = Field(default=None, description="压缩前 token 数")


class TreeEntry(BaseModel):
	
	"""会话树节点 (get_tree 的节点)"""
	
	entry			: Optional[SessionEntry] = Field(default=None, description="会话条目")
	children		: List[TreeEntry] = Field(default_factory=list, description="子节点列表")
	label			: Optional[str] = Field(default=None, description="节点标签")
	labelTimestamp	: Optional[str] = Field(default=None, description="标签时间戳")