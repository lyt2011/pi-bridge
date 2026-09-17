# Changelog

本项目的所有重要变更都记录在此文件。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增

- 错误体系：新增 `errors` 子包与 `BaseError` 库内错误根基类，便于调用方 `except BaseError` 统一兜底。
- `RequestRefuseError`：请求被 PI 拒绝（响应 `success=False`）时的具名异常，携带 `response`（响应本体，拒绝原因/指令/请求 id 均从它现取），可从 `pi_bridge` 包根直接导入。异常消息即 `response.error`（缺 `error` 字段时为空串）。

### 变更

- `PiClient.prompt` 在请求被拒（`success=False`）时由**静默结束（零事件）**改为抛出 `RequestRefuseError`；拒绝原因与响应本体不再丢失。
- `PiClient.prompt` 的 `streamingBehavior` 参数类型由 `Optional[str]` 收紧为 `Optional[Literal["steer", "followUp"]]`，IDE 与类型检查器可正确提示取值。
- `PiClient.prompt` 的返回标注由 `AsyncIterator[str]` 修正为 `AsyncIterator[models.BaseEvent]`（实际产出一直是事件模型）。
- `PIProcess.build` 的关键字参数 `session` 更名为 `session_id`（对应 PI CLI 的 `--session-id`）。

### 测试

- 新增 `tests/test_errors.py`（7 例）：导出路径 / 继承链 / response 单一真相源 / 消息只带拒绝原因 / 缺 `error` 字段时消息为空串 / 任意 `BaseResponse` 子类 / 以 `BaseError` 捕获。
- `test_prompt_rejected_yields_nothing` 改为 `test_prompt_rejected_raises_request_refuse_error`（断异常字段 + 订阅者仍退订），并新增缺 `error` 字段的拒绝用例。

### 清理

- 移除 `PIToolBackend` 连接建立时的调试 `print`，避免污染 stdout。
- `StateData` / `StateResponse` 字段顺序与格式对齐（无行为变化）。

## [0.5.5] - 2026-09-12

### 新增

- `PiClient.receive_events(*event_type)`：类型化事件过滤的 async generator。可传入一个或多个事件类，仅产出匹配类型的事件对象；不传类型时产出全部事件。reader 崩溃时抛出原始异常，消费结束时自动退订。
- `PIProcess.build(buffer_limit=...)`：新增子进程 stdout 读取缓冲区大小参数（默认 64KB），透传 `asyncio.subprocess` 的 `limit`，用于大输出场景（如长回复流）。

### 测试

- 新增 `receive_events` 4 组单测：单类型过滤 / 多类型过滤 / 跳过不匹配事件 / 零参数接收全部事件。

## [0.5.4] - 2026-09-05

### 重构

- 包路径 `pi_backend` → `pi_bridge`，`PiClient` 工厂拆缝统一 `build` 命名。
- 修复 `TreeEntry` 递归模型。

## [0.5.2] - 2026-09-02

### 重构

- `PiClient.connect` → `open` 工厂重命名，引用与文档同步。

## [0.5.0] - 2026-09-01

### 重构

- 架构重构 `PIBackend` → `PiClient` / `PiTransport` + 协议层，Field 化改造完成。

## [0.4.2] - 2026-08-30

### 变更

- tests 套件纳入版本控制。
- `follow_up` 语义文档补充。
- `close_backend` 幂等化。

## [0.4.1] - 2026-08-30

### 初始

- 初始提交：`pi_backend` v0.4.1。
