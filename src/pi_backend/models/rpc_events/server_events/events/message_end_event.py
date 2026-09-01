from ...base_rpc_event	import BaseRPCEvent
from ...._shared	import AgentMessage

from typing		import Literal, Optional
from pydantic	import Field



class MessageEndEvent(BaseRPCEvent):
	
	"""MessageEndEvent 事件模型"""
	
	type: Literal["message_end"] = Field(default="message_end", description="事件类型")
	message: Optional[AgentMessage] = Field(default=None, description="最终消息对象 (AgentMessage)")
