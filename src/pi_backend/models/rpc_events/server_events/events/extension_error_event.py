from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class ExtensionErrorEvent(BaseRPCEvent):
	
	"""ExtensionErrorEvent 事件模型"""
	
	type: Literal["extension_error"] = "extension_error"
	extensionPath: str = Field(default="", description="出错的扩展路径")
	event: str = Field(default="", description="出错的事件名")
	error: str = Field(default="", description="错误信息")
