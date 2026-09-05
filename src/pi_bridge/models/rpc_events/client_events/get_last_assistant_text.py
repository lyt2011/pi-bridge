from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class GetLastAssistantTextCommand(BaseCommand):
	
	"""GetLastAssistantTextCommand RPC 指令"""
	
	type: Literal["get_last_assistant_text"] = Field(default="get_last_assistant_text", description="指令类型")
