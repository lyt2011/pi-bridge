"""CommandEnum 集成测试

覆盖范围：
1. CommandEnum.GET_STATE 等成员存在
2. 字符串 "get_state" 能通过基类 validator 转成枚举（构造 dict 走 dispatcher 验证）
"""

from pi_backend.enums import CommandEnum
from pi_backend.factory import responses_factory


# ─── 成员存在性 ───

def test_command_enum_members_exist():
    """代表性 CommandEnum 成员应存在且值正确"""
    assert CommandEnum.GET_STATE.value == "get_state"
    assert CommandEnum.PROMPT.value == "prompt"
    assert CommandEnum.SET_MODEL.value == "set_model"
    assert CommandEnum.GET_AVAILABLE_MODELS.value == "get_available_models"
    assert CommandEnum.GET_LAST_ASSISTANT_TEXT.value == "get_last_assistant_text"
    assert CommandEnum.BASH.value == "bash"
    assert CommandEnum.GET_COMMANDS.value == "get_commands"


def test_command_enum_count():
    """CommandEnum 应包含 33 个指令名"""
    assert len(list(CommandEnum)) == 33


def test_command_enum_all_values_are_str():
    """所有 CommandEnum 成员的值都是字符串"""
    for member in CommandEnum:
        assert isinstance(member.value, str)


# ─── 字符串转枚举 ───

def test_string_get_state_converted_via_validator():
    """字符串 'get_state' 经 BaseResponse validator 转为 CommandEnum.GET_STATE"""
    obj = responses_factory.dispatcher({"type": "response", "command": "get_state", "success": True})
    assert obj.command == CommandEnum.GET_STATE
    assert isinstance(obj.command, CommandEnum)


def test_string_prompt_converted_via_validator():
    obj = responses_factory.dispatcher({"type": "response", "command": "prompt", "success": True})
    assert obj.command == CommandEnum.PROMPT


def test_string_set_model_converted_via_validator():
    obj = responses_factory.dispatcher({"type": "response", "command": "set_model", "success": True})
    assert obj.command == CommandEnum.SET_MODEL


def test_string_get_available_models_converted_via_validator():
    obj = responses_factory.dispatcher({"type": "response", "command": "get_available_models", "success": True})
    assert obj.command == CommandEnum.GET_AVAILABLE_MODELS


def test_string_get_last_assistant_text_converted_via_validator():
    obj = responses_factory.dispatcher(
        {"type": "response", "command": "get_last_assistant_text", "success": True}
    )
    assert obj.command == CommandEnum.GET_LAST_ASSISTANT_TEXT


def test_command_enum_direct_construction():
    """直接用枚举成员构造模型亦可"""
    from pi_backend.models import StateResponse
    obj = StateResponse(command=CommandEnum.GET_STATE, success=True)
    assert obj.command == CommandEnum.GET_STATE
    assert obj.command.value == "get_state"