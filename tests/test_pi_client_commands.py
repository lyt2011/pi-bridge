"""PiClient 指令语义方法测试

覆盖: 31 个指令方法 (prompt/get_state 已在 test_pi_client.py 覆盖)
表驱动: 每个方法 → 发出正确 type 的指令 → 收到对应类型的响应模型
"""

import orjson
import pytest

from pi_backend.core.pi_client		import PiClient
from pi_backend.core.pi_transport	import PiTransport
from pi_backend.models				import (
	SteerResponse, FollowUpResponse, AbortResponse, ClearQueueResponse,
	NewSessionResponse, GetMessagesResponse, SetModelResponse,
	CycleModelResponse, GetAvailableModelsResponse, SetThinkingLevelResponse,
	CycleThinkingLevelResponse, GetAvailableThinkingLevelsResponse,
	SetSteeringModeResponse, SetFollowUpModeResponse, CompactResponse,
	SetAutoCompactionResponse, SetAutoRetryResponse, AbortRetryResponse,
	BashResponse, AbortBashResponse, GetSessionStatsResponse,
	ExportHtmlResponse, SwitchSessionResponse, ForkResponse, CloneResponse,
	GetForkMessagesResponse, GetEntriesResponse, GetTreeResponse,
	GetLastAssistantTextResponse, SetSessionNameResponse, GetCommandsResponse,
)

import asyncio
import json


class FakeIO:
    """可编程的线级 IO (与 test_pi_client 同款)"""

    def __init__(self):
        self._inbox		= asyncio.Queue()
        self.written	= []

    async def read_line(self) -> str:
        return await self._inbox.get()

    async def write_line(self, *lines: str) -> None:
        self.written.extend(lines)

    async def close_process(self) -> None:
        pass

    def last_written(self) -> dict:
        return json.loads(self.written[-1])

    def push_response(self, cmd_type: str, rid: str, **data) -> None:
        line = {"type": "response", "command": cmd_type, "success": True, "id": rid}
        line.update(data)
        self._inbox.put_nowait(orjson.dumps(line).decode("utf-8"))


async def make_client() -> tuple[PiClient, FakeIO]:
    io = FakeIO()
    client = PiClient(PiTransport(io))
    await client.start()
    return client, io


# 表: (方法名, 调用方式, 期望指令type, 期望响应类)
CASES = [
    ("steer",					lambda c: c.steer("hi"),									"steer",				SteerResponse),
    ("follow_up",				lambda c: c.follow_up("hi"),								"follow_up",			FollowUpResponse),
    ("abort",					lambda c: c.abort(),										"abort",				AbortResponse),
    ("clear_queue",				lambda c: c.clear_queue(),									"clear_queue",			ClearQueueResponse),
    ("new_session",				lambda c: c.new_session(parent_session="p1"),				"new_session",			NewSessionResponse),
    ("get_messages",			lambda c: c.get_messages(),								"get_messages",			GetMessagesResponse),
    ("set_model",				lambda c: c.set_model("seed_api", "deepseek-v4-flash"),		"set_model",			SetModelResponse),
    ("cycle_model",				lambda c: c.cycle_model(),									"cycle_model",			CycleModelResponse),
    ("get_available_models",	lambda c: c.get_available_models(),						"get_available_models",	GetAvailableModelsResponse),
    ("set_thinking_level",		lambda c: c.set_thinking_level("high"),					"set_thinking_level",	SetThinkingLevelResponse),
    ("cycle_thinking_level",	lambda c: c.cycle_thinking_level(),						"cycle_thinking_level",	CycleThinkingLevelResponse),
    ("get_available_thinking_levels",	lambda c: c.get_available_thinking_levels(),	"get_available_thinking_levels",	GetAvailableThinkingLevelsResponse),
    ("set_steering_mode",		lambda c: c.set_steering_mode("all"),						"set_steering_mode",	SetSteeringModeResponse),
    ("set_follow_up_mode",		lambda c: c.set_follow_up_mode("all"),						"set_follow_up_mode",	SetFollowUpModeResponse),
    ("compact",					lambda c: c.compact(custom_instructions="keep summary"),	"compact",				CompactResponse),
    ("set_auto_compaction",		lambda c: c.set_auto_compaction(True),						"set_auto_compaction",	SetAutoCompactionResponse),
    ("set_auto_retry",			lambda c: c.set_auto_retry(True),							"set_auto_retry",		SetAutoRetryResponse),
    ("abort_retry",				lambda c: c.abort_retry(),								"abort_retry",			AbortRetryResponse),
    ("bash",					lambda c: c.bash("echo hi"),								"bash",					BashResponse),
    ("abort_bash",				lambda c: c.abort_bash(),									"abort_bash",			AbortBashResponse),
    ("get_session_stats",		lambda c: c.get_session_stats(),							"get_session_stats",	GetSessionStatsResponse),
    ("export_html",				lambda c: c.export_html(output_path="/tmp/x.html"),		"export_html",			ExportHtmlResponse),
    ("switch_session",			lambda c: c.switch_session("/tmp/s"),						"switch_session",		SwitchSessionResponse),
    ("fork",					lambda c: c.fork("e1"),									"fork",					ForkResponse),
    ("clone",					lambda c: c.clone(),										"clone",				CloneResponse),
    ("get_fork_messages",		lambda c: c.get_fork_messages(),							"get_fork_messages",	GetForkMessagesResponse),
    ("get_entries",				lambda c: c.get_entries(since="1"),						"get_entries",			GetEntriesResponse),
    ("get_tree",				lambda c: c.get_tree(),									"get_tree",				GetTreeResponse),
    ("get_last_assistant_text",	lambda c: c.get_last_assistant_text(),					"get_last_assistant_text",	GetLastAssistantTextResponse),
    ("set_session_name",		lambda c: c.set_session_name("我的会话"),					"set_session_name",		SetSessionNameResponse),
    ("get_commands",			lambda c: c.get_commands(),								"get_commands",			GetCommandsResponse),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("name, caller, cmd_type, resp_cls", CASES, ids=[c[0] for c in CASES])
async def test_semantic_command(name, caller, cmd_type, resp_cls):
    """每个语义方法: 发出正确 type 指令, 收到对应响应模型"""
    client, io = await make_client()

    task = asyncio.create_task(caller(client))
    await asyncio.sleep(0)

    written = io.last_written()
    assert written["type"] == cmd_type

    rid = written["id"]
    io.push_response(cmd_type, rid)

    resp = await task
    assert isinstance(resp, resp_cls)
    assert resp.success


@pytest.mark.asyncio
async def test_commands_in_same_client_share_reader():
    """多个语义方法复用同一 client + 后台 reader, 各拿各的响应"""
    client, io = await make_client()

    t1 = asyncio.create_task(client.get_commands())
    await asyncio.sleep(0)
    rid1 = io.last_written()["id"]

    t2 = asyncio.create_task(client.get_session_stats())
    await asyncio.sleep(0)
    rid2 = io.last_written()["id"]

    # 乱序回
    io.push_response("get_session_stats", rid2)
    io.push_response("get_commands", rid1)

    r1, r2 = await asyncio.gather(t1, t2)
    assert isinstance(r1, GetCommandsResponse)
    assert isinstance(r2, GetSessionStatsResponse)