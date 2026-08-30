from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class SwitchSessionCommand(BaseCommand):
	
	"""SwitchSessionCommand RPC 指令"""
	
	type: Literal["switch_session"] = "switch_session"
	
	sessionPath: str	= Field(..., description="会话文件路径")
