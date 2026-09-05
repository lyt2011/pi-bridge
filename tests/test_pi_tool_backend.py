"""PIToolBackend socket 端到端测试（真实 socket，本机回环）

覆盖范围：
1. 异步函数工具 → 1 个 tool_result 帧 + 1 个 tool_execution_end 帧
2. 异步生成器工具 → N 个 result 帧 + 1 个 end 帧
3. 并发双连接都正常
4. 随机空闲端口（绑定 0 端口取端口号）

**不依赖真实 pi 进程，独立于 pi 之外的私有协议**
"""

import asyncio
import socket

import orjson
import pytest

from pi_bridge import PIToolBackend


def _free_port() -> int:
    """获取一个随机空闲端口（绑定 0 端口取端口号后释放）"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


async def _send_tool_request(port: int, tool_name: str, tool_params: dict, tool_id: str):
    """客户端连接并发送 tool_execution 请求，收集所有响应帧直到连接关闭"""
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    req = {
        "type": "tool_execution",
        "id": tool_id,
        "tool_name": tool_name,
        "tool_params": tool_params,
    }
    writer.write(orjson.dumps(req) + b"\n")
    await writer.drain()

    frames = []
    while True:
        line = await reader.readline()
        if not line:
            break
        frames.append(orjson.loads(line))
    writer.close()
    await writer.wait_closed()
    return frames


async def _start_backend(host="127.0.0.1", port=None):
    """启动一个 PIToolBackend，返回 (backend, port)"""
    if port is None:
        port = _free_port()
    backend = PIToolBackend(host=host, port=port)
    await backend.run_server()
    return backend, backend.port


# ─── 异步函数工具 ───

@pytest.mark.asyncio
async def test_async_func_tool_returns_result_and_end():
    """异步函数工具 → 1 个 tool_result + 1 个 tool_execution_end"""
    backend, port = await _start_backend()

    async def echo(x: str) -> str:
        return f"echo:{x}"

    backend.register_tool(echo, "echo")
    try:
        frames = await _send_tool_request(port, "echo", {"x": "hello"}, "t1")
    finally:
        await backend.close_backend()

    assert len(frames) == 2
    assert frames[0]["type"] == "tool_result"
    assert frames[0]["id"] == "t1"
    assert frames[0]["result"] == "echo:hello"
    assert frames[1]["type"] == "tool_execution_end"
    assert frames[1]["id"] == "t1"


@pytest.mark.asyncio
async def test_async_func_tool_default_name():
    """register_tool 不传 name 时默认使用函数名"""
    backend, port = await _start_backend()

    async def add(a: int, b: int) -> int:
        return a + b

    backend.register_tool(add)
    try:
        frames = await _send_tool_request(port, "add", {"a": 2, "b": 3}, "t1")
    finally:
        await backend.close_backend()

    assert frames[0]["type"] == "tool_result"
    assert frames[0]["result"] == "5"
    assert frames[1]["type"] == "tool_execution_end"


# ─── 异步生成器工具 ───

@pytest.mark.asyncio
async def test_async_generator_tool_returns_n_results_and_end():
    """异步生成器工具 → N 个 result 帧 + 1 个 end 帧"""
    backend, port = await _start_backend()

    async def counter(n: int):
        for i in range(n):
            yield f"item-{i}"

    backend.register_tool(counter, "counter")
    try:
        frames = await _send_tool_request(port, "counter", {"n": 3}, "t2")
    finally:
        await backend.close_backend()

    result_frames = [f for f in frames if f["type"] == "tool_result"]
    end_frames = [f for f in frames if f["type"] == "tool_execution_end"]

    assert len(result_frames) == 3
    assert [f["result"] for f in result_frames] == ["item-0", "item-1", "item-2"]
    assert len(end_frames) == 1
    assert end_frames[0]["id"] == "t2"


@pytest.mark.asyncio
async def test_async_generator_tool_single_item():
    """单产出的生成器 → 1 个 result + 1 个 end"""
    backend, port = await _start_backend()

    async def one():
        yield "only"

    backend.register_tool(one, "one")
    try:
        frames = await _send_tool_request(port, "one", {}, "t1")
    finally:
        await backend.close_backend()

    assert len(frames) == 2
    assert frames[0]["type"] == "tool_result"
    assert frames[0]["result"] == "only"
    assert frames[1]["type"] == "tool_execution_end"


# ─── 并发双连接 ───

@pytest.mark.asyncio
async def test_concurrent_dual_connections():
    """并发双连接都正常返回结果与结束帧"""
    backend, port = await _start_backend()

    async def echo(x: str) -> str:
        return f"echo:{x}"

    async def multi(n: int):
        for i in range(n):
            yield f"m-{i}"

    backend.register_tool(echo, "echo")
    backend.register_tool(multi, "multi")
    try:
        r1, r2, r3 = await asyncio.gather(
            _send_tool_request(port, "echo", {"x": "a"}, "ta"),
            _send_tool_request(port, "echo", {"x": "b"}, "tb"),
            _send_tool_request(port, "multi", {"n": 2}, "tc"),
        )
    finally:
        await backend.close_backend()

    # 连接1：echo a
    assert [f["type"] for f in r1] == ["tool_result", "tool_execution_end"]
    assert r1[0]["result"] == "echo:a"
    # 连接2：echo b
    assert [f["type"] for f in r2] == ["tool_result", "tool_execution_end"]
    assert r2[0]["result"] == "echo:b"
    # 连接3：multi 2 项
    assert [f["type"] for f in r3] == ["tool_result", "tool_result", "tool_execution_end"]
    assert [f["result"] for f in r3 if f["type"] == "tool_result"] == ["m-0", "m-1"]


# ─── 其他行为 ───

@pytest.mark.asyncio
async def test_unknown_tool_returns_end_with_error_reason():
    """未注册的工具 → 返回 tool_execution_end（reason 含错误信息）"""
    backend, port = await _start_backend()
    try:
        frames = await _send_tool_request(port, "not_registered", {}, "t1")
    finally:
        await backend.close_backend()

    assert len(frames) == 1
    assert frames[0]["type"] == "tool_execution_end"
    assert "not_registered" in (frames[0].get("reason") or "")


@pytest.mark.asyncio
async def test_duplicate_register_raises():
    """重复注册同名工具抛 RuntimeError"""
    backend = PIToolBackend(host="127.0.0.1", port=_free_port())

    async def tool_a():
        return "a"

    async def tool_b():
        return "b"

    backend.register_tool(tool_a, "dup")
    with pytest.raises(RuntimeError):
        backend.register_tool(tool_b, "dup")
    await backend.close_backend()