from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class SummarizationRetryScheduledEvent(BaseRPCEvent):
	
	"""SummarizationRetryScheduledEvent 事件模型"""
	
	type: Literal["summarization_retry_scheduled"] = Field(default="summarization_retry_scheduled", description="事件类型")
	attempt: int = Field(default=1, description="当前尝试次数")
	maxAttempts: int = Field(default=1, description="最大尝试次数")
	delayMs: int = Field(default=0, description="重试延迟 (毫秒)")
	errorMessage: str = Field(default="", description="触发重试的错误信息")
