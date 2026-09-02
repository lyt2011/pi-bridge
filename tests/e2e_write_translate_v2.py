#!/usr/bin/env python3
"""
端到端测试 (PiClient): 让 pi 写短文 → 存 /tmp/ → 翻译 → 存 /tmp/。

用 PiClient.prompt() 流式消费事件 (async generator), 非旧的 read_pydantic 循环。
"""
import asyncio, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pi_backend import PiClient
from pi_backend.models import (
	MessageUpdateEvent, MessageEndEvent, AgentSettledEvent, TextDeltaEvent, TextEndEvent,
)


def extract_text(msg) -> str:
    """从 AgentMessage 模型提取所有 text 块内容 (属性访问, 非 dict)"""
    content = getattr(msg, "content", None)
    if isinstance(content, str):
        return content
    if not content:
        return ""
    return "".join(
        b.text
        for b in content
        if getattr(b, "type", None) == "text"
    )


async def main() -> None:
    client = await PiClient.open(session_dir="/tmp/pi_e2e_v2")

    # 切换模型
    resp = await client.set_model("seed_api", "deepseek-v4-flash")
    print(f"✅ 模型: seed_api/deepseek-v4-flash (success={resp.success})")

    # === 第 1 轮: 写中文短文 ===
    zh_prompt = "请写一篇50字左右的中文短文，主题是春天。直接输出正文，不要任何解释。"
    print("📝 第1轮: 写中文\n" + "─" * 40)
    zh_text = ""
    async for m in client.prompt(zh_prompt):
        if isinstance(m, MessageUpdateEvent) and isinstance(m.assistantMessageEvent, TextDeltaEvent):
            zh_text += m.assistantMessageEvent.delta
        elif isinstance(m, MessageEndEvent) and m.message is not None and m.message.role == "assistant":
            zh_text = extract_text(m.message)
        elif isinstance(m, AgentSettledEvent):
            print("  [agent_settled] 第1轮完成")
    zh_text = zh_text.strip()

    zh_path = "/tmp/pi_e2e_zh.txt"
    with open(zh_path, "w", encoding="utf-8") as f:
        f.write(zh_text)
    print(f"✅ 写入 {zh_path} ({len(zh_text)} 字)")
    print("   内容:", zh_text[:120])

    # === 第 2 轮: 新 prompt 翻译（带原文） ===
    en_prompt = f"请将下面的中文短文翻译成英文，只输出英文译文：\n\n{zh_text}"
    print("\n📝 第2轮: 翻译英文\n" + "─" * 40)
    en_text = ""
    async for m in client.prompt(en_prompt):
        if isinstance(m, MessageUpdateEvent) and isinstance(m.assistantMessageEvent, TextDeltaEvent):
            en_text += m.assistantMessageEvent.delta
        elif isinstance(m, MessageEndEvent) and m.message is not None and m.message.role == "assistant":
            en_text = extract_text(m.message)
        elif isinstance(m, AgentSettledEvent):
            print("  [agent_settled] 第2轮完成")
    en_text = en_text.strip()

    en_path = "/tmp/pi_e2e_en.txt"
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_text)
    print(f"✅ 写入 {en_path} ({len(en_text)} 字符)")
    print("   内容:", en_text[:200])

    await client.close()
    print("\n🎉 完成")
    # 验证文件
    for p in (zh_path, en_path):
        with open(p) as f:
            c = f.read()
        print(f"  {p}: {len(c)} 字符/字节")


if __name__ == "__main__":
    asyncio.run(main())
