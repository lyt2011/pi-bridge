from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class MessageEndEvent(BaseRPCEvent):
	
	"""MessageEndEvent 事件模型"""
	
	type: Literal["message_end"] = "message_end"
	message: Dict[str, Any] = Field(default_factory=dict, description="最终消息对象 (AgentMessage)")
