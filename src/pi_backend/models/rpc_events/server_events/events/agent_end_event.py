from ...base_rpc_event	import BaseRPCEvent
from ...._shared	import AgentMessage

from typing		import Literal, List
from pydantic	import Field



class AgentEndEvent(BaseRPCEvent):
	
	"""AgentEndEvent 事件模型"""
	
	type: Literal["agent_end"] = Field(default="agent_end", description="事件类型")
	messages: List[AgentMessage] = Field(default_factory=list, description="本次运行生成的所有消息")
	willRetry: bool = Field(default=False, description="是否将自动重试")
