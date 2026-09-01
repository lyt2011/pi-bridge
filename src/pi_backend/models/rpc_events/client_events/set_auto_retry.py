from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class SetAutoRetryCommand(BaseCommand):
	
	"""SetAutoRetryCommand RPC 指令"""
	
	type: Literal["set_auto_retry"] = Field(default="set_auto_retry", description="指令类型")
	
	enabled: bool	= Field(..., description="是否启用自动重试")
