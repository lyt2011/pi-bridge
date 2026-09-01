# Step 4: connect() 工厂 + get_state()/state

## 改动内容

给 `PiClient` 增加两条:

1. **connect() 工厂** —— 一条龙装配:
   ```python
   client = await PiClient.connect(session_dir="/tmp/xxx")
   ```
   内部: `PIProcess.build_process(**kwargs)` → `PiTransport(process)` → `cls(transport)` → `start()` 起后台 reader。
   参数透传给 build_process (pi_path / session / session_dir / tools / system_prompt)。
   默认装配路径, 与 `__init__(transport)` 注入缝并存 (测试/自定义传输走后者)。

2. **get_state() / state 属性** —— 惰性状态缓存:
   - `await client.get_state()`: 发 get_state → 等响应 → 取 `data` (StateData) → 缓存到 `_state` 并返回
   - `client.state`: 同步属性, 返回上次快照 (未调用时为 None)
   - 响应缺 data 字段时抛 `RuntimeError`

## 改动的文件

| 文件 | 动作 |
|------|------|
| `src/pi_backend/core/pi_client.py` | 新增 `connect()` / `get_state()` / `state`; `__init__` 加 `_state` |
| `tests/test_pi_client.py` | 新增 4 个用例 (共 15) |

## 测试

新增 4 个用例:
- get_state 返回 StateData 并缓存到 state 属性
- state 未调用前为 None
- get_state 响应缺 data 抛 RuntimeError
- connect 工厂透传进程参数并启动 reader (monkeypatch build_process)

**验证**: 全量 `160 passed` (138 原有 + 7 传输 + 15 客户端), PIBackend 未动, 零回归

## 遗留事项

- 命令语义方法 (33 个指令封装 → 除 prompt/get_state 外全部) 待 Step 5
- 顶层导出切换 + PIBackend 兼容/弃用待 Step 6
- 异常响应形状审计 (set_session_name 等) 待独立步骤
