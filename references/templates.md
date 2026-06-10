# Meme Templates Encyclopedia

Below is a catalog of popular meme templates. When a user asks for a specific meme by name,
use this reference to find the template image and where to place text.

## Template Format
Each entry:
- **Name**: How users refer to it
- **Keywords**: Alternative names / search terms
- **Imgflip ID**: Template ID on imgflip.com (most reliable source)
- **Text fields**: Where text goes (positions as [x%, y%] of image)
- **Best for**: What the template expresses

---

## Top Templates

### Drake Hotline Bling
- **Keywords**: drake, drake meme, hotline bling, 德雷克
- **Imgflip ID**: 181913649
- **URL**: https://i.imgflip.com/30b1gx.jpg
- **Text fields**:
  - top (rejected thing): center, ~top 15%
  - bottom (preferred thing): center, ~bottom 15%
- **Best for**: Choosing between two options, preferring one over another

### Distracted Boyfriend
- **Keywords**: distracted boyfriend, guy looking back, 分心男友
- **Imgflip ID**: 112126428
- **URL**: https://i.imgflip.com/1ur9b0.jpg
- **Text fields**:
  - Text on girlfriend (right side, ~20% from right, ~40% down)
  - Text on other woman (left side, ~20% from left, ~40% down)
  - Text on boyfriend (center, ~30% down)
- **Best for**: Being tempted by something new while ignoring existing thing

### Two Buttons
- **Keywords**: two buttons, sweating choice, 两个按钮, 艰难选择
- **Imgflip ID**: 87743020
- **URL**: https://i.imgflip.com/1g8my4.jpg
- **Text fields**:
  - Left button: bottom-left area
  - Right button: bottom-right area
  - *(Better as AI variant with custom text positioning)*
- **Best for**: Difficult choices, anxiety about decisions

### Change My Mind
- **Keywords**: change my mind, steven crowder, 改变我的想法
- **Imgflip ID**: 129242436
- **URL**: https://i.imgflip.com/24y43o.jpg
- **Text fields**:
  - Sign text: center of signboard (~center, ~60% down)
- **Best for**: Unpopular opinions, hot takes

### One Does Not Simply
- **Keywords**: one does not simply, boromir, lotr, 不能简单
- **Imgflip ID**: 61579
- **URL**: https://i.imgflip.com/1bij.jpg
- **Text fields**:
  - Top: "ONE DOES NOT SIMPLY"
  - Bottom: the actual task/thing
- **Best for**: Things that are harder than they seem

### Expanding Brain / Galaxy Brain
- **Keywords**: expanding brain, galaxy brain, brain meme, 大脑升级
- **Imgflip ID**: 93895088
- **URL**: https://i.imgflip.com/1jwhww.jpg
- **Text fields**: Usually 4 panels, text placed beside each brain
- **Best for**: Progressively absurd/hot takes, evolution of an idea

### Bernie Sanders Mittens
- **Keywords**: bernie, bernie sanders, mittens, once again asking, 伯尼桑德斯
- **Imgflip ID**: 222403160
- **URL**: https://i.imgflip.com/4t0m3k.jpg
- **Text fields**: Top/bottom classic meme text
- **Best for**: Reluctant requests, "I am once again asking..."

### This Is Fine (Dog in Fire)
- **Keywords**: this is fine, dog fire, 问题不大, 还行
- **Imgflip ID**: 55347173 (or search for "this is fine dog")
- **URL**: Can be generated better with AI
- **Text fields**: Top text only, or no text (image speaks for itself)
- **Best for**: Everything falling apart but pretending it's okay

### Woman Yelling at Cat
- **Keywords**: woman yelling cat, screaming cat, 女人吼猫
- **Imgflip ID**: 188390779 (woman) + 144575951 (cat, search "smudge the cat")
- **Text fields**:
  - Left panel (woman): text near the yelling woman
  - Right panel (cat): text near the confused cat
- **Best for**: Arguments, misunderstandings, someone overreacting

