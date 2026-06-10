#!/usr/bin/env python3
"""
Small Chinese meme caption planner.

This is intentionally heuristic: it gives Codex/user a sharper first draft before
rendering, instead of pretending every scene should use the same top/bottom text.
"""

import argparse
import random


ANGLES = {
    "发疯但体面": [
        ("表面：{calm}", "内心：{threat}"),
        ("我：{calm}", "也是我：{threat}"),
    ],
    "开源求关注": [
        ("开源是为了交流", "不是为了求 STAR（假的）"),
        ("我：欢迎大家试用", "内心：你最好真用"),
    ],
    "工具没人用": [
        ("工具做完了", "用户还在路上"),
        ("以为发布就结束了", "结果推广才刚开始"),
    ],
    "AI 打工人": [
        ("AI 帮我省了 3 小时", "我花 5 小时研究怎么发"),
        ("本来只是想提效", "结果开始内容创业"),
    ],
    "小红书标题党": [
        ("别再乱做 AI 工具了", "先学会让人想点开"),
        ("我发现一个离谱真相", "工具不会自己长流量"),
    ],
}

PRESET_HINTS = {
    "发疯但体面": "xiaohongshu-yellow",
    "开源求关注": "xiaohongshu-yellow",
    "工具没人用": "classic-white",
    "AI 打工人": "rage-red",
    "小红书标题党": "xiaohongshu-yellow",
}


def infer_slots(scene: str) -> dict[str, str]:
    calm = "欢迎大家试用"
    threat = "你最好真用"
    if "star" in scene.lower() or "开源" in scene or "github" in scene.lower():
        calm = "欢迎大家随便看看"
        threat = "顺手点个 STAR 不过分吧"
    elif "流量" in scene or "推广" in scene or "小红书" in scene:
        calm = "我只是随便发发"
        threat = "怎么还没人爆"
    elif "AI" in scene or "工具" in scene:
        calm = "这只是个小工具"
        threat = "已经开始想商业模式"
    return {"calm": calm, "threat": threat}


def generate(scene: str, count: int) -> list[tuple[str, str, str, str]]:
    slots = infer_slots(scene)
    pool = []
    for angle, patterns in ANGLES.items():
        for top, bottom in patterns:
            pool.append((
                angle,
                top.format(**slots),
                bottom.format(**slots),
                PRESET_HINTS[angle],
            ))
    random.seed(scene)
    random.shuffle(pool)
    return pool[:count]


def main():
    parser = argparse.ArgumentParser(description="Generate Chinese meme caption ideas")
    parser.add_argument("scene", help="Scene, product, hot topic, or meme concept")
    parser.add_argument("-n", "--count", type=int, default=6)
    args = parser.parse_args()

    for idx, (angle, top, bottom, preset) in enumerate(generate(args.scene, args.count), 1):
        print(f"{idx}. [{angle}] preset={preset}")
        print(f"   TOP: {top}")
        print(f"   BOTTOM: {bottom}")


if __name__ == "__main__":
    main()
