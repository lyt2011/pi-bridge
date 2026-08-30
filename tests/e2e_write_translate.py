#!/usr/bin/env python3
"""
端到端测试: 用 pi_backend 让 pi 写一篇 50 字左右的中文短文存入 /tmp/,
再翻译成英文存入 /tmp/。
"""
import asyncio, json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pi_backend import PIProcess, PIBackend
from pi_backend.models import (
    MessageUpdateEvent,
    MessageEndEvent,
    TurnEndEvent,
    AgentSettledEvent,
    BaseResponse,
)


def extract_text(msg: dict) -> str:
    """从 AgentMessage dict 提取所有 text 块内容"""
    content = msg.get("content", [])
    if isinstance(content, str):
        return content
    return "".join(
        b.get("text", "")
        for b in content
        if isinstance(b, dict) and b.get("type") == "text"
    )


async def collect_turn(backend: PIBackend, timeout: float = 180.0) -> str:
    """
    读取事件直到回合完全安定 (agent_settled)。
    返回 assistant 权威全文 (取最后一条 assistant message_end 的 message)。
    """
    deltas: list[str] = []
    authoritative: str = ""
    start = asyncio.get_event_loop().time()

    while asyncio.get_event_loop().time() - start < timeout:
        try:
            m = await asyncio.wait_for(backend.read_pydantic(), timeout=timeout)
        except asyncio.TimeoutError:
            print("  [collect_turn] TIMEOUT")
            break

        if isinstance(m, MessageUpdateEvent):
            ev = m.assistantMessageEvent
            if ev.get("type") == "text_delta":
                deltas.append(ev.get("delta", ""))
        elif isinstance(m, MessageEndEvent):
            if m.message.get("role") == "assistant":
                authoritative = extract_text(m.message)
        elif isinstance(m, AgentSettledEvent):
            # 完全安定: 无重试/压缩/队列延续
            break

    # 优先权威全文; 兜底累积 delta
    text = authoritative or "".join(deltas)
    return text.strip()


async def main() -> None:
    session_dir = "/tmp/pi_e2e_session"
    proc = await PIProcess.build_process(session_dir=session_dir)
    backend = PIBackend(pi_process=proc)

    # 1) 切换可用模型 (deepseek-v4-pro 无渠道, flash 可用)
    await backend.set_model("seed_api", "deepseek-v4-flash")
    end = asyncio.get_event_loop().time() + 60
    while asyncio.get_event_loop().time() < end:
        m = await asyncio.wait_for(backend.read_pydantic(), timeout=60)
        if type(m).__name__ == "SetModelResponse":
            print("✅ 模型已切换: seed_api/deepseek-v4-flash")
            break

    # 2) 让 pi 写中文短文
    await backend.prompt("请写一篇50字左右的中文短文，主题是春天。直接输出正文，不要任何解释。")
    zh_text = await collect_turn(backend)
    zh_path = "/tmp/pi_article_zh.txt"
    with open(zh_path, "w", encoding="utf-8") as f:
        f.write(zh_text)
    print(f"✅ 中文短文已写入 {zh_path} ({len(zh_text)} 字)")
    print("   ── 内容 ──")
    print("   " + zh_text.replace("\n", "\n   "))

    # 3) 同一会话 follow_up 翻译成英文
    await backend.follow_up("请把上面那篇短文翻译成英文。只输出英文译文，不要任何解释。")
    en_text = await collect_turn(backend)
    en_path = "/tmp/pi_article_en.txt"
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_text)
    print(f"\n✅ 英文译文已写入 {en_path} ({len(en_text)} 字符)")
    print("   ── 内容 ──")
    print("   " + en_text.replace("\n", "\n   "))

    await proc.close_process()
    print("\n🎉 端到端测试完成")


if __name__ == "__main__":
    asyncio.run(main())
