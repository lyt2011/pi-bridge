from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class AgentEndEvent(BaseRPCEvent):
	
	"""AgentEndEvent 事件模型"""
	
	type: Literal["agent_end"] = "agent_end"
	messages: List[Dict[str, Any]] = Field(default_factory=list, description="本次运行生成的所有消息")
	willRetry: bool = Field(default=False, description="是否将自动重试")
