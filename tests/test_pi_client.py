"""PiClient 核心引擎测试

覆盖: request id→Future 路由 / 并发请求各拿各的 / 事件 fan-out 广播 /
reader 崩溃传播 / close 生命周期
用可注入 FakeIO 驱动真实后台 reader, 不启动真实进程
"""

import json
import orjson
import pytest

from pi_bridge.core.pi_client		import PiClient
from pi_bridge.core.pi_process		import PIProcess
from pi_bridge.core.pi_transport	import PiTransport
from pi_bridge.models				import GetStateCommand, SetModelCommand
from pi_bridge.models				import StateResponse, MessageUpdateEvent, AgentStartEvent
from pi_bridge.models				import AgentEndEvent
from pi_bridge					import BaseError, RequestRefuseError

import asyncio


class FakeIO:
    """可编程的线级 IO: 测试往 _inbox 里塞行, reader 依次消费"""

    def __init__(self):
        self._inbox			= asyncio.Queue()
        self.written		= []
        self.fail			= None		# 若设置, read_line 抛此异常
        self.closed			= False

    async def read_line(self) -> str:
        line = await self._inbox.get()
        if self.fail is not None:
            raise self.fail
        return line

    async def write_line(self, *lines: str) -> None:
        self.written.extend(lines)

    async def close_process(self) -> None:
        self.closed = True

    # ---- 测试辅助 ----

    def last_written(self) -> dict:
        return json.loads(self.written[-1])

    def push(self, data: dict) -> None:
        self._inbox.put_nowait(orjson.dumps(data).decode("utf-8"))


def make_response_line(command, rid=None, success=True):
    return {"type": "response", "command": command, "success": success, "id": rid}


async def make_client() -> tuple[PiClient, FakeIO]:
    io = FakeIO()
    transport = PiTransport(io)
    client = PiClient(transport)
    await client.start()
    return client, io


@pytest.mark.asyncio
async def test_request_returns_matching_response():
    """request: 按 id 路由, 返回对应响应模型"""
    client, io = await make_client()

    task = asyncio.create_task(client.request(GetStateCommand()))
    await asyncio.sleep(0)			# 让 request 先把命令发出去

    rid = io.last_written()["id"]
    io.push(make_response_line("get_state", rid=rid))

    resp = await task
    assert isinstance(resp, StateResponse)
    assert resp.id == rid


@pytest.mark.asyncio
async def test_concurrent_requests_each_get_own_response():
    """并发 request: 各自拿到自己的响应, 不乱分配"""
    client, io = await make_client()

    t1 = asyncio.create_task(client.request(GetStateCommand()))
    await asyncio.sleep(0)
    rid1 = io.last_written()["id"]

    t2 = asyncio.create_task(client.request(SetModelCommand(provider="ceroxe", modelId="deepseek-v4-flash")))
    await asyncio.sleep(0)
    rid2 = io.last_written()["id"]

    # 故意乱序回响应
    io.push(make_response_line("set_model", rid=rid2))
    io.push(make_response_line("get_state", rid=rid1))

    r1, r2 = await asyncio.gather(t1, t2)
    assert r1.id == rid1
    assert r2.id == rid2


@pytest.mark.asyncio
async def test_events_broadcast_to_all_subscribers():
    """事件 fan-out: 每个订阅者都收到一份副本"""
    client, io = await make_client()

    q1 = client.subscribe()
    q2 = client.subscribe()

    io.push({"type": "agent_start"})
    io.push({"type": "message_update"})

    e1 = await asyncio.wait_for(q1.get(), timeout=1)
    e1b = await asyncio.wait_for(q1.get(), timeout=1)
    e2 = await asyncio.wait_for(q2.get(), timeout=1)

    assert isinstance(e1, AgentStartEvent)
    assert isinstance(e1b, MessageUpdateEvent)
    assert isinstance(e2, AgentStartEvent)


