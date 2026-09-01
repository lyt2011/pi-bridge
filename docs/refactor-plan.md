# pi_backend → PiClient 重构总计划

> 目标: 把当前"HTTP 服务器式"的薄转发层(PIBackend), 重构成
> "持有状态 + 自动路由 + 暴露事件流" 的 **PiClient**。
> 分步实施, 每步小改动, 每步全绿, 每步写独立 markdown 文档。

---

## 现状诊断

| 问题 | 现状 |
|------|------|
| 定位 | `PIBackend` 是纯 write-only 薄封装: 33 个方法全是"发指令不管响应" |
| 响应归属 | 调用方自己 `read_pydantic()` 循环读, 手动匹配是哪条响应 |
| 状态 | 无任何状态快照, 每次 get_state 都从零开始 |
| 事件 | 无流式消费, 调用方手工拼 `while` 循环 |
| 生命周期 | reader/进程管理散落在调用方 |

## 目标架构(讨论定稿)

```
PiClient                ← 唯一公开类: 协议 + 校验 + 业务方法 + connect 工厂
  ├── request(cmd)      ← id→Future 路由: 发指令 → await 对应响应 (点对点)
  ├── prompt(msg)       ← async generator: 事件流式消费 (fan-out 订阅者之一)
  ├── get_state()       ← 语义方法: 发 get_state → 等响应 → 缓存 state 属性
  ├── state             ← 属性: 上次 get_state 的缓存 (无后台状态维护)
  ├── subscribe()       ← 事件广播: 订阅者各有一个 asyncio.Queue
  ├── connect(...)      ← 工厂: 一条龙 建进程→建传输→建 client→起 reader
  ├── close()           ← 生命周期收尾
  └── 内部: _read_loop 后台 reader (15行, 集中错误处理)
        ↓
PiTransport             ← 传输层: send/recv/close, 序列化+工厂校验
        ↑ 注入 line-IO 伙伴 (鸭子类型, 不引用 PIProcess)
PIProcess               ← 进程管理: read_line/write_line/生命周期, 不懂协议
```

### 核心设计决策(讨论记录)

| 决策 | 结论 | 理由 |
|------|------|------|
| 响应路由 | `Dict[request_id, Future]`, reader 按 id set_result | 一对一、带值、单次; Event 语义对不上 |
| 事件分发 | **fan-out 广播**: reader 把每个事件复制给所有订阅者队列 | pi 事件是混合流(turn + ambient), 单消费者会饿死别人 |
| prompt | async generator, 发命令 → 从订阅队列拿事件 yield → settled 停 | `async for evt in client.prompt(...)` |
| 后台 reader | `asyncio.create_task` 常驻, 无条件 drain | 管道不消费会堵死 pi 进程; 崩溃集中 set_exception |
| 生命周期 | 在 PiClient (connect 起 / close 停), 不进传输层 | 传输层保持薄 |
| 状态 | 仅 `state` 属性(惰性缓存), 不维护 is_running 等 | 调用方按需拉取 |
| 继承点 | `_send_command` / `_route` 用 protected, 可重写做校验 | 使用者继承加校验 |

## 分步计划

| 步 | 内容 | 产物 | 验证 |
|----|------|------|------|
| 1 | 建 `PiTransport`(传输层): send/recv/close + 工厂校验, 从 PIBackend 提取, PIBackend 不动 | `core/pi_transport.py` + 测试 | 138 全绿 + 新测试 |
| 2 | 建 `PiClient` 骨架: 组合 transport + 后台 reader + `_route` | `core/pi_client.py` + 测试 | 138 + 新测试 |
| 3 | `request(cmd)` id→Future 路由 + 崩溃传播 | 同上 | 测试: 并发 request 各拿各的 |
| 4 | `subscribe()` 事件广播 (fan-out) | 同上 | 测试: 多订阅者各拿一份 |
| 5 | `prompt()` async generator 流式 | 同上 | 测试: 流式消费到 settled |
| 6 | `connect()` 工厂 + `close()` 生命周期 | 同上 | 测试: 生命周期 |
| 7 | 语义方法 `get_state()`/`state` 属性 + 其余指令封装 | 同上 | 测试 |
| 8 | 顶层导出切换: `__init__.py` 导出 PiClient, PIBackend 保留兼容 | `__init__.py` + README | 138 全绿 |
| 9 | (可选) PIBackend 标记 deprecated / 迁移测试 | 文档 | 全绿 |

## 编码规范(必须与项目一致)

- 缩进一律 **tab**
- import 分组: stdlib / 三方 / 本地, 组间空行, `from x\timport y` tab 对齐
- docstring 用 `"""..."""` 中文
- 类/方法间空行风格跟随现有文件 (pi_process.py 为参照)
- 模型/工厂层 **不动**
- `PIToolBackend`(独立 socket 服务)**不动**

## 文档约定

每步完成写 `docs/refactor/step-N-<名称>.md`:
- 改动内容 / 改了什么文件 / 新增了什么测试 / 验证结果 / 遗留事项
