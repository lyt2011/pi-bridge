# Step 1: 新建 PiTransport(传输层)

## 改动内容

新增**传输层** `PiTransport`,只做三件事:
- `send(command)`: 序列化指令模型 → 写入一行
- `recv()`: 读取一行 → 工厂校验解析 → 返回响应/事件模型
- `close()`: 委托底层 IO 的 `close_process` / `close`

**设计要点**:
- 构造接收一个**线级 IO 伙伴**(鸭子类型),只需 `read_line()` / `write_line()`,
  以及可选的 `close_process()` / `close()` —— **不引用 PIProcess**,彻底解耦
- 解析逻辑 = 复用已有工厂: 响应工厂优先, `DispatchFailed` 后回退事件工厂
  (与旧 `PIBackend.read_pydantic` 逻辑一致)
- **不负责**: 进程管理 / 后台 reader / 状态维护 —— 全部留给上层 PiClient

## 改动的文件

| 文件 | 动作 |
|------|------|
| `src/pi_backend/core/pi_transport.py` | 新增 |
| `src/pi_backend/core/__init__.py` | 导出 `PiTransport` |
| `tests/test_pi_transport.py` | 新增 7 个测试 |

## 测试

新增 `test_pi_transport.py` 7 个用例:
- send 序列化 (type 判别字段校验)
- recv 返回响应模型 / 事件模型 / 混合依次读取
- close 委托 close_process / 回退 close
- send+recv 往返

**验证**: 全量 `145 passed` (138 原有 + 7 新增), PIBackend 未动, 零回归

## 遗留事项

- 顶层 `__init__.py` 暂不导出 PiTransport (待 Step 8 统一切换)
- `PiClient` 将在 Step 2+ 组合本传输层
