from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class CompactionEndEvent(BaseRPCEvent):
	
	"""CompactionEndEvent 事件模型"""
	
	type: Literal["compaction_end"] = "compaction_end"
	reason: str = Field(default="", description="压缩原因: manual/threshold/overflow")
	result: Dict[str, Any] = Field(default_factory=dict, description="压缩结果 (失败/中止时为 None)")
	aborted: bool = Field(default=False, description="是否被中止")
	willRetry: bool = Field(default=False, description="是否将自动重试")
	errorMessage: str = Field(default="", description="失败时的错误信息")
