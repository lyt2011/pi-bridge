from ...base_rpc_event	import BaseRPCEvent
from ...._shared	import Usage, AssistantMessageEvent

from typing		import Literal, Optional
from pydantic	import Field



class MessageUpdateEvent(BaseRPCEvent):
	
	"""MessageUpdateEvent 事件模型"""
	
	type: Literal["message_update"] = Field(default="message_update", description="事件类型")
	usage: Optional[Usage] = Field(default=None, description="累计 usage 信息")
	assistantMessageEvent: Optional[AssistantMessageEvent] = Field(default=None, description="增量事件 (text/thinking/toolcall delta)")
