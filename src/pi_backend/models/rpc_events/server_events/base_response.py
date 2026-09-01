from ..base_rpc_event	import BaseRPCEvent

from ....enums	import CommandEnum

from typing		import Literal, Dict, Any, Optional
from pydantic	import Field, field_validator


class BaseResponse(BaseRPCEvent):
	
	"""PI AGENT 的响应基类"""
	
	type: Literal["response"] = Field(default="response", description="响应类型")
	
	id		: Optional[str]	= Field(default=None, description="请求/响应关联ID")
	command	: CommandEnum	= Field(..., description="server返回的RPC指令")
	success	: bool			= Field(..., description="指令是否被接受成功(非指令执行结果)")
	
	data	: Optional[Dict[str, Any]]	= Field(default_factory=dict, description="额外的信息字段")
	error	: Optional[str]				= Field(default=None, description="失败时的错误信息")
	
	@field_validator("command", mode="before")
	@classmethod
	def _coerce_command(cls, value: Any) -> Any:
		
		"""
		将字符串形式的 command 转换为 CommandEnum 成员
		以便子类使用 Literal[CommandEnum.xxx] 作为判别字段 (easy_factory 分发)
		"""
		
		if isinstance(value, str):
			return CommandEnum(value)
		
		return value