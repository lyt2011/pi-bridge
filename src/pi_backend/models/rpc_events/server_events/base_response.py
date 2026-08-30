from ..base_rpc_event	import BaseRPCEvent

from typing		import Literal, Dict, Any, Optional
from pydantic	import Field


class BaseResponse(BaseRPCEvent):
	
	"""PI AGENT 的响应基类"""
	
	type: Literal["response"] = "response"
	
	id		: Optional[str]	= Field(default=None, description="请求/响应关联ID")
	command	: str			= Field(..., description="server返回的RPC指令")
	success	: bool			= Field(..., description="指令是否被接受成功(非指令执行结果)")
	
	data	: Optional[Dict[str, Any]]	= Field(default_factory=dict, description="额外的信息字段")
	error	: Optional[str]				= Field(default=None, description="失败时的错误信息")