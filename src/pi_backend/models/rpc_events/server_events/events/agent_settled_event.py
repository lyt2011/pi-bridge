from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class AgentSettledEvent(BaseRPCEvent):
	
	"""AgentSettledEvent 事件模型"""
	
	type: Literal["agent_settled"] = "agent_settled"