@pytest.mark.asyncio
async def test_receive_events_filters_single_type():
    """receive_events: 单类型只 yield 匹配的事件对象"""
    client, io = await make_client()
    stream = client.receive_events(MessageUpdateEvent)

    task = asyncio.create_task(anext(stream))
    await asyncio.sleep(0)
    io.push({"type": "agent_start"})
    io.push({"type": "message_update"})

    event = await asyncio.wait_for(task, timeout=1)
    assert isinstance(event, MessageUpdateEvent)
    await stream.aclose()


@pytest.mark.asyncio
async def test_receive_events_filters_multiple_types():
    """receive_events: 多类型 yield 任一匹配的事件对象"""
    client, io = await make_client()
    stream = client.receive_events(AgentStartEvent, MessageUpdateEvent)

    first = asyncio.create_task(anext(stream))
    await asyncio.sleep(0)
    io.push({"type": "agent_start"})
    assert isinstance(await asyncio.wait_for(first, timeout=1), AgentStartEvent)

    second = asyncio.create_task(anext(stream))
    io.push({"type": "message_update"})
    assert isinstance(await asyncio.wait_for(second, timeout=1), MessageUpdateEvent)
    await stream.aclose()


@pytest.mark.asyncio
async def test_receive_events_skips_non_matching_events():
    """receive_events: 不匹配事件被消费但不 yield"""
    client, io = await make_client()
    stream = client.receive_events(MessageUpdateEvent)

    task = asyncio.create_task(anext(stream))
    await asyncio.sleep(0)
    io.push({"type": "agent_start"})

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(asyncio.shield(task), timeout=0.05)

    io.push({"type": "message_update"})
    assert isinstance(await asyncio.wait_for(task, timeout=1), MessageUpdateEvent)
    await stream.aclose()


@pytest.mark.asyncio
async def test_receive_events_without_types_yields_all_events():
    """receive_events: 零参数表示接收全部事件"""
    client, io = await make_client()
    stream = client.receive_events()

    first = asyncio.create_task(anext(stream))
    await asyncio.sleep(0)
    io.push({"type": "agent_end"})
    assert isinstance(await asyncio.wait_for(first, timeout=1), AgentEndEvent)

    second = asyncio.create_task(anext(stream))
    io.push({"type": "message_update"})
    assert isinstance(await asyncio.wait_for(second, timeout=1), MessageUpdateEvent)
    await stream.aclose()


@pytest.mark.asyncio
async def test_responses_not_broadcast_to_subscribers():
    """响应不进广播: 订阅者队列只收到事件, 不收到响应"""
    client, io = await make_client()

    q = client.subscribe()

    task = asyncio.create_task(client.request(GetStateCommand()))
    await asyncio.sleep(0)
    rid = io.last_written()["id"]
    io.push(make_response_line("get_state", rid=rid))
    resp = await task
    assert isinstance(resp, StateResponse)

    # 响应被路由走了, 订阅者队列应为空
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(q.get(), timeout=0.1)


@pytest.mark.asyncio
async def test_reader_crash_propagates_to_pending():
    """reader 崩溃: 未决 Future 全部 set_exception 唤醒"""
    client, io = await make_client()

    task = asyncio.create_task(client.request(GetStateCommand()))
    await asyncio.sleep(0)

    io.fail = ConnectionError("pipe broken")
    io.push({})					# 触发一次 recv, 让 reader 撞上 fail

    with pytest.raises(ConnectionError):
        await task


@pytest.mark.asyncio
async def test_request_after_crash_raises_immediately():
    """崩溃发生后: 新 request 立即抛 _broken, 不再发指令"""
    client, io = await make_client()

    io.fail = RuntimeError("boom")
    io.push({})
    await asyncio.sleep(0)			# reader 撞上 fail 并记录 _broken
    await asyncio.sleep(0)

    with pytest.raises(RuntimeError):
        await client.request(GetStateCommand())


@pytest.mark.asyncio
async def test_close_cancels_reader_and_closes_transport():
    """close: 取消后台 reader, 关闭底层传输"""
    client, io = await make_client()
    await client.close()
    assert io.closed


