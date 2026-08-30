from ..base_event	import BaseEvent

from pydantic	import Field


class PrivateToolEvent(BaseEvent):
	
	id: str = Field(..., description="工具调用ID")