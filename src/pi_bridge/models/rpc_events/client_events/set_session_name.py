from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class SetSessionNameCommand(BaseCommand):
	
	"""SetSessionNameCommand RPC 指令"""
	
	type: Literal["set_session_name"] = Field(default="set_session_name", description="指令类型")
	
	name: str	= Field(..., description="会话显示名称")
