#!/usr/bin/env python3
"""
端到端测试 v2: 让 pi 写短文 → 存 /tmp/ → 翻译 → 存 /tmp/。
用 prompt 而非 follow_up，避免队列问题。
"""
import asyncio, json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pi_backend import PIProcess, PIBackend
from pi_backend.models import (
    MessageUpdateEvent,
    MessageEndEvent,
    TurnEndEvent,
    AgentSettledEvent,
)


def extract_text(msg: dict) -> str:
    content = msg.get("content", [])
    if isinstance(content, str):
        return content
    return "".join(
        b.get("text", "")
        for b in content
        if isinstance(b, dict) and b.get("type") == "text"
    )


async def collect_turn(backend, timeout=180, debug=True):
    deltas = []
    authoritative = ""
    start = asyncio.get_event_loop().time()

    while asyncio.get_event_loop().time() - start < timeout:
        try:
            m = await asyncio.wait_for(backend.read_pydantic(), timeout=timeout)
        except asyncio.TimeoutError:
            print("  [TIMEOUT] collect_turn")
            break

        name = type(m).__name__
        if isinstance(m, MessageUpdateEvent):
            ev = m.assistantMessageEvent
            if ev.get("type") == "text_delta":
                deltas.append(ev.get("delta", ""))
        elif isinstance(m, MessageEndEvent):
            if m.message.get("role") == "assistant":
                authoritative = extract_text(m.message)
                if debug:
                    print(f"  [message_end] assistant 权威: {repr(authoritative[:80])}...")
        elif isinstance(m, AgentSettledEvent):
            if debug:
                print("  [agent_settled] 回合完成")
            break
        elif isinstance(m, TurnEndEvent):
            if debug:
                print("  [turn_end] turn 完成")
        elif m.type == "response":
            cmd = getattr(m, "command", "")
            if debug:
                print(f"  [response] command={cmd}")

    text = authoritative or "".join(deltas)
    return text.strip()


async def main():
    proc = await PIProcess.build_process(session_dir="/tmp/pi_e2e_v2")
    backend = PIBackend(pi_process=proc)

    # 切换模型
    await backend.set_model("seed_api", "deepseek-v4-flash")
    end = asyncio.get_event_loop().time() + 60
    while asyncio.get_event_loop().time() < end:
        m = await asyncio.wait_for(backend.read_pydantic(), timeout=60)
        if type(m).__name__ == "SetModelResponse":
            print("✅ 模型: seed_api/deepseek-v4-flash")
            break

    # === 第 1 轮: 写中文短文 ===
    zh_prompt = "请写一篇50字左右的中文短文，主题是春天。直接输出正文，不要任何解释。"
    await backend.prompt(zh_prompt)
    print("📝 第1轮: 写中文\n" + "─" * 40)
    zh_text = await collect_turn(backend)
    zh_path = "/tmp/pi_e2e_zh.txt"
    with open(zh_path, "w", encoding="utf-8") as f:
        f.write(zh_text)
    print(f"✅ 写入 {zh_path} ({len(zh_text)} 字)")
    print("   内容:", zh_text[:120])

    # === 第 2 轮: 新 prompt 翻译（带原文） ===
    en_prompt = f"请将下面的中文短文翻译成英文，只输出英文译文：\n\n{zh_text}"
    await backend.prompt(en_prompt)
    print("\n📝 第2轮: 翻译英文\n" + "─" * 40)
    en_text = await collect_turn(backend, timeout=300)
    en_path = "/tmp/pi_e2e_en.txt"
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_text)
    print(f"✅ 写入 {en_path} ({len(en_text)} 字符)")
    print("   内容:", en_text[:200])

    await proc.close_process()
    print("\n🎉 完成")
    # 验证文件
    for p in (zh_path, en_path):
        with open(p) as f:
            c = f.read()
        print(f"  {p}: {len(c)} 字符/字节")


if __name__ == "__main__":
    asyncio.run(main())