from dataclasses	import dataclass, field
from typing			import Any


@dataclass
class ToolResultChunk:
	
	"""
	内部模型
	工具产出的一个结果块
	由后端转换为 tool_result 帧
	"""
	
	result: Any	= field(default=None)