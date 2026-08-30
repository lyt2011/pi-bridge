"""PIBackend read_pydantic 统一接口测试

覆盖范围：
用伪造的 PIProcess 注入 PIBackend（PIBackend 构造参数是 `pi_process`），
伪造 read_line 依次返回 response 行和事件行，断言 read_pydantic 分别返回
响应模型和事件模型。**不启动真实 pi 进程**。
"""

import orjson
import pytest

from pi_backend import PIBackend
from pi_backend.models import StateResponse, SetModelResponse, AgentStartEvent, MessageUpdateEvent


class FakePIProcess:
    """伪造的 PIProcess：按顺序返回预先定义的行"""

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


@pytest.mark.asyncio
async def test_read_raw_returns_dict():
    """read_raw 返回 orjson.loads 后的 dict"""
    line = orjson.dumps({"type": "response", "command": "get_state", "success": True}).decode("utf-8")
    fake = FakePIProcess([line])
    backend = PIBackend(pi_process=fake)
    data = await backend.read_raw()
    assert isinstance(data, dict)
    assert data["command"] == "get_state"
    assert data["success"] is True


@pytest.mark.asyncio
async def test_read_pydantic_returns_response_model():
    """read_pydantic 对 response 行返回响应模型"""
    line = orjson.dumps({"type": "response", "command": "get_state", "success": True}).decode("utf-8")
    fake = FakePIProcess([line])
    backend = PIBackend(pi_process=fake)
    model = await backend.read_pydantic()
    assert isinstance(model, StateResponse)
    assert model.command.value == "get_state"


@pytest.mark.asyncio
async def test_read_pydantic_returns_event_model():
    """read_pydantic 对事件行返回事件模型（响应工厂 DispatchFailed 后回退事件工厂）"""
    line = orjson.dumps({"type": "agent_start"}).decode("utf-8")
    fake = FakePIProcess([line])
    backend = PIBackend(pi_process=fake)
    model = await backend.read_pydantic()
    assert isinstance(model, AgentStartEvent)


@pytest.mark.asyncio
async def test_read_pydantic_returns_response_then_event():
    """伪造 read_line 依次返回 response 行和事件行，read_pydantic 分别返回对应模型"""
    resp_line = orjson.dumps({"type": "response", "command": "set_model", "success": True}).decode("utf-8")
    event_line = orjson.dumps({"type": "message_update"}).decode("utf-8")
    fake = FakePIProcess([resp_line, event_line])
    backend = PIBackend(pi_process=fake)

    first = await backend.read_pydantic()
    assert isinstance(first, SetModelResponse)

    second = await backend.read_pydantic()
    assert isinstance(second, MessageUpdateEvent)


@pytest.mark.asyncio
async def test_write_jsonl_rejects_non_str():
    """write_jsonl 对非 str 输入抛 TypeError"""
    fake = FakePIProcess([])
    backend = PIBackend(pi_process=fake)
    with pytest.raises(TypeError):
        await backend.write_jsonl({"not": "str"})