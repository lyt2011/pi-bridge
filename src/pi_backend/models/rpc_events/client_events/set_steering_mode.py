from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class SetSteeringModeCommand(BaseCommand):
	
	"""SetSteeringModeCommand RPC 指令"""
	
	type: Literal["set_steering_mode"] = "set_steering_mode"
	
	mode: Literal["all", "one-at-a-time"]	= Field(..., description="steering消息投递模式")
