from dataclasses	import dataclass, field
from typing			import Any, Optional


@dataclass
class ToolEndFlag:
	
	"""
	内部模型
	工具调用结束标记
	由后端转换为 tool_execution_end 帧
	"""
	
	reason: Optional[str] = field(default=None)