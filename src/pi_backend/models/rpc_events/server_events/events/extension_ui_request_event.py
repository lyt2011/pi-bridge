from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List, Optional
from pydantic	import Field



class ExtensionUIRequestEvent(BaseRPCEvent):
	
	"""ExtensionUIRequestEvent 事件模型"""
	
	type: Literal["extension_ui_request"] = "extension_ui_request"
	id	: Optional[str]	= Field(default=None, description="UI 请求唯一 id")
	method: str = Field(..., description="UI 方法: select/confirm/input/editor/notify/setStatus/setWidget/setTitle/set_editor_text")
	title: str = Field(default="", description="标题")
	message: str = Field(default="", description="消息内容")
	options: List[str] = Field(default_factory=list, description="选项列表 (select)")
	timeout: int = Field(default=0, description="超时毫秒数 (dialog 方法可选)")
	placeholder: str = Field(default="", description="输入占位符 (input)")
	prefill: str = Field(default="", description="预填充内容 (editor)")
	notifyType: str = Field(default="info", description="通知类型: info/warning/error")
	statusKey: str = Field(default="", description="状态栏键 (setStatus)")
	statusText: str = Field(default="", description="状态文本 (setStatus)")
	widgetKey: str = Field(default="", description="组件键 (setWidget)")
	widgetLines: List[str] = Field(default_factory=list, description="组件文本行 (setWidget)")
	widgetPlacement: str = Field(default="aboveEditor", description="组件位置: aboveEditor/belowEditor")
	text: str = Field(default="", description="编辑器文本 (set_editor_text)")
