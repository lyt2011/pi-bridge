from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class TurnStartEvent(BaseRPCEvent):
	
	"""TurnStartEvent 事件模型"""
	
	type: Literal["turn_start"] = Field(default="turn_start", description="事件类型")
