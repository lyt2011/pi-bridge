from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class TurnEndEvent(BaseRPCEvent):
	
	"""TurnEndEvent 事件模型"""
	
	type: Literal["turn_end"] = "turn_end"
	message: Dict[str, Any] = Field(default_factory=dict, description="助手消息")
	toolResults: List[Dict[str, Any]] = Field(default_factory=list, description="工具执行结果列表")
