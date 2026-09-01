# Step 3: prompt() async generator 流式

## 改动内容

给 `PiClient` 增加 **prompt 流式消费**:

```python
async for evt in client.prompt("你好"):
    print(evt)
```

**工作流程**:
1. 构造 `PromptCommand` (message / images / streamingBehavior)
2. **先订阅再发指令** (避免响应到达前漏事件)
3. `request()` 发指令并等待接受响应 (走 id→Future, 不进订阅队列)
4. 接受成功 → 从订阅队列逐个 yield 事件, 遇到 `AgentSettledEvent` 结束
5. 接受被拒 (success=False) → 立即结束, 不产出事件
6. `finally` 退订

**配套基础设施强化** (本轮一并做, 支撑流式的健壮性):
- `_read_loop`: **DispatchFailed 行跳过** —— 无法解析的行 (如 `set_session_name`
  无 command 判别键的异常响应) 不视为崩溃, 继续读取
- `_read_loop` 崩溃时: 除了给所有未决 Future set_exception, 还向所有订阅者
  队列 **push 异常 sentinel** (防 prompt 永久阻塞在 `q.get()`)
- `_route`: 未匹配到未决请求的响应直接丢弃 (不误广播)
- 广播 `put_nowait` 加 `QueueFull` 保护 (订阅者消费慢时丢事件, 不炸 reader)

## 改动的文件

| 文件 | 动作 |
|------|------|
| `src/pi_backend/core/pi_client.py` | 新增 `prompt()`; 强化 `_read_loop`/`_route` |
| `tests/test_pi_client.py` | 新增 4 个 prompt 用例 |

## 测试

新增 4 个用例 (共 11 个):
- prompt 流式: 接受响应 → agent_start / message_update / agent_settled 依次 yield
- 接受被拒 (success=False) → 不产出任何事件
- reader 崩溃 → prompt 抛异常, 不永久阻塞
- settled 结束后退订, 不再收到事件

**验证**: 全量 `156 passed` (138 原有 + 7 传输 + 11 客户端), PIBackend 未动, 零回归

## 遗留事项

- connect 工厂 + 命令语义方法 (33 个指令封装) 待 Step 4/5
- PIBackend 统一兼容/弃用待 Step 6
- 异常响应形状审计 (set_session_name 等) 待独立步骤