from ...base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, List, Optional
from pydantic	import Field



class BashExecutionUpdateEvent(BaseRPCEvent):
	
	"""BashExecutionUpdateEvent 事件模型"""
	
	type: Literal["bash_execution_update"] = "bash_execution_update"
	id	: Optional[str]	= Field(default=None, description="关联的 bash 指令 id")
	delta: str			= Field(default="", description="命令输出增量")
