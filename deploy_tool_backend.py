"""部署 pi 私有工具后端 (PIToolBackend @ 127.0.0.1:39999)

配合 pi 扩展 pi-tool-backend.ts 使用：
扩展把 pi 的工具调用通过私有协议转发到这里，本后端注册同名工具 backend_echo 真正执行。

用法：
    PYTHONPATH=src python deploy_tool_backend.py

说明：
    - 监听 127.0.0.1:39999
    - 注册工具 backend_echo(message: str) -> str   （与扩展注册的工具名/参数一致）
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from pi_bridge import PIToolBackend  # noqa: E402

HOST = "127.0.0.1"
PORT = 39999


async def backend_echo(message: str) -> str:
    """回显输入消息"""
    return f"echo: {message}"


async def main() -> None:
    backend = PIToolBackend(host=HOST, port=PORT)
    backend.register_tool(backend_echo, "backend_echo")

    server, task = await backend.run_server()
    print(f"PIToolBackend 已启动: {HOST}:{PORT}  注册工具: backend_echo", flush=True)

    try:
        # 保持服务运行直到被终止
        await asyncio.Event().wait()
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        await backend.close_backend()
        print("PIToolBackend 已关闭", flush=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("收到 Ctrl+C，退出", flush=True)
