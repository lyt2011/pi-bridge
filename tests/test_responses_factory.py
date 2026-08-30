"""responses_factory 分发测试

覆盖范围：
1. 注册数 == 33
2. 对代表性 command 构造原始 dict，断言返回正确类型
3. 未知 command 抛 DispatchFailed
4. CommandEnum 集成：字符串 "get_state" 能通过基类 validator 转成枚举
"""

import pytest
from easy_factory import DispatchFailed
from pi_backend.factory import responses_factory
from pi_backend.enums import CommandEnum
from pi_backend.models import (
    PromptResponse,
    SteerResponse,
    AbortResponse,
    ClearQueueResponse,
    NewSessionResponse,
    StateResponse,
    GetMessagesResponse,
    SetModelResponse,
    CycleModelResponse,
    GetAvailableModelsResponse,
    SetThinkingLevelResponse,
    CycleThinkingLevelResponse,
    GetAvailableThinkingLevelsResponse,
    SetSteeringModeResponse,
    SetFollowUpModeResponse,
    CompactResponse,
    SetAutoCompactionResponse,
    SetAutoRetryResponse,
    AbortRetryResponse,
    BashResponse,
    AbortBashResponse,
    GetSessionStatsResponse,
    ExportHtmlResponse,
    SwitchSessionResponse,
    ForkResponse,
    CloneResponse,
    GetForkMessagesResponse,
    GetEntriesResponse,
    GetTreeResponse,
    GetLastAssistantTextResponse,
    SetSessionNameResponse,
    GetCommandsResponse,
)


def _resp(command: str, **kw) -> dict:
    """构造一个原始响应 dict"""
    d = {"type": "response", "command": command, "success": True}
    d.update(kw)
    return d


# ─── 注册数 ───

def test_responses_factory_registered_count():
    """responses_factory 应注册 33 个响应模型"""
    assert len(responses_factory) == 33


# ─── 代表性 command 分发 ───

def test_dispatch_prompt():
    obj = responses_factory.dispatcher(_resp("prompt"))
    assert isinstance(obj, PromptResponse)


def test_dispatch_get_state():
    obj = responses_factory.dispatcher(_resp("get_state"))
    assert isinstance(obj, StateResponse)


def test_dispatch_set_model():
    obj = responses_factory.dispatcher(_resp("set_model"))
    assert isinstance(obj, SetModelResponse)


def test_dispatch_get_available_models():
    obj = responses_factory.dispatcher(_resp("get_available_models"))
    assert isinstance(obj, GetAvailableModelsResponse)


def test_dispatch_get_last_assistant_text():
    obj = responses_factory.dispatcher(_resp("get_last_assistant_text"))
    assert isinstance(obj, GetLastAssistantTextResponse)


def test_dispatch_steer():
    obj = responses_factory.dispatcher(_resp("steer"))
    assert isinstance(obj, SteerResponse)


def test_dispatch_abort():
    obj = responses_factory.dispatcher(_resp("abort"))
    assert isinstance(obj, AbortResponse)


def test_dispatch_clear_queue():
    obj = responses_factory.dispatcher(_resp("clear_queue"))
    assert isinstance(obj, ClearQueueResponse)


def test_dispatch_new_session():
    obj = responses_factory.dispatcher(_resp("new_session"))
    assert isinstance(obj, NewSessionResponse)


def test_dispatch_get_messages():
    obj = responses_factory.dispatcher(_resp("get_messages"))
    assert isinstance(obj, GetMessagesResponse)


def test_dispatch_cycle_model():
    obj = responses_factory.dispatcher(_resp("cycle_model"))
    assert isinstance(obj, CycleModelResponse)


def test_dispatch_set_thinking_level():
    obj = responses_factory.dispatcher(_resp("set_thinking_level"))
    assert isinstance(obj, SetThinkingLevelResponse)


def test_dispatch_cycle_thinking_level():
    obj = responses_factory.dispatcher(_resp("cycle_thinking_level"))
    assert isinstance(obj, CycleThinkingLevelResponse)


def test_dispatch_get_available_thinking_levels():
    obj = responses_factory.dispatcher(_resp("get_available_thinking_levels"))
    assert isinstance(obj, GetAvailableThinkingLevelsResponse)