async def collect_prompt(client, message, **kw):
    """把 prompt async generator 收集成事件列表"""
    events = []
    async for evt in client.prompt(message, **kw):
        events.append(evt)
    return events


async def fake_open(client_factory=None, io=None) -> tuple[PiClient, FakeIO]:
    """模拟 open 的装配路径: 返回已 start 的 client + FakeIO"""
    io = io or FakeIO()
    transport = PiTransport(io)
    client = PiClient(transport)
    await client.start()
    return client, io


@pytest.mark.asyncio
async def test_set_timeout_global_applies_to_requests():
    """set_timeout: 设置实例全局超时, request 未显式传 timeout 时生效"""
    client, io = await make_client()

    client.set_timeout(0.05)

    # 不回响应: 全局超时应在 50ms 后触发 TimeoutError
    task = asyncio.create_task(client.request(GetStateCommand()))
    await asyncio.sleep(0)

    with pytest.raises(asyncio.TimeoutError):
        await task


@pytest.mark.asyncio
async def test_set_timeout_none_disables_global():
    """set_timeout(None): 关闭全局超时 (默认不限时)"""
    client, io = await make_client()

    client.set_timeout(0.05)
    client.set_timeout(None)

    task = asyncio.create_task(client.request(GetStateCommand()))
    await asyncio.sleep(0)

    rid = io.last_written()["id"]
    io.push(make_response_line("get_state", rid=rid))

    resp = await task
    assert isinstance(resp, StateResponse)


@pytest.mark.asyncio
async def test_request_explicit_timeout_overrides_global():
    """request: 显式传 timeout 覆盖全局设置 (单次覆盖)"""
    client, io = await make_client()

    client.set_timeout(1.0)  # 全局 1 秒

    # 单次覆盖为 0.05 秒, 不回响应 → 应快速超时
    task = asyncio.create_task(client.request(GetStateCommand(), timeout=0.05))
    await asyncio.sleep(0)

    with pytest.raises(asyncio.TimeoutError):
        await task


@pytest.mark.asyncio
async def test_get_state_caches_state_property():
    """get_state: 发送指令, 返回 StateData 并缓存到 state 属性"""
    client, io = await fake_open()

    task = asyncio.create_task(client.get_state())
    await asyncio.sleep(0)

    rid = io.last_written()["id"]
    assert io.last_written()["type"] == "get_state"

    io.push({
        "type": "response", "command": "get_state", "success": True,
        "id": rid, "data": {"messageCount": 3},
    })

    state = await task
    assert state.messageCount == 3
    assert client.state.messageCount == 3


@pytest.mark.asyncio
async def test_state_none_before_get_state():
    """state 属性: 未调用 get_state 前为 None"""
    client, io = await fake_open()
    assert client.state is None


@pytest.mark.asyncio
async def test_get_state_missing_data_raises():
    """get_state: 响应缺 data 时抛 RuntimeError"""
    client, io = await fake_open()

    task = asyncio.create_task(client.get_state())
    await asyncio.sleep(0)
    rid = io.last_written()["id"]
    io.push({"type": "response", "command": "get_state", "success": True, "id": rid})

    with pytest.raises(RuntimeError):
        await task


@pytest.mark.asyncio
async def test_open_factory_with_fake_process(monkeypatch):
    """open: 工厂透传进程参数, 构建 client 并启动 reader"""
    io = FakeIO()

    class FakeProcess:
        def __init__(self):
            self.read_line = io.read_line
            self.write_line = io.write_line
            self.close_process = io.close_process

    async def fake_build(**kwargs):
        assert kwargs["session_dir"] == "/tmp/fake"
        return FakeProcess()

    monkeypatch.setattr(PIProcess, "build", fake_build)

    client = await PiClient.open(session_dir="/tmp/fake")
    assert isinstance(client._transport._io, FakeProcess)
    assert client._reader is not None

    await client.close()
    assert io.closed


