from typing	import Literal, Union, Annotated

from pydantic	import BaseModel, Field

from .content_block	import ToolCall


class TextStartEvent(BaseModel):
	
	"""文本开始增量事件"""
	
	type			: Literal["text_start"]	= Field(default="text_start", description="事件类型")
	contentIndex	: int	= Field(default=0, description="内容块索引")


class TextDeltaEvent(BaseModel):
	
	"""文本增量事件"""
	
	type			: Literal["text_delta"]	= Field(default="text_delta", description="事件类型")
	contentIndex	: int	= Field(default=0, description="内容块索引")
	delta			: str	= Field(default="", description="增量文本")


class TextEndEvent(BaseModel):
	
	"""文本结束增量事件"""
	
	type			: Literal["text_end"]	= Field(default="text_end", description="事件类型")
	contentIndex	: int	= Field(default=0, description="内容块索引")
	content			: str	= Field(default="", description="完整文本")


class ThinkingStartEvent(BaseModel):
	
	"""思考开始增量事件"""
	
	type			: Literal["thinking_start"]	= Field(default="thinking_start", description="事件类型")
	contentIndex	: int	= Field(default=0, description="内容块索引")


class ThinkingDeltaEvent(BaseModel):
	
	"""思考增量事件"""
	
	type			: Literal["thinking_delta"]	= Field(default="thinking_delta", description="事件类型")
	contentIndex	: int	= Field(default=0, description="内容块索引")
	delta			: str	= Field(default="", description="增量思考内容")


class ThinkingEndEvent(BaseModel):
	
	"""思考结束增量事件"""
	
	type			: Literal["thinking_end"]	= Field(default="thinking_end", description="事件类型")
	contentIndex	: int	= Field(default=0, description="内容块索引")
	thinking		: str	= Field(default="", description="思考内容")


class ToolcallStartEvent(BaseModel):
	
	"""工具调用开始增量事件"""
	
	type			: Literal["toolcall_start"]	= Field(default="toolcall_start", description="事件类型")
	contentIndex	: int	= Field(default=0, description="内容块索引")
	id				: str	= Field(default="", description="工具调用ID")
	toolName		: str	= Field(default="", description="工具名称")


class ToolcallDeltaEvent(BaseModel):
	
	"""工具调用增量事件"""
	
	type			: Literal["toolcall_delta"]	= Field(default="toolcall_delta", description="事件类型")
	contentIndex	: int	= Field(default=0, description="内容块索引")
	delta			: str	= Field(default="", description="增量数据")


class ToolcallEndEvent(BaseModel):
	
	"""工具调用结束增量事件"""
	
	type			: Literal["toolcall_end"]	= Field(default="toolcall_end", description="事件类型")
	contentIndex	: int	= Field(default=0, description="内容块索引")
	toolCall		: ToolCall = Field(default_factory=ToolCall, description="完成的工具调用")


AssistantMessageEvent = Annotated[
	Union[
		TextStartEvent,
		TextDeltaEvent,
		TextEndEvent,
		ThinkingStartEvent,
		ThinkingDeltaEvent,
		ThinkingEndEvent,
		ToolcallStartEvent,
		ToolcallDeltaEvent,
		ToolcallEndEvent,
	],
	Field(discriminator="type")
]