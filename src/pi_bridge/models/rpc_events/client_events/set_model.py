from .base_command	import BaseCommand

from typing		import Literal
from pydantic	import Field


class SetModelCommand(BaseCommand):
	
	"""SetModelCommand RPC 指令"""
	
	type: Literal["set_model"] = Field(default="set_model", description="指令类型")
	
	provider: str	= Field(..., description="提供商")
	modelId: str	= Field(..., description="模型ID")
