from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class GetAvailableThinkingLevelsCommand(BaseCommand):
	
	"""GetAvailableThinkingLevelsCommand RPC 指令"""
	
	type: Literal["get_available_thinking_levels"] = Field(default="get_available_thinking_levels", description="指令类型")
