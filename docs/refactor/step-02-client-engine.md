# Step 2: 建 PiClient 核心引擎

## 改动内容

新增**客户端** `PiClient`,组合 `PiTransport`,内置三件套:

1. **后台 reader** (`_read_loop`): 常驻 drain 管道(不消费会堵死 pi 进程);
   EOF/异常时记录 `_broken`,并给所有未决 Future `set_exception`
2. **id→Future 路由** (`_route`): 响应按 `id` 找到未决 Future 并 set_result(点对点);
   非响应(事件)fan-out 广播给所有订阅者
3. **事件广播** (`subscribe`): 每人一个 `asyncio.Queue`,reader 收到事件复制给全部订阅者

对外核心方法:
- `request(command, timeout=None)`: 发指令 → 设 id → await Future → 返回响应模型
  (先查 `_broken`,已崩溃则立即抛;发指令失败时清理 pending)
- `subscribe(maxsize=0)`: 注册订阅者,返回队列
- `start()` / `close()`: 生命周期 —— 起/停后台 reader,close 关闭底层传输

## 改动的文件

| 文件 | 动作 |
|------|------|
| `src/pi_backend/core/pi_client.py` | 新增 |
| `src/pi_backend/core/__init__.py` | 导出 `PiClient` |
| `tests/test_pi_client.py` | 新增 7 个测试 |

## 测试

新增 `test_pi_client.py` 7 个用例(用可编程 FakeIO 驱动**真实**后台 reader):
- request 按 id 路由返回对应响应模型
- 并发 request 乱序回响应,各拿各的
- 事件 fan-out: 两个订阅者各收到副本
- 响应不进广播(只进 Future)
- reader 崩溃 → 未决 Future 全部 set_exception
- 崩溃后新 request 立即抛 _broken
- close 取消 reader + 关闭底层 IO

**验证**: 全量 `152 passed` (138 原有 + 7 传输 + 7 客户端), PIBackend 未动, 零回归

## 遗留事项

- prompt 流式(async generator)待 Step 5
- connect 工厂 + 命令语义方法(33 个指令封装)待 Step 6/7
- PIBackend 统一兼容/弃用待 Step 8