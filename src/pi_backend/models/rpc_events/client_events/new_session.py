from .base_command	import BaseCommand

from typing		import Literal, Optional
from pydantic	import Field


class NewSessionCommand(BaseCommand):
	
	"""NewSessionCommand RPC 指令"""
	
	type: Literal["new_session"] = "new_session"
	
	parentSession: Optional[str]	= Field(default=None, description="父会话文件路径")
