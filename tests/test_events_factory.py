"""events_factory 分发测试

覆盖范围：
1. 注册数 == 22
2. 对代表性事件构造原始 dict，断言返回正确类型
3. 未知 type 抛 DispatchFailed
"""

import pytest
from easy_factory import DispatchFailed
from pi_backend.factory import events_factory
from pi_backend.models import (
    AgentStartEvent,
    AgentEndEvent,
    AgentSettledEvent,
    TurnStartEvent,
    TurnEndEvent,
    MessageStartEvent,
    MessageUpdateEvent,
    MessageEndEvent,
    BashExecutionUpdateEvent,
    ToolExecutionStartEvent,
    ToolExecutionUpdateEvent,
    ToolExecutionEndEvent,
    QueueUpdateEvent,
    CompactionStartEvent,
    CompactionEndEvent,
    AutoRetryStartEvent,
    AutoRetryEndEvent,
    SummarizationRetryScheduledEvent,
    SummarizationRetryAttemptStartEvent,
    SummarizationRetryFinishedEvent,
    ExtensionErrorEvent,
    ExtensionUIRequestEvent,
)


def _ev(type_: str, **kw) -> dict:
    d = {"type": type_}
    d.update(kw)
    return d


# ─── 注册数 ───

def test_events_factory_registered_count():
    """events_factory 应注册 22 个事件模型"""
    assert len(events_factory) == 22


# ─── 代表性事件分发 ───

def test_dispatch_agent_start():
    obj = events_factory.dispatcher(_ev("agent_start"))
    assert isinstance(obj, AgentStartEvent)


def test_dispatch_agent_end():
    obj = events_factory.dispatcher(_ev("agent_end"))
    assert isinstance(obj, AgentEndEvent)


def test_dispatch_agent_settled():
    obj = events_factory.dispatcher(_ev("agent_settled"))
    assert isinstance(obj, AgentSettledEvent)


def test_dispatch_turn_start():
    obj = events_factory.dispatcher(_ev("turn_start"))
    assert isinstance(obj, TurnStartEvent)


def test_dispatch_turn_end():
    obj = events_factory.dispatcher(_ev("turn_end"))
    assert isinstance(obj, TurnEndEvent)


def test_dispatch_message_start():
    obj = events_factory.dispatcher(_ev("message_start"))
    assert isinstance(obj, MessageStartEvent)


def test_dispatch_message_update():
    obj = events_factory.dispatcher(_ev("message_update"))
    assert isinstance(obj, MessageUpdateEvent)


def test_dispatch_message_end():
    obj = events_factory.dispatcher(_ev("message_end"))
    assert isinstance(obj, MessageEndEvent)


def test_dispatch_bash_execution_update():
    obj = events_factory.dispatcher(_ev("bash_execution_update"))
    assert isinstance(obj, BashExecutionUpdateEvent)


def test_dispatch_tool_execution_start():
    obj = events_factory.dispatcher(_ev("tool_execution_start"))
    assert isinstance(obj, ToolExecutionStartEvent)


def test_dispatch_tool_execution_update():
    obj = events_factory.dispatcher(_ev("tool_execution_update"))
    assert isinstance(obj, ToolExecutionUpdateEvent)


def test_dispatch_tool_execution_end():
    obj = events_factory.dispatcher(_ev("tool_execution_end"))
    assert isinstance(obj, ToolExecutionEndEvent)


def test_dispatch_queue_update():
    obj = events_factory.dispatcher(_ev("queue_update"))
    assert isinstance(obj, QueueUpdateEvent)


def test_dispatch_compaction_start():
    obj = events_factory.dispatcher(_ev("compaction_start"))
    assert isinstance(obj, CompactionStartEvent)


def test_dispatch_compaction_end():
    obj = events_factory.dispatcher(_ev("compaction_end"))
    assert isinstance(obj, CompactionEndEvent)


def test_dispatch_auto_retry_start():
    obj = events_factory.dispatcher(_ev("auto_retry_start"))
    assert isinstance(obj, AutoRetryStartEvent)


def test_dispatch_auto_retry_end():
    obj = events_factory.dispatcher(_ev("auto_retry_end"))
    assert isinstance(obj, AutoRetryEndEvent)


def test_dispatch_summarization_retry_scheduled():
    obj = events_factory.dispatcher(_ev("summarization_retry_scheduled"))
    assert isinstance(obj, SummarizationRetryScheduledEvent)


def test_dispatch_summarization_retry_attempt_start():
    obj = events_factory.dispatcher(_ev("summarization_retry_attempt_start"))
    assert isinstance(obj, SummarizationRetryAttemptStartEvent)


def test_dispatch_summarization_retry_finished():
    obj = events_factory.dispatcher(_ev("summarization_retry_finished"))
    assert isinstance(obj, SummarizationRetryFinishedEvent)


def test_dispatch_extension_error():
    obj = events_factory.dispatcher(_ev("extension_error"))
    assert isinstance(obj, ExtensionErrorEvent)


def test_dispatch_extension_ui_request():
    """extension_ui_request 需要 method 字段"""
    obj = events_factory.dispatcher(_ev("extension_ui_request", method="notify"))
    assert isinstance(obj, ExtensionUIRequestEvent)
    assert obj.method == "notify"


# ─── 未知 type ───

def test_unknown_type_raises_dispatch_failed():
    """未知 type 导致 DispatchFailed"""
    with pytest.raises(DispatchFailed):
        events_factory.dispatcher(_ev("not_a_real_event_type"))