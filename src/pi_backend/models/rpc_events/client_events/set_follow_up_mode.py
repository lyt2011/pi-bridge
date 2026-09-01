from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class SetFollowUpModeCommand(BaseCommand):
	
	"""SetFollowUpModeCommand RPC 指令"""
	
	type: Literal["set_follow_up_mode"] = Field(default="set_follow_up_mode", description="指令类型")
	
	mode: Literal["all", "one-at-a-time"]	= Field(..., description="follow-up消息投递模式")
