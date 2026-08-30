from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class SetAutoRetryCommand(BaseCommand):
	
	"""SetAutoRetryCommand RPC 指令"""
	
	type: Literal["set_auto_retry"] = "set_auto_retry"
	
	enabled: bool	= Field(..., description="是否启用自动重试")
