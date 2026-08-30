from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class SummarizationRetryFinishedEvent(BaseRPCEvent):
	
	"""SummarizationRetryFinishedEvent 事件模型"""
	
	type: Literal["summarization_retry_finished"] = "summarization_retry_finished"
