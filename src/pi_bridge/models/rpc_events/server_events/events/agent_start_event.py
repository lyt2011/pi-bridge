from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class AgentStartEvent(BaseRPCEvent):
	
	"""AgentStartEvent 事件模型"""
	
	type: Literal["agent_start"] = Field(default="agent_start", description="事件类型")
