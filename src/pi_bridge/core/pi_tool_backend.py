from ..models			import PrivateToolExecution, PrivateToolResult, PrivateToolExecutionEnd
from ..models._internal import ToolResultChunk, ToolEndFlag

from typing		import Dict, Callable, Any, Awaitable, Tuple, Optional, AsyncIterable, Union
from inspect	import isasyncgenfunction
from asyncio	import StreamWriter, StreamReader, Lock, Server, Task, CancelledError, wait_for
from contextlib	import suppress, aclosing

import asyncio
import os


ASYNC_FUNC = Callable[..., Awaitable[Any]]
STREAM_PAIR = Tuple[StreamReader, StreamWriter]

RECV_TIMEOUT = 5
DEFAULT_HOST = str(os.environ.get("PTBACKEND_HOST", "127.0.0.1"))
DEFAULT_PORT = int(os.environ.get("PTBACKEND_PORT", 39999))


class PIToolBackend:
	
	"""
	PI 的私有工具协议后端
	**不是 PI 官方的协议**
	"""

	def __init__(
		self, *,
		host: Optional[str] = None,
		port: Optional[int] = None
	) -> None:
		
		self.host = host or DEFAULT_HOST
		self.port = port or DEFAULT_PORT
		
		# tool_waiter字典操作锁
		self._tw_op_lock: Lock = Lock()
		
		self._registered_tools	: Dict[str, ASYNC_FUNC]		= {}
		self._tool_waiter		: Dict[str, STREAM_PAIR]	= {}
		self._connections		: set	= set()
		self._handler_tasks		: set	= set()
		
		self._execute_timeout_seconds: float = 30.0
		
		self.task	: Task		= None
		self.server	: Server	= None
	
	@property # 守护任务与server实例同时存在才True
	def is_available(self) -> bool:
		return (self.task is not None) and (self.server is not None)
	
	def set_timeout(self, timeout: float) -> None:
		self._execute_timeout_seconds = timeout
	
	def register_tool(self, func: ASYNC_FUNC, name: Optional[str] = None) -> None:
		
		# 可选的name 默认使用函数名
		if not isinstance(name, str):
			name = func.__name__
		
		if name in self._registered_tools:
			raise RuntimeError(f"Tool {name} is existing")
		
		self._registered_tools[name] = func
	
	async def send_result(self, id: str, result: Any) -> None:
		
		"""
		给 id 对应的 writer 发送 结果帧
		不存在的 id 则 直接抛弃该信息
		(注意:不移除 waiter 条目,便于生成器工具多次发送;连接由 ensure_close 统一关闭)
		"""
		
		async with self._tw_op_lock:
		
			if id not in self._tool_waiter:
				return None
			
			_, writer = self._tool_waiter[id]
		
		await self._send(writer, PrivateToolResult(id=id, result=str(result)).model_dump_json())
	
	async def send_end(self, id: str, reason: Optional[str] = None) -> None:
		
		"""
		给 id 对应的 writer 发送 结束帧
		不存在的 id 则 直接抛弃该信息
		(注意:不移除 waiter 条目,连接由 ensure_close 统一关闭)
		"""
		
		async with self._tw_op_lock:
		
			if id not in self._tool_waiter:
				return None
			
			_, writer = self._tool_waiter[id]
		
		await self._send(writer, PrivateToolExecutionEnd(id=id, reason=reason).model_dump_json())
	
	async def close_backend(self) -> None:
		
		"""执行清理工作后关闭 socket 监听"""
		
		async with self._tw_op_lock:
			
			writers			= list(self._connections)
			handler_tasks	= list(self._handler_tasks)
			
			self._connections.clear()
			self._tool_waiter.clear()
		
		for writer in writers:
			await self._close_writer(writer)
		
		for handler_task in handler_tasks:
			handler_task.cancel()
		
		for handler_task in handler_tasks:
			with suppress(Exception, CancelledError):
				await wait_for(handler_task, timeout=5)
		
		await self._close_server()
		
		return None
				
	
	async def ensure_close(self, id: str) -> None:
		
		"""
		高层:管理 reader 与 writer 的生命周期
		负责关闭连接并清理数据
		id 不存在则 直接返回 不进行任何操作
		"""
		
		await self._cleanup_connection(id)
	
	async def on_execute_tool(self, id: str, tool_name: str, tool_params: Dict[str, Any]) -> None:
		
		"""
		对外暴露带有超时的工具执行函数
		自动发送结果/结束/超时帧
		"""
		
		generation = self._execute_tool(tool_name, tool_params)
		
		# aclosing 保证生成器在循环结束(正常/异常/取消)后一定被关闭,资源不泄漏
		async with aclosing(generation):
		
			while True:
			
				output = await self._next_tool_output(tool_name, generation)
				
				# 结束标记 → 发送结束帧
				if isinstance(output, ToolEndFlag):
					await self.send_end(id, reason = output.reason)
					return
				
				# 结果块 → 发送结果帧
				await self.send_result(id, output.result)
		
		return None
	
	async def on_connect(self, reader: StreamReader, writer: StreamWriter) -> None:
		
		"""
		处理单个工具调用请求:
		读取一帧 PrivateToolExecution → 注册 waiter → 执行工具并自动发送结果/结束帧 → 关闭连接
		无论正常/异常/取消,finally 都会确保连接关闭、waiter 清理
		"""
		
		handler_task = asyncio.current_task()
		
		async with self._tw_op_lock:
			self._connections.add(writer)
			self._handler_tasks.add(handler_task)
		
		tool_execution: Optional[PrivateToolExecution] = None
		
		try:
		
			tool_execution = await self._recv_tool_request(reader)
			
			# 解析失败:不建 waiter,直接关闭连接 避免资源泄漏
			if tool_execution is None:
				return None
			
			# 已拿到有效请求:注册 waiter 供工具推送帧
			async with self._tw_op_lock:
				self._tool_waiter[tool_execution.id] = (reader, writer)
			
			# 只负责执行逻辑
			await self.on_execute_tool(tool_execution.id, tool_execution.tool_name, tool_execution.tool_params)
			
			return None
		
		finally:
			
			if tool_execution is None:
				await self._close_writer(writer)
			
			else:
				await self.ensure_close(tool_execution.id)
			
			async with self._tw_op_lock:
				self._connections.discard(writer)
				self._handler_tasks.discard(handler_task)
	
	async def run_server(self, **kwargs) -> Tuple[Server, Task]:
		
		self.server = await asyncio.start_server(
			self.on_connect,
			host	= self.host,
			port	= self.port,
			**kwargs
		)
		
		self.task = asyncio.create_task(self.server.serve_forever())
		
		return self.server, self.task
	
	async def _execute_tool(self, tool_name: str, tool_params: Dict[str, Any]) -> AsyncIterable[Any]:
		
		"""
		兼容异步生成器/函数的工具执行器
		仅负责执行:内部将参数字典展开传给工具
		"""
		
		if tool_name not in self._registered_tools:
			raise RuntimeError(f"Tool {tool_name} is not found")
		
		func = self._registered_tools[tool_name]
		
		# 生成器逻辑
		if isasyncgenfunction(func):
			
			async for output in func(**tool_params):
				yield output
		
		# 普通异步函数逻辑
		else:
			
			result = await func(**tool_params)
			yield result
		
		return
	
	async def _next_tool_output(self, tool_name: str, generation) -> Union[ToolResultChunk, ToolEndFlag]:
		
		"""
		单步推进工具生成器
		返回 ToolResultChunk:正常产出一帧,继续推进
		返回 ToolEndFlag:调用结束(正常结束 / 超时 / 错误),并携带结束原因
		"""
		
		try:
		
			async with asyncio.timeout(self._execute_timeout_seconds):
				result = await generation.__anext__()
		
		except StopAsyncIteration:
			return ToolEndFlag()
		
		except asyncio.TimeoutError:
			return ToolEndFlag(reason = f"tool {tool_name} executed timeout with {self._execute_timeout_seconds} seconds")
		
		except Exception as exception:
			return ToolEndFlag(reason = f"tool {tool_name} executed with error {str(exception)}")
		
		return ToolResultChunk(result = result)
	
	async def _send(self, writer: StreamWriter, msg: str) -> None:
		
		"""封装缓冲区写入与提交的内部函数(帧以换行分隔)"""
		
		writer.write(msg.encode("utf-8") + b"\n")
		await writer.drain()
	
	async def _recv_line(self, reader: StreamReader) -> bytes:
		
		"""封装接收逻辑 增加超时"""
		
		b_msg = await asyncio.wait_for(
			reader.readline(),
			timeout = RECV_TIMEOUT
		)
		
		return b_msg
	
	async def _recv_tool_request(self, reader: StreamReader) -> Optional[PrivateToolExecution]:
		
		"""
		读取一帧请求并解析为 PrivateToolExecution
		失败则返回 None
		"""
		
		try:
		
			b_first_msg = await self._recv_line(reader)
			first_msg = b_first_msg.decode("utf-8")
			return PrivateToolExecution.model_validate_json(first_msg)
		
		except Exception:
			return None
	
	async def _cleanup_connection(self, id: str) -> None:
		
		"""
		仅按 id 从 waiter 表弹出该连接并关闭
		只负责 waiter 清理,不耦合任何请求模型
		id 不存在则 直接返回 不进行任何操作
		"""
		
		async with self._tw_op_lock:
		
			if id not in self._tool_waiter:
				return None
			
			_, writer = self._tool_waiter.pop(id)
		
		# 锁外关闭连接 不堵塞锁
		await self._close_writer(writer)
		
		return None
	
	async def _close_writer(self, writer: StreamWriter) -> None:
		
		"""关闭连接 吞掉一切异常(收尾专用)"""
		
		with suppress(Exception):
			writer.close()
			await writer.wait_closed()
	
	async def _close_server(self) -> None:
		
		# server 未启动时无需清理(幂等)
		if self.task is None or self.server is None:
			return None
		
		# 关闭 socket 管道
		self.server.close()
		await self.server.wait_closed()
		
		# 关闭守护任务
		with suppress(asyncio.CancelledError):
			self.task.cancel()
			await self.task
		
		self.task	= None
		self.server	= None
		
		return None