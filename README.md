# pi-backend

PI AGENT 的 Python 后端封装。提供进程管理、RPC 指令发送、工具调用后端等核心能力。

## 安装

```bash
pip install /path/to/pi-backend/  # easy-factory 需另行安装(本地包)
```

需要 Python >= 3.11, pydantic >= 2.13。

## 架构

```
pi_backend/
├── core/              # 核心层
│   ├── pi_process.py      # PI 子进程管理 (启动/读写/关闭)
│   ├── pi_tool_backend.py # 工具调用 socket 后端
│   └── pi_backend.py      # 高层封装 (指令发送 + 读写委托)
├── enums/             # 枚举层
│   └── command_enum.py    # CommandEnum (33 个 RPC 指令名)
├── factory/           # 模型分发
│   ├── responses_factory.py # 响应模型工厂 (33 个, 按 command 分发)
│   └── events_factory.py    # 事件模型工厂 (22 个, 按 type 分发)
├── models/            # 模型层
│   ├── rpc_events/        # RPC 指令/响应/事件模型
│   │   └── server_events/ # 响应 (responses/) + 事件 (events/)
│   ├── _tool_events/      # 私有工具调用协议模型 (python↔pi 桥接)
│   └── _internal/         # 内部辅助模型
└── __init__.py         # 顶层导出: PIProcess, PIToolBackend, PIBackend, models, CommandEnum
```

## 快速开始

### 启动 PI 进程并发送指令

```python
import asyncio
from pi_backend import PIProcess, PIBackend

async def main():
    # 构建 pi 子进程 (RPC 模式)
    proc = await PIProcess.build_process(
        session_dir = "/tmp/pi_session",
        tools      = ["bash", "read"],
        system_prompt = "你是助手",
    )
    
    backend = PIBackend(pi_process=proc)
    
    # 发送指令
    await backend.get_state()
    resp = await backend.read_raw()       # 原始字典
    print(resp)  # {"type":"response","command":"get_state","success":true,...}
    
    await backend.prompt("你好")
    model = await backend.read_pydantic() # 统一接口: 响应或事件模型
    print(type(model).__name__, model.type)
    
    # 释放资源
    await backend.pi_process.close_process()

asyncio.run(main())
```

### 工具调用后端

```python
from pi_backend import PIToolBackend

backend = PIToolBackend(host="127.0.0.1", port=39999)

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
| `build_process(pi_path, session, session_dir, tools, system_prompt)` | 构建并启动 pi 子进程 (RPC 模式) |
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

### PIBackend

| 方法 | 说明 |
|------|------|
| `read_raw()` | 读取一行 JSON 并返回原始字典 |
| `read_pydantic()` | 统一读取接口: 解析为响应或事件模型 (按 command/type 分发) |
| `write_jsonl(msg)` | 写入一行 JSON (委托 PIProcess) |
| `prompt(message, images, streaming_behavior, request_id)` | 发送 prompt 指令 |
| `set_model(provider, model_id, request_id)` | 切换模型 |
| `get_state(request_id)` | 获取当前状态 |
| `bash(command, exclude_from_context, request_id)` | 执行 shell 命令 |
| `get_commands(request_id)` | 获取可用指令列表 |
| `_send_command(command)` | 序列化并写入指令 (供内部使用) |

共 33 个指令发送方法，对应所有 RPC 指令类型。`request_id` 可选，提供后响应会回带相同 id 用于请求-响应关联。

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

`PIBackend.read_pydantic()` 即统一封装：优先匹配响应模型，非响应行回退到事件工厂——调用方拿到模型后自行决定使用或丢弃。

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