# meme-generator.skill

A Codex skill for making memes with more than plain top/bottom text.

It can:

- add classic meme captions to images
- generate Chinese meme caption ideas
- use Chinese-style layout presets like yellow text with black stroke
- collect lightweight trend signals from GitHub Trending
- compose platform-native layouts such as fake X screenshots and sticker-store-style images

This project is experimental. The goal is not a polished poster generator. The goal is to make images that feel like internet memes: blunt, platform-native, slightly ugly, and easy to understand in one second.

## Install

Install the skill into Codex:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo hyj-STAR/meme-generator.skill \
  --path . \
  --name meme-generator
```

Then restart Codex.

Install Python dependencies if you want to run scripts directly:

```bash
python3 -m pip install -r requirements.txt
```

## Quick Use

Classic caption:

```bash
python3 scripts/meme_text.py input.jpg \
  --preset classic-white \
  -t "TOP TEXT" \
  -b "BOTTOM TEXT" \
  -o output.jpg
```

Chinese/Xiaohongshu-style big text:

```bash
python3 scripts/meme_text.py input.jpg \
  --preset xiaohongshu-yellow \
  -t "表面：欢迎大家试用" \
  -b "内心：你最好真用" \
  -o output.jpg
```

Generate caption ideas before rendering:

```bash
python3 scripts/meme_brain.py "开源 AI 工具没人用 GitHub star" -n 8
```

Collect trend signals:

```bash
python3 scripts/trend_scraper.py --source github --limit 5 --angles
```

Make a fake X screenshot meme:

```bash
python3 scripts/meme_layout.py input.jpg \
  --style x-screenshot \
  --title "普通开源项目：写 README\\n我的开源项目：先做成烂梗" \
  --punchline "咔咔整活！！！" \
  -o x-meme.jpg
```

Make a sticker-store-style roast:

```bash
python3 scripts/meme_layout.py input.jpg \
  --style sticker \
  --caption "作者本人受到暴击" \
  -o sticker-meme.jpg
```

## Presets

`meme_text.py` supports these presets:

- `classic-white`: white text, black stroke, classic meme style
- `xiaohongshu-yellow`: yellow text, heavy black stroke, Chinese social platform cover style
- `rage-red`: red text with white stroke, useful for high-emotion captions
- `subtitle-black`: black text with white stroke, useful for screenshot/commentary memes

You can still override preset values:

```bash
python3 scripts/meme_text.py input.jpg \
  --preset xiaohongshu-yellow \
  --fill "#FFD426" \
  --stroke-fill "#050505" \
  --font-size 0.072 \
  --top-y 0.05 \
  --bottom-y 0.83 \
  --no-uppercase \
  -t "表面：欢迎大家试用" \
  -b "内心：你最好真用" \
  -o output.jpg
```

## What Makes It Different

Most meme tools stop at adding text. This skill adds a small meme workflow:

1. Find a scene or trend.
2. Generate caption angles.
3. Choose a platform-native visual style.
4. Render with preset typography and layout.

Reference files:

- `references/templates.md`: classic meme templates and common IDs
- `references/chinese-meme-playbook.md`: Chinese meme caption and layout rules
- `references/reference-styles.md`: visual recipes extracted from real meme screenshots

## X/Twitter Notes

Direct X scraping is brittle and often requires account auth, cookies, proxies, or paid infrastructure. This repo does not brute-force anti-bot systems.

The trend collector currently supports GitHub Trending by default. Reddit public JSON may be blocked depending on network conditions. X support is intentionally left as an optional adapter path for tools such as Scweet, twscrape, Twikit, official API access, or user-provided `X_AUTH_TOKEN`.

## Example Captions

- 表面：欢迎大家试用 / 内心：你最好真用
- 开源是为了交流 / 不是为了求 STAR（假的）
- 普通开源项目：写 README / 我的开源项目：先做成烂梗
- 工具做完了 / 用户还在路上
- 本来只是想提效 / 结果开始内容创业

## Status

Experimental and evolving. The current focus is Chinese tech meme energy: GitHub, AI agents, Codex skills, open-source promotion, and developer self-roast.
