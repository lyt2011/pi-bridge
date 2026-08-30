from ..base_rpc_event	import BaseRPCEvent

from typing		import Optional
from pydantic	import Field


class BaseCommand(BaseRPCEvent):
	
	"""PI AGENT 的 RPC 指令基类"""
	
	id: Optional[str] = Field(default=None, description="请求/响应关联ID")
