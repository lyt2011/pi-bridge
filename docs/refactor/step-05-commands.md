# Step 5: 33 个命令语义方法封装

## 改动内容

给 `PiClient` 补全全部 33 个指令方法 (prompt/get_state 在 Step 3/4 已实现, 本轮补其余 31 个)。

**统一形态**: 每个方法 = 构造命令模型 → `await request()` → 返回**具体响应模型**

```python
client = await PiClient.connect(session_dir="/tmp/x")
resp = await client.set_model("seed_api", "deepseek-v4-flash")
print(resp.data)          # SetModelResponse.data
```

**与旧 PIBackend 的本质区别**:
- PIBackend 全部方法返回 `None` (纯发送, 调用方自己循环 read_pydantic 匹配)
- PiClient 每个方法按 id 路由自动等对应响应, 返回类型化响应模型 (含 data/success/error)

**31 个新方法清单** (均带可选 `timeout`):
steer / follow_up / abort / clear_queue / new_session / get_messages /
set_model / cycle_model / get_available_models / set_thinking_level /
cycle_thinking_level / get_available_thinking_levels / set_steering_mode /
set_follow_up_mode / compact / set_auto_compaction / set_auto_retry /
abort_retry / bash / abort_bash / get_session_stats / export_html /
switch_session / fork / clone / get_fork_messages / get_entries / get_tree /
get_last_assistant_text / set_session_name / get_commands

## 改动的文件

| 文件 | 动作 |
|------|------|
| `src/pi_bridge/core/pi_client.py` | 新增 31 个语义方法 + 扩充模型导入 |
| `tests/test_pi_client_commands.py` | 新增 32 个用例 (表驱动) |

## 测试

新增 `test_pi_client_commands.py`:
- 表驱动 31 个方法: 发出正确 type 指令 + 收到对应响应模型 (31 个)
- 多方法复用同一 client/reader, 乱序回响应各拿各的 (1 个)

**验证**: 全量 `192 passed` (138 原有 + 7 传输 + 15 客户端 + 32 命令), PIBackend 未动, 零回归

## 遗留事项

- 顶层导出切换 + PIBackend 兼容/弃用待 Step 6
- 异常响应形状审计 (set_session_name 等) 待独立步骤