### Roll Safe / Think About It
- **Keywords**: roll safe, think about it, tapping head, 聪明
- **Imgflip ID**: 89370399
- **URL**: https://i.imgflip.com/1h7in3.jpg
- **Text fields**: Top/bottom classic format
- **Best for**: "Clever" but actually stupid solutions

### Surprised Pikachu
- **Keywords**: surprised pikachu, shocked pikachu, 皮卡丘惊讶
- **Imgflip ID**: 155067746
- **URL**: https://i.imgflip.com/2kbn1h.jpg
- **Text fields**: Top text (setup), bottom text (obvious outcome)
- **Best for**: Being shocked by predictable outcomes

### Gru's Plan
- **Keywords**: gru plan, gru presentation, 格鲁计划
- **Imgflip ID**: 131940431 (4-panel version)
- **URL**: https://i.imgflip.com/26amvb.jpg
- **Text fields**: Each panel gets text overlay
- **Best for**: Plans going progressively wrong

### Waiting Skeleton
- **Keywords**: waiting skeleton, skeleton computer, skeleton waiting
- **Imgflip ID**: search "waiting skeleton" or "skeleton at computer"
- **Best for**: Waiting forever, abandoned projects, OP never delivered

### Monkey Puppet
- **Keywords**: monkey puppet, side eye monkey, 猴子木偶
- **Imgflip ID**: 148909805
- **URL**: https://i.imgflip.com/2gn1hx.jpg
- **Text fields**: Top/bottom format
- **Best for**: Awkward situations, being caught

### Always Has Been (Astronaut Gun)
- **Keywords**: always has been, astronaut gun, 一直都是
- **Best for**: AI generation — two astronauts, one with gun
- **Text fields**: "Wait it's all X?" / "Always has been."

---

## Chinese Internet Memes (中文梗)

### 熊猫头 (Panda Head)
- **Keywords**: 熊猫头, panda head meme, 表情包
- **Best for**: AI generation — crude panda face drawing
- **Text fields**: Top/bottom or speech bubble style

### 地铁老人看手机 (Old Man Looking at Phone on Subway)
- **Keywords**: 地铁老人, confused old man phone, grandpa phone
- **Best for**: Confusion, disbelief, "wtf is this"

### 真香 (Zhen Xiang — "So Fragrant")
- **Keywords**: 真香, 王境泽, so fragrant
- **Best for**: Hypocrisy, going back on your word

### 我全都要 (I Want It All)
- **Keywords**: 我全都要, 徐锦江, i want all
- **Best for**: Greed, wanting everything

---

## Using Templates

### Method 1: Imgflip API (recommended for known templates)
```
https://api.imgflip.com/caption_image
  ?template_id={ID}
  &username={IMGFLIP_USER}
  &password={IMGFLIP_PASS}
  &text0=top text
  &text1=bottom text
```

Credentials can be stored in environment variables `IMGFLIP_USER` and `IMGFLIP_PASS`.
Free account at https://imgflip.com/signup

### Method 2: Download + meme_text.py
1. Download the template image
2. Use `scripts/meme_text.py` to overlay text

### Method 3: AI Generation
For templates without a good source image, or when user wants original meme,
use the `image_generate` tool to create the base image, then add text.

---

## Meme Site Sources

### Top Sources
1. **Imgflip** — Largest meme template database + API
   - Template search: https://imgflip.com/memetemplates
   - API docs: https://imgflip.com/api
2. **Know Your Meme** — Encyclopedia of meme origins
   - https://knowyourmeme.com
3. **Reddit** — /r/memes, /r/dankmemes, /r/MemeTemplatesOfficial
4. **Make a Meme** — https://makeameme.org (another generator)

### Chinese Meme Sources
- **微博/小红书** — Search trends + current Chinese meme trends
- **Bilibili 弹幕** — Rich source of evolving Chinese internet culture
- **百度贴吧** — Classic Chinese meme birthplace (especially 戒赌吧, 李毅吧)
