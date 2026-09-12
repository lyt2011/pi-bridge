# Changelog

本项目的所有重要变更都记录在此文件。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

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
