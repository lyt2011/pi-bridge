# pi-backend

PI AGENT 的 Python 后端封装。提供进程管理、RPC 指令发送、工具调用后端等核心能力。

## 安装

```bash
pip install /path/to/pi-backend/
```

需要 Python >= 3.11, pydantic >= 2.13。

## 架构

```
pi_backend/
├── core/              # 核心层
│   ├── pi_process.py      # PI 子进程管理 (启动/读写/关闭)
│   ├── pi_tool_backend.py # 工具调用 socket 后端
│   └── pi_backend.py      # 高层封装 (指令发送 + 读写委托)
├── models/            # 模型层
│   ├── rpc_events/        # RPC 指令/响应模型 (33 个 command + 33 个 response)
│   ├── tool_events/       # 工具调用协议模型
│   └── _internal/         # 内部辅助模型
└── __init__.py         # 顶层导出: PIProcess, PIToolBackend, PIBackend, models
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
    resp = await backend.read_jsonl()
    print(resp)  # {"type":"response","command":"get_state","success":true,...}
    
    await backend.prompt("你好")
    prompt_resp = await backend.read_jsonl()
    print(prompt_resp)
    
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
| `read_jsonl()` | 读取一行并解析为 dict |
| `write_jsonl(msg)` | 写入一行 JSON (委托 PIProcess) |
| `prompt(message, images, streaming_behavior, request_id)` | 发送 prompt 指令 |
| `set_model(provider, model_id, request_id)` | 切换模型 |
| `get_state(request_id)` | 获取当前状态 |
| `bash(command, exclude_from_context, request_id)` | 执行 shell 命令 |
| `get_commands(request_id)` | 获取可用指令列表 |
| `_send_command(command)` | 序列化并写入指令 (供内部使用) |

共 33 个指令发送方法，对应所有 RPC 指令类型。`request_id` 可选，提供后响应会回带相同 id 用于请求-响应关联。

## 开发

```bash
# 安装依赖
pip install pydantic orjson

# 测试
PYTHONPATH=src pytest
```

## 依赖

- `pydantic >= 2.13.4` — 模型定义与校验
- `orjson >= 3.10` — 高性能 JSON 解析