from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class MessageStartEvent(BaseRPCEvent):
	
	"""MessageStartEvent 事件模型"""
	
	type: Literal["message_start"] = "message_start"
	message: Dict[str, Any] = Field(default_factory=dict, description="消息对象 (AgentMessage)")
