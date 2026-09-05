from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class SummarizationRetryAttemptStartEvent(BaseRPCEvent):
	
	"""SummarizationRetryAttemptStartEvent 事件模型"""
	
	type: Literal["summarization_retry_attempt_start"] = Field(default="summarization_retry_attempt_start", description="事件类型")
	source: str = Field(default="", description="来源: compaction/branchSummary")
	reason: str = Field(default="", description="压缩原因 (branchSummary 时无此字段)")
