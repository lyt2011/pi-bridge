from typing		import Optional, Dict, List, Literal, Any, Self
from collections.abc	import Awaitable, Callable
from contextlib	import suppress

from .pi_process	import PIProcess
from .pi_transport	import PiTransport
from ..				import models

from easy_factory	import DispatchFailed

import asyncio
import uuid


# ------------------------------------------------------------------
# 类型别名
# ------------------------------------------------------------------

# 构建工厂: 任意 async callable (函数 / 可调用实例); None 表示用默认构建器
BuildFactory = Optional[Callable[..., Awaitable[Any]]]


class PiClient:
	
	"""
	PI 的类型化 RPC 客户端
	
	组合一个 PiTransport, 提供:
	- request(): 发指令 → id→Future 路由 → 等对应响应 (点对点)
	- subscribe(): 事件广播订阅 (fan-out, 每个订阅者一个 Queue)
	- 后台 reader: 常驻 drain 管道, 崩溃时 set_exception 唤醒全部等待者
	
	生命周期: start() 起 reader, close() 收尾。响应/事件都由 reader 统一分发。
	
	超时: 用 set_timeout() 设置实例全局超时 (秒), 默认不启用 (None);
	request() 未显式传 timeout 时使用该全局值 (timeout or self._timeout)。
	"""
	
	def __init__(self, transport: PiTransport) -> None:
		
		# 依赖注入
		self._transport		= transport
		
		# 运行时状态
		self._pending		= {}			# id → Future, 未决的请求
		self._subscribers	= []			# 事件广播订阅者 (asyncio.Queue)
		self._reader		= None			# 后台 reader task
		self._broken		= None			# reader 崩溃原因 (异常)
		
		# 配置与缓存
		self._state			= None			# 上次 get_state() 的状态快照
		self._timeout		= None			# 全局请求超时 (秒), set_timeout 设置
	
	# ------------------------------------------------------------------
	# 工厂: 建进程 → 建传输 → 建 client → 起 reader
	# ------------------------------------------------------------------
	
	@staticmethod
	async def _build_process(*args, build_factory: BuildFactory = None, **kwargs) -> Any:
		
		"""
		构建 PIProcess (默认 PIProcess.build)
		
		build_factory 仅关键字传参, 缺省回退到 PIProcess.build;
		传入任意 async callable (函数 / 可调用实例) 可注入自定义构建逻辑;
		args/kwargs 透传给 build_factory (如 open 里的进程参数)
		"""
		
		if build_factory is None:
			build_factory = PIProcess.build
		
		return await build_factory(*args, **kwargs)
	
	@staticmethod
	async def _build_transport(*args, build_factory: BuildFactory = None, **kwargs) -> Any:
		
		"""
		构建 PiTransport (默认 PiTransport.build)
		
		build_factory 仅关键字传参, 缺省回退到 PiTransport.build;
		传入任意 async callable (函数 / 可调用实例) 可注入自定义构建逻辑;
		args/kwargs 透传给 build_factory (如 open 里的 io 伙伴)
		"""
		
		if build_factory is None:
			build_factory = PiTransport.build
		
		return await build_factory(*args, **kwargs)
	
	@classmethod
	async def build(cls, transport: PiTransport, **kwargs) -> Self:
		
		"""
		用已构建好的 transport 实例化 client
		
		kwargs 透传给 cls, 供子类扩展构造参数
		"""
		
		return cls(transport, **kwargs)
	
	@classmethod
	async def open(cls, **process_kwargs) -> Self:
		
		"""
		一条龙工厂: 构建 PIProcess → PiTransport → PiClient 并启动后台 reader
		
		process_kwargs 透传给 PIProcess.build
		(pi_path / session / session_dir / tools / system_prompt)
		"""
		
		process		= await cls._build_process(**process_kwargs)
		transport	= await cls._build_transport(process)
		client		= await cls.build(transport)
		
		await client.start()
		
		return client
	
	# ------------------------------------------------------------------
	# 生命周期
	# ------------------------------------------------------------------
	
	async def start(self) -> asyncio.Task:
		
		"""启动后台 reader"""
		
		if self._reader is None:
			self._reader = asyncio.create_task(self._read_loop())
		
		return self._reader
	
	async def close(self) -> None:
		
		"""取消后台 reader 并关闭传输层"""
		
		if self._reader is not None:
			
			self._reader.cancel()
			
			with suppress(Exception, asyncio.CancelledError):
				await self._reader
			
			self._reader = None
		
		await self._transport.close()
	
	# ------------------------------------------------------------------
	# 后台 reader: 常驻 drain, 集中错误处理
	# ------------------------------------------------------------------
	
	def _set_exception_pendings(self, exception: Exception) -> None:
		
		for fut in self._pending.values():
			if not fut.done():
				fut.set_exception(exception)
		
		return None
	
	async def _read_loop(self) -> None:
		
		"""
		后台读取循环
		
		无条件 drain 管道 (管道不消费会堵死 pi 进程);
		EOF/崩溃时: 记录 _broken, 给所有未决 Future set_exception,
		并向所有订阅者队列 push 异常 sentinel (防止消费方永久阻塞);
		解析失败的行 (DispatchFailed) 跳过, 不视为崩溃
		"""
		
		while True:
			
			try:
				
				model = await self._transport.recv()
				self._route(model)
				
			except asyncio.CancelledError:
				raise
				
			except DispatchFailed:
				# 无法解析的行 (如无 command 判别键的异常响应): 跳过, 继续
				continue
				
			except Exception as e:
				
				self._broken = e
				
				self._set_exception_pendings(e)
				self._pending.clear()
				
				for q in self._subscribers:
					q.put_nowait(e)
				
				return None
	
	# ------------------------------------------------------------------
	# 路由: 响应 → Future (点对点), 其余 → 广播 (fan-out)
	# ------------------------------------------------------------------
	
	def _route(self, model: object) -> None:
		
		"""
		把 reader 收到的模型分发给对应消费者
		
		响应 (models.BaseResponse): 按 id 找到未决 Future 并 set_result;
		非响应 (事件等): fan-out 广播给所有订阅者队列
		"""
		
		if isinstance(model, models.BaseResponse):
			
			req_id	= model.id
			fut			= self._pending.pop(req_id, None)
			
			if fut is not None and not fut.done():
				fut.set_result(model)
			
			# 未匹配到未决请求的响应 (如已被取消/超时): 直接丢弃
			return None
		
		for queue in self._subscribers:
			
			if queue.maxsize > 0 and queue.qsize() >= queue.maxsize:
				queue.get_nowait()
			
			queue.put_nowait(model)
		
		return None
	
	# ------------------------------------------------------------------
	# 提示: 发 prompt 指令 → 流式消费事件
	# ------------------------------------------------------------------
	
	async def prompt(self, message: str, *, images: Optional[list] = None, streamingBehavior: Optional[str] = None):
		
		"""
		发送 prompt 指令并以 async generator 流式消费后续事件
		
		用法:
			async for evt in client.prompt("你好"):
				print(evt)
		
		接受成功后, 依次 yield 每个事件, 遇到 models.AgentSettledEvent 结束;
		接受被拒 (success=False) 时立即结束, 不产出事件
		"""
		
		cmd = models.PromptCommand(
			message				= message,
			images				= images,
			streamingBehavior	= streamingBehavior,
		)
		
		# 先订阅再发指令: 避免响应到达前漏掉事件
		q = self.subscribe()
		
		try:
			
			resp = await self.request(cmd)
			
			if not resp.success:
				return
			
			while True:
				
				evt = await q.get()
				
				# reader 崩溃时队列里会出现异常 sentinel
				if isinstance(evt, BaseException):
					raise evt
				
				yield evt
				
				if isinstance(evt, models.AgentSettledEvent):
					break
		
		finally:
			self._subscribers.remove(q)
	
	# ------------------------------------------------------------------
	# 超时: 实例全局超时设置
	# ------------------------------------------------------------------
	
	def set_timeout(self, timeout: Optional[float] = None) -> None:
		
		"""
		设置实例全局请求超时 (秒)
		
		之后所有 request (含各语义方法) 默认使用该超时;
		timeout=None 表示不启用超时 (默认行为, 不限时);
		单次覆盖: request(cmd, timeout=...) 或 asyncio.wait_for(...)
		"""
		
		self._timeout = timeout
	
	# ------------------------------------------------------------------
	# 请求: 发指令 → 等响应
	# ------------------------------------------------------------------
	
	async def request(self, command: models.BaseCommand, timeout: Optional[float] = None) -> models.BaseResponse:
		
		"""
		发送指令并等待对应响应 (按 id 路由)
		
		返回响应模型; reader 崩溃时抛出崩溃异常;
		timeout 未传时用全局 set_timeout() 设置 (默认不限时), 单次可覆盖
		"""
		
		timeout = timeout or self._timeout
		
		if self._broken is not None:
			raise self._broken
		
		req_id		= uuid.uuid4().hex
		command.id	= req_id
		
		fut	= asyncio.get_running_loop().create_future()
		self._pending[req_id] = fut
		
		try:
			
			await self._transport.send(command)
			
			if timeout is None:
				return await fut
			
			return await asyncio.wait_for(fut, timeout=timeout)
		
		finally:
			self._pending.pop(req_id, None)
	
	# ------------------------------------------------------------------
	# 事件广播: fan-out 订阅
	# ------------------------------------------------------------------
	
	def subscribe(self, maxsize: int = 0) -> asyncio.Queue:
		
		"""
		注册一个事件订阅者 (fan-out)
		
		返回独立的 asyncio.Queue, reader 收到的事件会复制给所有订阅者;
		maxsize=0 表示不限; 设置 maxsize 可防止消费慢时积压,
		队满时挤掉最旧的 (保新丢旧), 结束时信号不会丢
		"""
		
		q = asyncio.Queue(maxsize=maxsize)
		self._subscribers.append(q)
		
		return q
	
	# ------------------------------------------------------------------
	# 状态: get_state() 惰性缓存 → state 属性
	# ------------------------------------------------------------------
	
	async def get_state(self) -> models.StateData:
		
		"""
		发送 get_state 指令并返回状态快照 (StateData)
		
		顺手缓存到 state 属性, 供同步读取
		"""
		
		response = await self.request(models.GetStateCommand())
		
		if response.data is None:
			raise RuntimeError("get_state 响应缺少 data 字段")
		
		if isinstance(response.data, dict):
			self._state = models.StateData.model_validate(response.data)
		
		else:
			self._state = response.data
		
		return self._state
	
	@property
	def state(self) -> Optional[models.StateData]:
		
		"""
		上次 get_state() 的状态快照 (惰性缓存, 无后台状态维护)
		
		未调用过 get_state 时为 None
		"""
		
		return self._state
	
	# ------------------------------------------------------------------
	# 指令语义方法: 构造命令 → await request() → 返回具体响应模型
	# ------------------------------------------------------------------
	
	async def steer(
		self,
		message	: str, *,
		images	: Optional[List[Dict]]	= None,
	) -> models.SteerResponse:
		
		"""发送 steer 指令 (排队投递插入消息)"""
		
		return await self.request(models.SteerCommand(message=message, images=images))
	
	async def follow_up(
		self,
		message	: str, *,
		images	: Optional[List[Dict]]	= None,
	) -> models.FollowUpResponse:
		
		"""发送 follow_up 指令 (排队投递消息, 仅在 agent 运行时触发)"""
		
		return await self.request(models.FollowUpCommand(message=message, images=images))
	
	async def abort(self) -> models.AbortResponse:
		
		"""发送 abort 指令 (中止当前处理)"""
		
		return await self.request(models.AbortCommand())
	
	async def clear_queue(self) -> models.ClearQueueResponse:
		
		"""发送 clear_queue 指令 (清空队列)"""
		
		return await self.request(models.ClearQueueCommand())
	
	async def new_session(self, parent_session: Optional[str] = None) -> models.NewSessionResponse:
		
		"""发送 new_session 指令 (新会话, 可选关联父会话)"""
		
		return await self.request(models.NewSessionCommand(parentSession=parent_session))
	
	async def get_messages(self) -> models.GetMessagesResponse:
		
		"""发送 get_messages 指令 (获取消息列表)"""
		
		return await self.request(models.GetMessagesCommand())
	
	async def set_model(self, provider: str, model_id: str) -> models.SetModelResponse:
		
		"""发送 set_model 指令 (切换模型)"""
		
		return await self.request(models.SetModelCommand(provider=provider, modelId=model_id))
	
	async def cycle_model(self) -> models.CycleModelResponse:
		
		"""发送 cycle_model 指令 (轮换模型)"""
		
		return await self.request(models.CycleModelCommand())
	
	async def get_available_models(self) -> models.GetAvailableModelsResponse:
		
		"""发送 get_available_models 指令 (获取可用模型列表)"""
		
		return await self.request(models.GetAvailableModelsCommand())
	
	async def set_thinking_level(self, level: str) -> models.SetThinkingLevelResponse:
		
		"""发送 set_thinking_level 指令 (设置思考级别)"""
		
		return await self.request(models.SetThinkingLevelCommand(level=level))
	
	async def cycle_thinking_level(self) -> models.CycleThinkingLevelResponse:
		
		"""发送 cycle_thinking_level 指令 (轮换思考级别)"""
		
		return await self.request(models.CycleThinkingLevelCommand())
	
	async def get_available_thinking_levels(self) -> models.GetAvailableThinkingLevelsResponse:
		
		"""发送 get_available_thinking_levels 指令 (获取可用思考级别列表)"""
		
		return await self.request(models.GetAvailableThinkingLevelsCommand())
	
	async def set_steering_mode(self, mode: Literal["all", "one-at-a-time"]) -> models.SetSteeringModeResponse:
		
		"""发送 set_steering_mode 指令 (设置steering模式)"""
		
		return await self.request(models.SetSteeringModeCommand(mode=mode))
	
	async def set_follow_up_mode(self, mode: Literal["all", "one-at-a-time"]) -> models.SetFollowUpModeResponse:
		
		"""发送 set_follow_up_mode 指令 (设置follow-up模式)"""
		
		return await self.request(models.SetFollowUpModeCommand(mode=mode))
	
	async def compact(self, custom_instructions: Optional[str] = None) -> models.CompactResponse:
		
		"""发送 compact 指令 (触发压缩, 可选自定义指令)"""
		
		return await self.request(models.CompactCommand(customInstructions=custom_instructions))
	
	async def set_auto_compaction(self, enabled: bool) -> models.SetAutoCompactionResponse:
		
		"""发送 set_auto_compaction 指令 (开启/关闭自动压缩)"""
		
		return await self.request(models.SetAutoCompactionCommand(enabled=enabled))
	
	async def set_auto_retry(self, enabled: bool) -> models.SetAutoRetryResponse:
		
		"""发送 set_auto_retry 指令 (开启/关闭自动重试)"""
		
		return await self.request(models.SetAutoRetryCommand(enabled=enabled))
	
	async def abort_retry(self) -> models.AbortRetryResponse:
		
		"""发送 abort_retry 指令 (中止重试)"""
		
		return await self.request(models.AbortRetryCommand())
	
	async def bash(
		self,
		command: str, *,
		exclude_from_context: Optional[bool] = None,
	) -> models.BashResponse:
		
		"""发送 bash 指令 (执行 shell 命令)"""
		
		return await self.request(models.BashCommand(command=command, excludeFromContext=exclude_from_context))
	
	async def abort_bash(self) -> models.AbortBashResponse:
		
		"""发送 abort_bash 指令 (中止 bash 执行)"""
		
		return await self.request(models.AbortBashCommand())
	
	async def get_session_stats(self) -> models.GetSessionStatsResponse:
		
		"""发送 get_session_stats 指令 (获取会话统计)"""
		
		return await self.request(models.GetSessionStatsCommand())
	
	async def export_html(self, output_path: Optional[str] = None) -> models.ExportHtmlResponse:
		
		"""发送 export_html 指令 (导出会话为 HTML)"""
		
		return await self.request(models.ExportHtmlCommand(outputPath=output_path))
	
	async def switch_session(self, session_path: str) -> models.SwitchSessionResponse:
		
		"""发送 switch_session 指令 (切换会话)"""
		
		return await self.request(models.SwitchSessionCommand(sessionPath=session_path))
	
	async def fork(self, entry_id: str) -> models.ForkResponse:
		
		"""发送 fork 指令 (从指定条目派生新会话)"""
		
		return await self.request(models.ForkCommand(entryId=entry_id))
	
	async def clone(self) -> models.CloneResponse:
		
		"""发送 clone 指令 (克隆当前会话)"""
		
		return await self.request(models.CloneCommand())
	
	async def get_fork_messages(self) -> models.GetForkMessagesResponse:
		
		"""发送 get_fork_messages 指令 (获取 fork 消息)"""
		
		return await self.request(models.GetForkMessagesCommand())
	
	async def get_entries(self, since: Optional[str] = None) -> models.GetEntriesResponse:
		
		"""发送 get_entries 指令 (获取会话条目列表)"""
		
		return await self.request(models.GetEntriesCommand(since=since))
	
	async def get_tree(self) -> models.GetTreeResponse:
		
		"""发送 get_tree 指令 (获取会话树)"""
		
		return await self.request(models.GetTreeCommand())
	
	async def get_last_assistant_text(self) -> models.GetLastAssistantTextResponse:
		
		"""发送 get_last_assistant_text 指令 (获取最后一条 assistant 文本)"""
		
		return await self.request(models.GetLastAssistantTextCommand())
	
	async def set_session_name(self, name: str) -> models.SetSessionNameResponse:
		
		"""发送 set_session_name 指令 (设置会话名称)"""
		
		return await self.request(models.SetSessionNameCommand(name=name))
	
	async def get_commands(self) -> models.GetCommandsResponse:
		
		"""发送 get_commands 指令 (获取可用命令列表)"""
		
		return await self.request(models.GetCommandsCommand())
