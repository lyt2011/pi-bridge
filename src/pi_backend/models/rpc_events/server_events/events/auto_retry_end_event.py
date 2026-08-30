from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List
from pydantic	import Field



class AutoRetryEndEvent(BaseRPCEvent):
	
	"""AutoRetryEndEvent 事件模型"""
	
	type: Literal["auto_retry_end"] = "auto_retry_end"
	success: bool = Field(default=False, description="是否重试成功")
	attempt: int = Field(default=1, description="最终尝试次数")
	finalError: str = Field(default="", description="最终失败时的错误信息")
