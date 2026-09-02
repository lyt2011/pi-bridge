# pi-bridge

PI AGENT 的 Python 后端封装。提供进程管理、RPC 指令发送、工具调用后端等核心能力。

## 安装

```bash
# easy-factory 为本地依赖包, 需先安装
pip install /path/to/easy_factory/
# 再安装本包
pip install /path/to/pi-bridge/
```

需要 Python >= 3.11, pydantic >= 2.13.4。

## 架构

```
pi_backend/
├── core/              # 核心层
│   ├── pi_process.py      # PI 子进程管理 (启动/读写/关闭)
│   ├── pi_transport.py    # 传输层 (序列化 + 工厂校验, 不碰进程)
│   ├── pi_client.py       # 类型化 RPC 客户端 (后台 reader + id→Future 路由 + 事件广播)
│   ├── pi_tool_backend.py # 工具调用 socket 后端
├── enums/             # 枚举层
│   └── command_enum.py    # CommandEnum (33 个 RPC 指令名)
├── factory/           # 模型分发
│   ├── responses_factory.py # 响应模型工厂 (33 个, 按 command 分发)
│   └── events_factory.py    # 事件模型工厂 (22 个, 按 type 分发)
├── models/            # 模型层
│   ├── rpc_events/        # RPC 指令/响应/事件模型
│   │   ├── client_events/ # 指令模型 (33 个, 含 base_command 基类)
│   │   └── server_events/ # 响应 (responses/) + 事件 (events/)
│   ├── _tool_events/      # 私有工具调用协议模型 (python↔pi 桥接)
│   └── _internal/         # 内部辅助模型
├── protocols/          # 协议层
│   └── io.py              # LineProtocol: 线级 IO 协议 (鸭子类型, 供 PiTransport 注入)
└── __init__.py         # 顶层导出: PIProcess, PIToolBackend, PiClient, PiTransport, models, CommandEnum
```

## 快速开始

### 启动 PI 进程并发送指令

```python
import asyncio
from pi_backend import PiClient

async def main():
    # 一条龙: 建进程 → 建传输 → 起后台 reader
    client = await PiClient.connect(
        session_dir = "/tmp/pi_session",
        tools      = ["bash", "read"],
        system_prompt = "你是助手",
    )
    
    # 发指令 → 自动等对应响应 (id→Future 路由)
    resp = await client.get_state()
    print(resp.data)  # StateData
    
    # prompt 流式: async generator, 到 agent_settled 结束
    async for evt in client.prompt("你好"):
        print(type(evt).__name__, evt)
    
    # 事件广播订阅 (ambient 事件)
    q = client.subscribe()
    
    # 释放资源
    await client.close()

asyncio.run(main())
```

### 工具调用后端

```python
from pi_backend import PIToolBackend

backend = PIToolBackend(host="127.0.0.1", port=39999)
# 或者不传任何参数 自动从环境变量(PTBACKEND_HOST, PTBACKEND_PORT)读取 默认127.0.0.1:39999

# 注册工具
async def my_tool(param: str) -> str:
    return f"处理: {param}"

backend.register_tool(my_tool)

# 启动服务
server, task = await backend.run_server()
```

## 核心接口

### PIProcess

| 方法 | 说明 |
|------|------|
| `build_process(*, pi_path, session, session_dir, tools, system_prompt)` | 构建并启动 pi 子进程 (RPC 模式, 全部关键字传参) |
| `read_line()` | 从 stdout 读取一行 (UTF-8) |
| `write_line(*lines)` | 向 stdin 写入一行或多行 (自动补 \n) |
| `close_process()` | 关闭 stdin 并等待进程退出 |

### PIToolBackend

| 方法 | 说明 |
|------|------|
| `register_tool(func, name)` | 注册工具函数 |
| `send_result(id, result)` | 发送结果帧 |
| `send_end(id, reason)` | 发送结束帧 |
| `close_backend()` | 关闭所有连接和 socket 服务 |
| `run_server(**kwargs)` | 启动 socket 监听 |

### PiClient (推荐)

| 方法 | 说明 |
|------|------|
| `connect(**process_kwargs)` | 一条龙工厂: 建进程 → 建传输 → 起 reader |
| `request(command, timeout)` | 发指令 → id→Future 路由 → 等对应响应 |
| `set_timeout(timeout)` | 设置全局请求超时 (默认不限时, 单次可覆盖) |
| `prompt(message, images, streamingBehavior)` | async generator 流式消费事件, 到 agent_settled 结束 |
| `get_state()` / `state` 属性 | 状态快照 (惰性缓存) |
| `subscribe(maxsize)` | 事件广播订阅 (fan-out, 返回 asyncio.Queue) |
| `close()` | 取消后台 reader 并关闭传输/进程 |

指令语义方法 33 个 (prompt / steer / follow_up / set_model / get_state / bash / get_commands 等):
每个都构造命令模型 → `await request()` → 返回**具体响应模型** (含 data/success/error)。

### PiTransport (传输层)

| 方法 | 说明 |
|------|------|
| `send(command)` | 序列化指令模型并写入一行 |
| `recv()` | 读一行 → 工厂校验解析 → 响应/事件模型 |
| `close()` | 委托底层 IO 的 close_process / close |

### responses_factory / events_factory

基于 `easy_factory` 的模型分发工厂，按判别字段自动分发：

```python
from pi_backend.factory import responses_factory, events_factory

# 响应: 按 command 分发 (返回对应的 Response 模型)
model = responses_factory.dispatcher({"type":"response","command":"get_state","success":True})
# -> StateResponse 实例

# 事件: 按 type 分发 (agent_start/message_update/bash_execution_update/extension_ui_request 等)
event = events_factory.dispatcher({"type":"extension_ui_request","id":"u1","method":"setStatus"})
# -> ExtensionUIRequestEvent 实例
```

所有响应模型的 `command` 均为唯一 `Literal`，所有事件模型的 `type` 均为唯一 `Literal`，保证分发正确。未知类型抛出 `DispatchFailed`。

`PiClient.request()` 即统一封装: 自动按 id 路由到对应等待方; 事件走 fan-out 广播。

## 开发

```bash
# 安装依赖
pip install pydantic orjson easy-factory

# 测试
PYTHONPATH=src pytest
```

## 依赖

- `pydantic >= 2.13.4` — 模型定义与校验
- `orjson >= 3.10` — 高性能 JSON 解析
- `easy-factory >= 1.0.0` — 响应模型分发 (本地包, 需单独安装)