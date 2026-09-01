from typing	import Optional

from ..factory		import responses_factory, events_factory
from ..models		import BaseCommand, BaseRPCEvent
from ..protocols	import LineProtocol

from easy_factory	import DispatchFailed

import orjson


class PiTransport:
	
	"""
	PI 的 JSONL 传输层
	
	仅负责: 序列化指令 + 发送 / 读取行 + 工厂校验解析
	不负责: 进程管理 / 后台 reader / 状态维护
	
	接收一个线级 IO 对象作为伙伴 (鸭子类型, 见 protocols.LineProtocol), 需要提供:
	- read_line()   -> str     (异步)
	- write_line(*lines) -> None (异步)
	- close_process() 或 close() -> None (可选, 用于清理)
	"""
	
	def __init__(self, io: LineProtocol) -> None:
		
		self._io = io
	
	async def send(self, command: BaseCommand) -> None:
		
		"""序列化指令模型并写入一行"""
		
		await self._io.write_line(command.model_dump_json(exclude_none=True))
	
	async def recv(self) -> BaseRPCEvent:
		
		"""
		读取一行并解析为响应/事件模型
		
		优先匹配响应工厂 (responses_factory.dispatcher);
		非响应行 (事件等) 回退到事件工厂 (events_factory.dispatcher)
		"""
		
		line = await self._io.read_line()
		data = orjson.loads(line)
		
		try:
			return responses_factory.dispatcher(data)
		except DispatchFailed:
			return events_factory.dispatcher(data)
	
	async def close(self) -> None:
		
		"""关闭底层 IO (若提供了 close_process 或 close 方法)"""
		
		closer = getattr(self._io, "close_process", None) or getattr(self._io, "close", None)
		
		if closer is not None:
			await closer()