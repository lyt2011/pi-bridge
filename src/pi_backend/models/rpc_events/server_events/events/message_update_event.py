from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class MessageUpdateEvent(BaseRPCEvent):
	
	"""MessageUpdateEvent 事件模型"""
	
	type: Literal["message_update"] = "message_update"
	usage: Dict[str, Any] = Field(default_factory=dict, description="累计 usage 信息")
	assistantMessageEvent: Dict[str, Any] = Field(default_factory=dict, description="增量事件 (text/thinking/toolcall delta)")
