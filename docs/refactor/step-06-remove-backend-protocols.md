# Step 6: 删除 PIBackend + 新建 protocols/ 包

## 改动内容

### 1. 删除 PIBackend (已被 PiClient 完全取代)

- 删除 `core/pi_backend.py` (薄传输层旧实现, 33 个纯发送方法 + read_raw/read_pydantic)
- 清理两个 `__init__.py` 的导入与 `__all__` 导出
- 删除 `tests/test_pi_backend.py` (其覆盖已由 `test_pi_transport.py` 取代)
- 删除 `tests/e2e_write_translate.py` (v1 用 follow_up, 有已知队列问题, 与 v2 重复)
- 迁移 `tests/e2e_write_translate_v2.py` 到 PiClient (用 prompt 流式, 保留真实进程端到端验证)
- README: 移除全部 PIBackend 兼容段落与导出说明

### 2. 新建 protocols/ 包 + io 类型注解

- 新建 `protocols/io.py`: 定义 `LineProtocol` 协议 (鸭子类型, 供 PiTransport 注入缝)
  - `read_line() -> str` / `write_line(*lines) -> None` (必须)
  - close 可选: 先尝试 `close_process()`, 回退 `close()`
- `pi_transport.py`: `__init__(self, io: LineProtocol)` 加上类型注解 (原来裸 `io`)
- `pi_client.py`: 把 30 行 `from ..models import (...)` 改为 `from .. import models`, 全文件用 `models.XXX` 属性访问

## 改动的文件

| 文件 | 动作 |
|------|------|
| `src/pi_backend/core/pi_backend.py` | 删除 |
| `src/pi_backend/core/__init__.py` | 移除 PIBackend 导出 |
| `src/pi_backend/__init__.py` | 移除 PIBackend 导出 |
| `src/pi_backend/protocols/__init__.py` | 新增 (导出 LineProtocol) |
| `src/pi_backend/protocols/io.py` | 新增 (LineProtocol 协议) |
| `src/pi_backend/core/pi_transport.py` | io 参数加 `LineProtocol` 注解 |
| `src/pi_backend/core/pi_client.py` | 导入改为 `from .. import models` + `models.XXX` 访问 |
| `tests/test_pi_backend.py` | 删除 (覆盖已转移) |
| `tests/e2e_write_translate.py` | 删除 (v1, follow_up 队列问题) |
| `tests/e2e_write_translate_v2.py` | 迁移到 PiClient |
| `README.md` | 移除 PIBackend, 加 protocols/ |

## 测试

**验证**: 全量 `187 passed` (192 - 5 删除的 test_pi_backend 用例), 零回归。
顶层导出: `['PIProcess', 'PIToolBackend', 'PiClient', 'PiTransport', 'models', 'CommandEnum']`
源码内 `grep PIBackend` 无残留 (仅旧 __pycache__ 字节码, 已清理)。

## 遗留事项

- miaoli_bot 插件接入可等重构完成后进行
- 真实进程响应形状审计 (set_session_name 等) 仍待独立步骤
- 尚未 git commit (Field 化改造 93 文件 + 重构各步成果均未提交)