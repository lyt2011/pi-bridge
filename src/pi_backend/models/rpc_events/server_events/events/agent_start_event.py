from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class AgentStartEvent(BaseRPCEvent):
	
	"""AgentStartEvent 事件模型"""
	
	type: Literal["agent_start"] = "agent_start"