def test_dispatch_set_steering_mode():
    obj = responses_factory.dispatcher(_resp("set_steering_mode"))
    assert isinstance(obj, SetSteeringModeResponse)


def test_dispatch_set_follow_up_mode():
    obj = responses_factory.dispatcher(_resp("set_follow_up_mode"))
    assert isinstance(obj, SetFollowUpModeResponse)


def test_dispatch_compact():
    obj = responses_factory.dispatcher(_resp("compact"))
    assert isinstance(obj, CompactResponse)


def test_dispatch_set_auto_compaction():
    obj = responses_factory.dispatcher(_resp("set_auto_compaction"))
    assert isinstance(obj, SetAutoCompactionResponse)


def test_dispatch_set_auto_retry():
    obj = responses_factory.dispatcher(_resp("set_auto_retry"))
    assert isinstance(obj, SetAutoRetryResponse)


def test_dispatch_abort_retry():
    obj = responses_factory.dispatcher(_resp("abort_retry"))
    assert isinstance(obj, AbortRetryResponse)


def test_dispatch_bash():
    obj = responses_factory.dispatcher(_resp("bash"))
    assert isinstance(obj, BashResponse)


def test_dispatch_abort_bash():
    obj = responses_factory.dispatcher(_resp("abort_bash"))
    assert isinstance(obj, AbortBashResponse)


def test_dispatch_get_session_stats():
    obj = responses_factory.dispatcher(_resp("get_session_stats"))
    assert isinstance(obj, GetSessionStatsResponse)


def test_dispatch_export_html():
    obj = responses_factory.dispatcher(_resp("export_html"))
    assert isinstance(obj, ExportHtmlResponse)


def test_dispatch_switch_session():
    obj = responses_factory.dispatcher(_resp("switch_session"))
    assert isinstance(obj, SwitchSessionResponse)


def test_dispatch_fork():
    obj = responses_factory.dispatcher(_resp("fork"))
    assert isinstance(obj, ForkResponse)


def test_dispatch_clone():
    obj = responses_factory.dispatcher(_resp("clone"))
    assert isinstance(obj, CloneResponse)


def test_dispatch_get_fork_messages():
    obj = responses_factory.dispatcher(_resp("get_fork_messages"))
    assert isinstance(obj, GetForkMessagesResponse)


def test_dispatch_get_entries():
    obj = responses_factory.dispatcher(_resp("get_entries"))
    assert isinstance(obj, GetEntriesResponse)


def test_dispatch_get_tree():
    obj = responses_factory.dispatcher(_resp("get_tree"))
    assert isinstance(obj, GetTreeResponse)


def test_dispatch_set_session_name():
    obj = responses_factory.dispatcher(_resp("set_session_name"))
    assert isinstance(obj, SetSessionNameResponse)


def test_dispatch_get_commands():
    obj = responses_factory.dispatcher(_resp("get_commands"))
    assert isinstance(obj, GetCommandsResponse)


# ─── 未知 command ───

def test_unknown_command_raises_dispatch_failed():
    """未知 command 导致 DispatchFailed"""
    with pytest.raises(DispatchFailed):
        responses_factory.dispatcher(_resp("not_a_real_command"))


# ─── CommandEnum 集成 ───

def test_command_string_converted_to_enum_via_dispatcher():
    """字符串 'get_state' 经 BaseResponse validator 转为 CommandEnum.GET_STATE"""
    obj = responses_factory.dispatcher(_resp("get_state"))
    assert obj.command == CommandEnum.GET_STATE


def test_command_string_converted_to_enum_prompt():
    """字符串 'prompt' 经 validator 转为 CommandEnum.PROMPT"""
    obj = responses_factory.dispatcher(_resp("prompt"))
    assert obj.command == CommandEnum.PROMPT


def test_command_string_converted_to_enum_set_model():
    """字符串 'set_model' 经 validator 转为 CommandEnum.SET_MODEL"""
    obj = responses_factory.dispatcher(_resp("set_model"))
    assert obj.command == CommandEnum.SET_MODEL