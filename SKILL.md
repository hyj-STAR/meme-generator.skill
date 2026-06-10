---
name: meme-generator
description: |
  Generate, create, and customize memes in Chinese and English.
  Use this skill when the user wants to: (1) Add classic top/bottom Impact-font text
  to any image to make a meme, (2) Use popular meme templates (Drake, Distracted
  Boyfriend, Surprised Pikachu, panda head, confused old man etc.), (3) AI-generate
  original meme images, (4) Search for and fetch meme templates from the web (Imgflip,
  Reddit, Know Your Meme), (5) Create Chinese internet memes with proper formatting,
  (6) Browse trending memes or find templates by description. Triggers on requests
  like making memes, adding text to images, making reaction images, or any mention of
  specific meme formats or templates.
---

# Meme Generator

Comprehensive meme creation toolkit — classic text overlays, template-based memes,
AI-generated originals, and web-sourced templates.

## Quick Decision Tree

```
User request
├─ "给这张图加字" / "add text to this image"
│   → Use scripts/meme_text.py
│
├─ "做个 XXX 梗图" / "make a XXX meme" (known template)
│   → Check references/templates.md for template
│   → If found: download template → meme_text.py
│   → If Imgflip credentials available: use Imgflip API
│
├─ "生成一个梗图" / "generate a meme" (new/original)
│   → Use image_generate tool for base image
│   → Then meme_text.py for text overlay
│
├─ "有没有 XXX 的模板" / "find me a template for..."
│   → web_search for template → download best match
│   → Or browse imgflip.com/memetemplates with browser
│
└─ "最近有什么梗" / "what memes are trending"
    → web_search "trending memes [today/week]"
    → Summarize with links
```

## Core Workflow 1: Add Text to Image (Classic Meme)

Use `scripts/meme_text.py` for the classic Impact-font top/bottom text format:

First-time setup:

```bash
python3 -m pip install -r requirements.txt
```

```bash
python3 scripts/meme_text.py <image_path> \
  -t "TOP TEXT" \
  -b "BOTTOM TEXT" \
  -o output.png
```

Options:
- `-t / --top` — Top text (auto-uppercased, classic style)
- `-b / --bottom` — Bottom text
- `-o / --output` — Output path (default: `<input>_meme.png`)
- `-f / --font` — Custom .ttf font (auto-detects Impact/LiberationSans)
- `--font-size` — Fraction of image height (default 0.09)

**Important**: Always uppercase the text for classic memes. Split long text across lines naturally — the script auto-wraps.

## Core Workflow 2: Template-Based Memes

When the user names a specific meme template, look it up in `references/templates.md`.

### Using Imgflip API (preferred when credentials available)

Check for `IMGFLIP_USER` and `IMGFLIP_PASS` environment variables:

```bash
curl -X POST "https://api.imgflip.com/caption_image" \
  -d "template_id=<ID>" \
  -d "username=$IMGFLIP_USER" \
  -d "password=$IMGFLIP_PASS" \
  -d "text0=<top text>" \
  -d "text1=<bottom text>"
```

The response contains `data.url` — the generated meme image.

If no credentials: direct the user to sign up (free) at https://imgflip.com/signup and set env vars.

### Manual download + overlay (fallback)

```bash
# 1. Download template
curl -L -o /tmp/template.jpg "<template_url>"

# 2. Add text
python3 scripts/meme_text.py /tmp/template.jpg -t "TOP" -b "BOTTOM" -o /tmp/meme.png
```

## Core Workflow 3: AI-Generated Memes

For original meme concepts or templates without good source images:

1. **Generate base image** with `image_generate`:
   - Describe the meme scene clearly
   - Specify style: "meme template style", "crude drawing", "reaction image"
   - For Chinese memes: specify style (熊猫头风格, 暴漫风格, etc.)

2. **Add text** with `scripts/meme_text.py` on the generated image

3. **Example prompts**:
   - "A surprised white cat sitting at a dinner table, meme template style, blank space for text"
   - "A crude panda face drawing, Chinese meme style (熊猫头), white background"
   - "Two astronauts in space, one pointing a gun at the other, meme format, from behind"

## Core Workflow 4: Finding Templates

### Search the web
```bash
web_search "<concept> meme template"
```

### Browse Imgflip templates
Use the `browser` tool to navigate: https://imgflip.com/memetemplates

### Browse Reddit
Search `/r/MemeTemplatesOfficial` for clean template images.

### Chinese platform search
- 微博搜索: `<关键词> 表情包`
- 小红书搜索: `<关键词> 梗图模板`

## Design Conventions

### Classic Meme Format (English)
- **Font**: Impact or bold sans-serif, white with black stroke
- **Text**: ALL CAPS
- **Position**: Top and/or bottom, centered
- **Stroke**: ~3-5px black outline

### Chinese Meme Format (中文表情包)
- **Font**: Bold sans-serif works for Chinese too
- **Text**: Can be mixed case, often with emoji
- **Position**: Top/bottom or speech-bubble style
- **Tone**: Often more conversational, less ALL-CAPS

### Multi-panel Memes
For memes with multiple panels (Gru's Plan, Expanding Brain):
- Generate or find the multi-panel template
- Add text to individual panels using spatial positioning
- May need manual coordinates if template varies

### AI Generation Best Practices
- Request "meme template style" or "reaction image style" for authenticity
- Leave blank space for text
- For reaction images: strong facial expressions, clear subject
- Avoid overly polished/professional look — memes should feel organic

## Reference Files

- `references/templates.md` — Full template catalog with names, keywords, URLs, text positions
  - **Load this when**: User names a specific meme template, or you need to suggest templates
  - **Grep for**: template name, keyword, or Chinese name

- `scripts/meme_text.py` — Text overlay script
  - **Use this when**: Any text needs to be added to an image
  - Run directly, don't read into context unless debugging

## Tips

- **Long text**: The script auto-wraps, but keep meme text punchy — 4-6 words per line ideal
- **Image quality**: Templates should be at least 400px wide for readable text
- **Face placement**: Avoid placing text over people's faces
- **Trending memes**: When unsure of current trends, search web or check Reddit
- **Chinese font**: Liberation Sans supports CJK characters out of the box
- **Emoji in memes**: Can be included in text, but test rendering
