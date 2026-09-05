from typing	import Any, Dict, Literal, Union, Annotated

from pydantic	import BaseModel, Field


class TextContent(BaseModel):
	
	"""文本内容块"""
	
	type	: Literal["text"]	= Field(default="text", description="内容块类型")
	text	: str				= Field(default="", description="文本内容")


class ImageContent(BaseModel):
	
	"""图片内容块"""
	
	type	: Literal["image"]	= Field(default="image", description="内容块类型")
	data	: str				= Field(default="", description="图片数据")
	mimeType: str				= Field(default="", description="MIME 类型")


class ThinkingContent(BaseModel):
	
	"""思考内容块"""
	
	type		: Literal["thinking"]	= Field(default="thinking", description="内容块类型")
	thinking	: str					= Field(default="", description="思考内容")


class ToolCall(BaseModel):
	
	"""工具调用内容块"""
	
	type		: Literal["toolCall"]	= Field(default="toolCall", description="内容块类型")
	id			: str					= Field(default="", description="工具调用ID")
	name		: str					= Field(default="", description="工具名称")
	arguments	: Dict[str, Any]		= Field(default_factory=dict, description="工具调用参数")


ContentBlock = Annotated[
	Union[TextContent, ImageContent, ThinkingContent, ToolCall],
	Field(discriminator="type")
]