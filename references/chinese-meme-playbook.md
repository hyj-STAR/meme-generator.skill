# Chinese Meme Playbook

中文梗图优先做“情绪共鸣”，不是只做英文 meme 的直译。

## Core Ingredients

1. **模板**
   - 经典模板：熊猫头、地铁老人、真香、我全都要、黑人问号、猫猫震惊、打工人发疯。
   - 平台模板：小红书封面式大字、朋友圈吐槽截图、聊天记录反转、老板/员工对话。
   - AI 生成模板：当没有合适版权安全素材时，生成原创夸张表情底图。

2. **文案**
   - 中文平台更适合短句、反转、阴阳怪气和生活场景。
   - 常用结构：
     - “本来只是想 X / 结果开始 Y”
     - “嘴上说 X / 身体已经 Y”
     - “别人用 AI：X / 我用 AI：Y”
     - “老板：X / 我：Y”
     - “以为是 X / 实际是 Y”

3. **热点**
   - 实时热点不要硬编码进 skill。
   - 每次生成前先搜索或读取当天热词，再改写成用户场景。
   - 推荐来源：小红书搜索建议、微博热搜、B 站热榜、知乎热榜、即刻/X 话题。
   - 输出时标注热点日期，避免旧梗装新梗。
   - 先用 `scripts/trend_scraper.py` 抓公开趋势信号，再让 `meme_brain.py` 改写文案。
   - X/Twitter 不要默认硬爬。优先官方 API、用户授权 cookie/token、或托管采集服务；否则稳定性会很差。

4. **排版**
   - 中文梗图不一定要全大写，通常保留原文。
   - 小红书封面式：大字号、高对比、黄/红/白字、黑描边。
   - 表情包式：白字黑边或黑字白底，短句居中。
   - 对话式：文字尽量贴近角色或放在空白气泡里。

## Layout Presets

Use `scripts/meme_text.py` options:

```bash
python3 scripts/meme_text.py input.png \
  --no-uppercase \
  --fill "#FFD84D" \
  --stroke-fill "#111111" \
  --font-size 0.075 \
  --top-y 0.08 \
  --bottom-y 0.76 \
  -t "本来只是想做个小工具" \
  -b "结果开始研究怎么引流"
```

### Preset: 小红书大字封面

- `--no-uppercase`
- `--fill "#FFD84D"` or `"#FF4D4D"`
- `--stroke-fill "#111111"`
- `--font-size 0.07` to `0.10`
- Keep text to 10-18 Chinese characters per line.

### Preset: Classic 表情包

- `--no-uppercase`
- `--fill "white"`
- `--stroke-fill "black"`
- `--font-size 0.08` to `0.11`
- Top and bottom text only.

### Preset: Screenshot Roast

- Use black text on white/cream blocks when the base image already has speech bubbles.
- Avoid covering faces.
- Prefer two short lines over one long sentence.

## Generation Flow

1. Identify user scene:
   - AI tool, work, study, money, relationship, productivity, anxiety, boss/client.
2. Choose meme angle:
   - self-roast, contrast, reversal, absurd seriousness, fake calm, social death.
3. Choose template:
   - known template if user names one;
   - generated Chinese reaction image if no safe/clean template exists.
4. Generate 5 captions:
   - at least one direct roast;
   - one absurd formal version;
   - one Xiaohongshu-style version;
   - one workplace version;
   - one AI/coding version.
5. Render 1-3 final images.

## Caption Seeds For AI Tool Promotion

- 本来只是想做个小工具 / 结果开始研究怎么引流
- 别人开源项目：技术交流 / 我开源项目：求求你点个星
- 说好不做内容营销 / 已经开始排 30 天选题
- AI 帮我省了 3 小时 / 我花 5 小时研究怎么发出去
- 工具还没火 / 人已经开始商业化焦虑
