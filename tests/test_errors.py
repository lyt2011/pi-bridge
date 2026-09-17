"""错误体系测试

覆盖: 导出路径 / 继承链 / RequestRefuseError 的 response 单一真相源 /
异常消息(唯一可见输出) / 任意 BaseResponse 子类 / 兜底文案
不启动进程、不连后端。
"""

import pytest

from pi_bridge			import BaseError, RequestRefuseError
from pi_bridge.enums	import CommandEnum
from pi_bridge.errors	import pi_errors
from pi_bridge.models	import PromptResponse, BashResponse


def test_errors_exported_from_package_root():
    """错误类可从包根与子包两处导入, 且属同一对象"""
    assert pi_errors.RequestRefuseError is RequestRefuseError
    assert issubclass(RequestRefuseError, BaseError)


def test_base_error_is_library_root():
    """BaseError 是库内错误根, 继承自 Exception"""
    assert issubclass(BaseError, Exception)
    assert RequestRefuseError.__mro__[1] is BaseError


def test_request_refuse_error_exposes_response():
    """唯一真相源是 response: 拒绝原因/指令/请求 id 都从它现取, 不另存副本"""
    resp = PromptResponse(command="prompt", success=False, id="r1", error="正忙")

    err = RequestRefuseError(resp)

    assert err.response is resp
    assert err.response.error == "正忙"
    assert err.response.id == "r1"
    assert err.response.command is CommandEnum.PROMPT


def test_message_is_reason_only():
    """消息只带拒绝原因, 不加指令名/前缀"""
    err = RequestRefuseError(PromptResponse(command="prompt", success=False, error="正忙"))

    assert str(err) == err.response.error
    assert str(err) == "正忙"


def test_message_is_empty_without_error_field():
    """响应缺 error 字段时消息为空串; 数据仍在 response 上, 用 err.response.error 取"""
    err = RequestRefuseError(PromptResponse(command="prompt", success=False))

    assert str(err) == ""
    assert err.response.error is None


def test_request_refuse_error_accepts_any_response_subclass():
    """任意 BaseResponse 子类 (如 BashResponse) 都能构造"""
    err = RequestRefuseError(BashResponse(command="bash", success=False, error="command not found"))

    assert str(err) == "command not found"
    assert err.response.command is CommandEnum.BASH


def test_request_refuse_error_is_catchable_as_base_error():
    """可用 BaseError 统一兜住所有库错误"""
    with pytest.raises(BaseError):
        raise RequestRefuseError(PromptResponse(command="prompt", success=False))
