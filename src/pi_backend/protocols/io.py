"""线级 IO 协议 (鸭子类型, 供 PiTransport 注入缝)"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class LineProtocol(Protocol):
	
	"""
	线级 IO 伙伴协议
	
	要求: async read_line() -> str
		  async write_line(*lines: str) -> None
	
	close 可选: PiTransport.close() 会先尝试 io.close_process(),
	再回退到 io.close(), 两者都没有则跳过
	"""
	
	async def read_line(self) -> str: ...
	
	async def write_line(self, *lines: str) -> None: ...