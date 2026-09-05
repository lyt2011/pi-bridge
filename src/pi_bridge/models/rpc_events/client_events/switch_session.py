from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class SwitchSessionCommand(BaseCommand):
	
	"""SwitchSessionCommand RPC 指令"""
	
	type: Literal["switch_session"] = Field(default="switch_session", description="指令类型")
	
	sessionPath: str	= Field(..., description="会话文件路径")
