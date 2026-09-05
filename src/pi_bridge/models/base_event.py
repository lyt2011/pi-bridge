from pydantic	import BaseModel, Field


class BaseEvent(BaseModel):
	
	type: str = Field(..., description="事件类型")