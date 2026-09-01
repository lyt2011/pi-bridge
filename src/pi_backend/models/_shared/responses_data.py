from typing	import List, Optional

from pydantic	import BaseModel, Field

from .model				import Model
from .agent_message		import AgentMessage
from .session_entry		import SessionEntry, TreeEntry
from .compaction_result	import CompactionResult


class StateData(BaseModel):
	
	"""get_state 响应 data"""
	
	model				: Optional[Model] = Field(default=None, description="当前模型")
	thinkingLevel		: str	= Field(default="", description="思考级别")
	isStreaming			: bool	= Field(default=False, description="是否正在流式输出")
	isCompacting		: bool	= Field(default=False, description="是否正在压缩")
	steeringMode		: str	= Field(default="", description="引导模式")
	followUpMode		: str	= Field(default="", description="追问模式")
	sessionFile			: Optional[str] = Field(default=None, description="会话文件路径")
	sessionId			: Optional[str] = Field(default=None, description="会话ID")
	sessionName			: Optional[str] = Field(default=None, description="会话名称")
	autoCompactionEnabled	: bool	= Field(default=False, description="是否启用自动压缩")
	messageCount		: int	= Field(default=0, description="消息数")
	pendingMessageCount	: int	= Field(default=0, description="待处理消息数")


class BashData(BaseModel):
	
	"""bash 响应 data"""
	
	output			: str	= Field(default="", description="命令输出")
	exitCode		: int	= Field(default=0, description="退出码")
	cancelled		: bool	= Field(default=False, description="是否被取消")
	truncated		: bool	= Field(default=False, description="输出是否被截断")
	fullOutputPath	: Optional[str] = Field(default=None, description="完整输出文件路径")


class ModelsData(BaseModel):
	
	"""get_available_models 响应 data"""
	
	models	: List[Model] = Field(default_factory=list, description="可用模型列表")


class LevelsData(BaseModel):
	
	"""get_available_thinking_levels 响应 data"""
	
	levels	: List[str] = Field(default_factory=list, description="可用思考级别列表")


class ForkMessage(BaseModel):
	
	"""get_fork_messages 中的单条消息"""
	
	entryId	: str	= Field(default="", description="条目ID")
	text	: str	= Field(default="", description="消息文本")


class ForkMessagesData(BaseModel):
	
	"""get_fork_messages 响应 data"""
	
	messages	: List[ForkMessage] = Field(default_factory=list, description="分叉消息列表")


class EntriesData(BaseModel):
	
	"""get_entries 响应 data"""
	
	entries	: List[SessionEntry] = Field(default_factory=list, description="会话条目列表")
	leafId	: Optional[str] = Field(default=None, description="叶子节点ID")


class TreeData(BaseModel):
	
	"""get_tree 响应 data"""
	
	tree	: List[TreeEntry] = Field(default_factory=list, description="会话树节点列表")
	leafId	: Optional[str] = Field(default=None, description="叶子节点ID")


class LastAssistantTextData(BaseModel):
	
	"""get_last_assistant_text 响应 data"""
	
	text	: Optional[str] = Field(default=None, description="最后一条助手文本")


class ExportHtmlData(BaseModel):
	
	"""export_html 响应 data"""
	
	path	: str	= Field(default="", description="导出文件路径")


class CancelledData(BaseModel):
	
	"""switch_session / clone 等响应 data"""
	
	cancelled	: bool	= Field(default=False, description="是否已取消")


class ForkData(BaseModel):
	
	"""fork 响应 data"""
	
	text		: str	= Field(default="", description="分支消息文本")
	cancelled	: bool	= Field(default=False, description="是否已取消")


class CommandInfo(BaseModel):
	
	"""get_commands 中的单条指令信息"""
	
	name		: str	= Field(default="", description="指令名称")
	description	: Optional[str] = Field(default=None, description="指令描述")
	source		: str	= Field(default="", description="指令来源")
	location	: Optional[str] = Field(default=None, description="指令位置")
	path		: Optional[str] = Field(default=None, description="指令路径")


class CommandsData(BaseModel):
	
	"""get_commands 响应 data"""
	
	commands	: List[CommandInfo] = Field(default_factory=list, description="指令列表")


class MessagesData(BaseModel):
	
	"""get_messages 响应 data"""
	
	messages	: List[AgentMessage] = Field(default_factory=list, description="消息列表")


class CycleModelData(BaseModel):
	
	"""cycle_model 响应 data"""
	
	model			: Optional[Model] = Field(default=None, description="当前模型")
	thinkingLevel	: str	= Field(default="", description="思考级别")
	isScoped			: bool	= Field(default=False, description="是否限定范围")