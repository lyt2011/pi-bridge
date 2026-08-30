from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class CompactionStartEvent(BaseRPCEvent):
	
	"""CompactionStartEvent 事件模型"""
	
	type: Literal["compaction_start"] = "compaction_start"
	reason: str = Field(default="", description="压缩原因: manual/threshold/overflow")
