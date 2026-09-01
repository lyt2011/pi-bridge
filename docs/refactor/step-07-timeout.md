# Step 7: 全局超时 set_timeout, 语义方法去掉 timeout 参数

## 背景

用户反馈: 每个语义方法都带 `timeout` 参数太啰嗦, 希望统一用 `set_timeout()` 设置实例全局超时,
方法签名保持清爽。全局超时默认不启用 (None); 如需单次覆盖, 可用 `request(cmd, timeout=...)`
或 `asyncio.wait_for(...)`。

## 改动

### `core/pi_client.py`

1. **新增 `set_timeout(timeout: Optional[float] = None) -> None`**
   - 设置实例全局请求超时 (秒); `None` = 不启用超时 (默认)
   - 之后所有 `request` (含各语义方法) 默认使用该超时

2. **`request()` 支持全局超时, 用 `timeout or self._timeout` 合并**
   ```python
   async def request(self, command, timeout: Optional[float] = None):
       timeout = timeout or self._timeout
       ...
   ```
   - `request(cmd)` → timeout 为 None → 用全局超时 (未设置则不限时)
   - `request(cmd, timeout=5)` → 本次 5 秒 (单次覆盖全局)

   > 注: 用 `or` 而非哨兵, 简洁且符合直觉。代价是全局已设置时,
   > 无法用 `timeout=None` 表达"本次不限时" (会退化为用全局);
   > 如需彻底不限时可用 `asyncio.wait_for(client.request(cmd), timeout=None)` 兜底。

3. **全部 33 个方法去掉 `timeout` 参数**: prompt / get_state / steer / follow_up / abort /
   clear_queue / new_session / get_messages / set_model / cycle_model / get_available_models /
   set_thinking_level / cycle_thinking_level / get_available_thinking_levels / set_steering_mode /
   set_follow_up_mode / compact / set_auto_compaction / set_auto_retry / abort_retry / bash /
   abort_bash / get_session_stats / export_html / switch_session / fork / clone / get_fork_messages /
   get_entries / get_tree / get_last_assistant_text / set_session_name / get_commands

### 顺手修复 (卡死元凶 + 笔误)

1. **`_set_exception_pendings` 里 `e` 未定义**: 参数名是 `exception`, 函数体却写 `fut.set_exception(e)`
   → NameError。reader 崩溃路径走到这里会抛 NameError, 导致所有未决 Future 永不 `set_exception`,
   调用方永久阻塞 —— **这就是全量测试跑 15 分钟跑不完的根因**。改为 `fut.set_exception(exception)`。

2. **`get_state` 里 `model.StateData` 笔误**: `model` 未定义, 应为 `models.StateData`;
   同时恢复了 `self._state` 缓存与 `state` 属性 (Step 4 的设计, 测试依赖)。

## 测试

- `tests/test_pi_client.py` 新增 3 个用例:
  - `test_set_timeout_global_applies_to_requests`: 全局超时生效 (不回响应 → TimeoutError)
  - `test_set_timeout_none_disables_global`: `set_timeout(None)` 关闭全局超时
  - `test_request_explicit_timeout_overrides_global`: 显式 `timeout=` 单次覆盖全局

## 验证

- 全量 pytest: **190 passed** (原 187 + 新增 3)
- 真实进程 e2e (`tests/e2e_write_translate_v2.py`): 两轮 prompt 流式跑通, 写入/翻译正常

## 用法示例

```python
client = await PiClient.connect(session_dir="/tmp/x")

# 全局 30 秒超时 (之后所有方法默认生效)
client.set_timeout(30)

# 单次覆盖: 本次 5 秒
await client.request(cmd, timeout=5)

# 单次不限时: set_timeout(None) 关闭全局, 或 asyncio.wait_for 包一层
await asyncio.wait_for(client.request(cmd), timeout=None)

# 或直接 asyncio.wait_for
await asyncio.wait_for(client.get_commands(), timeout=10)
```