@pytest.mark.asyncio
async def test_prompt_streams_events_until_settled():
    """prompt: 接受成功后依次 yield 事件, 到 AgentSettledEvent 结束"""
    client, io = await make_client()

    task = asyncio.create_task(collect_prompt(client, "你好"))
    await asyncio.sleep(0)			# 让 prompt 订阅并发出指令

    rid = io.last_written()["id"]
    assert io.last_written()["type"] == "prompt"

    # 先回接受响应 (响应走 Future, 不进订阅队列)
    io.push(make_response_line("prompt", rid=rid))
    await asyncio.sleep(0)

    # 再推事件流
    io.push({"type": "agent_start"})
    io.push({"type": "message_update"})
    io.push({"type": "agent_settled"})

    events = await task
    assert [type(e).__name__ for e in events] == [
        "AgentStartEvent", "MessageUpdateEvent", "AgentSettledEvent",
    ]


@pytest.mark.asyncio
async def test_prompt_rejected_raises_request_refuse_error():
    """prompt: 接受被拒 (success=False) 时抛出 RequestRefuseError, 响应本体与原因可回查"""
    client, io = await make_client()

    task = asyncio.create_task(collect_prompt(client, "你好"))
    await asyncio.sleep(0)

    rid = io.last_written()["id"]
    io.push({**make_response_line("prompt", rid=rid, success=False), "error": "pi 正忙"})

    with pytest.raises(RequestRefuseError) as exc_info:
        await task

    err = exc_info.value
    assert isinstance(err, BaseError)            # 可从包根捕获到基类
    assert err.response.id == rid                # 响应本体可回查
    assert err.response.error == "pi 正忙"
    assert "pi 正忙" in str(err)                 # 原因要出现在日志可见处

    # 被拒不依赖异常路径收尾: 订阅者仍会被注销
    assert client._subscribers == []

    await client.close()


@pytest.mark.asyncio
async def test_prompt_rejected_without_error_field_yields_nothing():
    """prompt: 拒绝响应缺 error 字段时消息为空串, 但响应本体仍可回查; 迭代器零产出"""
    client, io = await make_client()

    events = []

    async def consume():
        async for evt in client.prompt("你好"):
            events.append(evt)

    task = asyncio.create_task(consume())
    await asyncio.sleep(0)

    rid = io.last_written()["id"]
    io.push(make_response_line("prompt", rid=rid, success=False))

    with pytest.raises(RequestRefuseError) as exc_info:
        await task

    assert str(exc_info.value) == ""
    assert exc_info.value.response.success is False
    assert exc_info.value.response.id == rid
    assert events == []

    await client.close()


@pytest.mark.asyncio
async def test_prompt_propagates_reader_crash():
    """prompt: reader 崩溃时抛崩溃异常, 不会永久阻塞"""
    client, io = await make_client()

    task = asyncio.create_task(collect_prompt(client, "你好"))
    await asyncio.sleep(0)

    rid = io.last_written()["id"]
    io.push(make_response_line("prompt", rid=rid))
    await asyncio.sleep(0)

    io.fail = ConnectionError("pipe broken")
    io.push({})

    with pytest.raises(ConnectionError):
        await task


@pytest.mark.asyncio
async def test_prompt_unsubscribes_after_settled():
    """prompt: settled 结束后退订, 不再收到事件"""
    client, io = await make_client()

    # 一个旁路订阅者 (用于观察退订后事件不再分发到 prompt)
    other = client.subscribe()

    task = asyncio.create_task(collect_prompt(client, "你好"))
    await asyncio.sleep(0)
    rid = io.last_written()["id"]

    io.push(make_response_line("prompt", rid=rid))
    io.push({"type": "agent_settled"})
    await task

    assert client._subscribers == [other]

    # 退订后事件不再进 prompt 的旧队列 (旧队列已移除)
    assert len(client._subscribers) == 1

    await client.close()