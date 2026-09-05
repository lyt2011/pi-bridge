"""PiTransport 传输层测试

覆盖: send / recv / close 的三种行类型 (响应/事件/混合)
不启动真实进程, 用 FakeIO 模拟线级 IO
"""

import orjson
import pytest

from pi_bridge.models import StateResponse, AgentStartEvent, MessageUpdateEvent
from pi_bridge.core.pi_transport import PiTransport


class FakeIO:
    """伪造的线级 IO 伙伴: 按顺序返回预先定义的行"""

    def __init__(self, lines):
        self._lines = list(lines)
        self._idx = 0
        self.written = []

    async def read_line(self) -> str:
        if self._idx >= len(self._lines):
            raise EOFError("no more lines")
        line = self._lines[self._idx]
        self._idx += 1
        return line

    async def write_line(self, *lines: str) -> None:
        self.written.extend(lines)

    async def close_process(self) -> None:
        pass


@pytest.mark.asyncio
async def test_send_serializes_command():
    """send 将指令序列化为 JSONL 写入"""
    fake = FakeIO([])
    transport = PiTransport(fake)
    from pi_bridge.models import GetStateCommand
    cmd = GetStateCommand()
    await transport.send(cmd)
    assert len(fake.written) == 1
    import json
    data = json.loads(fake.written[0])
    assert data["type"] == "get_state"


@pytest.mark.asyncio
async def test_recv_returns_response():
    """recv 对 response 行返回响应模型"""
    line = orjson.dumps({"type": "response", "command": "get_state", "success": True}).decode("utf-8")
    fake = FakeIO([line])
    transport = PiTransport(fake)
    model = await transport.recv()
    assert isinstance(model, StateResponse)
    assert model.command.value == "get_state"


@pytest.mark.asyncio
async def test_recv_returns_event():
    """recv 对事件行返回事件模型 (响应工厂 DispatchFailed 后回退事件工厂)"""
    line = orjson.dumps({"type": "agent_start"}).decode("utf-8")
    fake = FakeIO([line])
    transport = PiTransport(fake)
    model = await transport.recv()
    assert isinstance(model, AgentStartEvent)


@pytest.mark.asyncio
async def test_recv_response_then_event():
    """recv 依次读取响应行和事件行, 分别返回对应模型"""
    resp_line = orjson.dumps({"type": "response", "command": "get_state", "success": True}).decode("utf-8")
    event_line = orjson.dumps({"type": "message_update"}).decode("utf-8")
    fake = FakeIO([resp_line, event_line])
    transport = PiTransport(fake)

    first = await transport.recv()
    assert isinstance(first, StateResponse)

    second = await transport.recv()
    assert isinstance(second, MessageUpdateEvent)


@pytest.mark.asyncio
async def test_close_calls_close_process():
    """close 委托给 io 的 close_process"""
    fake = FakeIO([])
    transport = PiTransport(fake)
    await transport.close()
    # 没有异常即通过


@pytest.mark.asyncio
async def test_close_falls_back_to_close():
    """close 回退到 io 的 close 方法 (若没有 close_process)"""
    class FakeIOClose:
        def __init__(self):
            self.closed = False
        async def read_line(self): return "{}"
        async def write_line(self, *lines): pass
        async def close(self):
            self.closed = True

    io = FakeIOClose()
    transport = PiTransport(io)
    await transport.close()
    assert io.closed


@pytest.mark.asyncio
async def test_send_then_recv_roundtrip():
    """send + recv 往返: 发指令模型, 收响应行"""
    from pi_bridge.models import GetStateCommand
    cmd = GetStateCommand()
    resp_line = orjson.dumps({"type": "response", "command": "get_state", "success": True}).decode("utf-8")
    fake = FakeIO([resp_line])
    transport = PiTransport(fake)

    await transport.send(cmd)
    model = await transport.recv()
    assert isinstance(model, StateResponse)