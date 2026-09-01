from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class QueueUpdateEvent(BaseRPCEvent):
	
	"""QueueUpdateEvent 事件模型"""
	
	type: Literal["queue_update"] = Field(default="queue_update", description="事件类型")
	steering: List[str] = Field(default_factory=list, description="待处理的 steering 队列")
	followUp: List[str] = Field(default_factory=list, description="待处理的 follow-up 队列")
