from .base_command	import BaseCommand

from typing		import Literal


class GetLastAssistantTextCommand(BaseCommand):
	
	"""GetLastAssistantTextCommand RPC 指令"""
	
	type: Literal["get_last_assistant_text"] = "get_last_assistant_text"
