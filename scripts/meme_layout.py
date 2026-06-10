#!/usr/bin/env python3
"""
Compose platform-native meme layouts.

This is for "网感" layouts where the outer shell matters: fake X screenshots,
sticker-store screenshots, and ugly tech collage cards.
"""

import argparse
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


FONT_CANDIDATES = [
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]


def font(size: int):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fit_text(draw, text, max_width, start_size, min_size=22):
    size = start_size
    while size >= min_size:
        f = font(size)
        bbox = draw.textbbox((0, 0), text, font=f)
        if bbox[2] - bbox[0] <= max_width:
            return f
        size -= 2
    return font(min_size)


def draw_centered(draw, box, text, fill, start_size):
    x1, y1, x2, y2 = box
    f = fit_text(draw, text, x2 - x1, start_size)
    bbox = draw.textbbox((0, 0), text, font=f)
    x = x1 + (x2 - x1 - (bbox[2] - bbox[0])) // 2
    y = y1 + (y2 - y1 - (bbox[3] - bbox[1])) // 2
    draw.text((x, y), text, font=f, fill=fill)


def draw_text_lines(draw, xy, text, fill, size, max_width, line_gap=8):
    lines = []
    f = font(size)
    for raw_line in text.splitlines() or [text]:
        words = list(raw_line) if " " not in raw_line else raw_line.split(" ")
        current = ""
        for token in words:
            test = current + token if " " not in raw_line else f"{current} {token}".strip()
            bbox = draw.textbbox((0, 0), test, font=f)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = token
        if current:
            lines.append(current)
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += size + line_gap
    return y


def paste_cover(canvas, image, box):
    x1, y1, x2, y2 = box
    target_w, target_h = x2 - x1, y2 - y1
    img = image.convert("RGB")
    scale = max(target_w / img.width, target_h / img.height)
    resized = img.resize((int(img.width * scale), int(img.height * scale)))
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    cropped = resized.crop((left, top, left + target_w, top + target_h))
    canvas.paste(cropped, (x1, y1))


def sticker_layout(input_path, output_path, caption):
    w, h = 1256, 2760
    canvas = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(canvas)
    img = Image.open(input_path).convert("RGB")
    img.thumbnail((620, 620))
    x = (w - img.width) // 2
    y = 1130 - img.height // 2
    canvas.paste(img, (x, y))

    bar_w, bar_h = 680, 88
    bx = (w - bar_w) // 2
    by = y + img.height - 40
    draw.rectangle((bx, by, bx + bar_w, by + bar_h), fill="#C9302C")
    draw_centered(draw, (bx + 22, by + 8, bx + bar_w - 22, by + bar_h - 8), caption, "white", 46)

    button_w, button_h = 460, 104
    btx = (w - button_w) // 2
    bty = 2030
    draw.rounded_rectangle((btx, bty, btx + button_w, bty + button_h), radius=52, fill="#F23B50")
    draw_centered(draw, (btx, bty, btx + button_w, bty + button_h), "添加表情", "white", 42)
    canvas.save(output_path, quality=94)


def x_screenshot_layout(input_path, output_path, title, punchline, handle="@meme_skill"):
    w, h = 1256, 2760
    canvas = Image.new("RGB", (w, h), "black")
    draw = ImageDraw.Draw(canvas)

    draw.text((78, 54), "19:15", font=font(42), fill="white")
    draw.text((70, 210), "←", font=font(72), fill="white")
    draw.ellipse((74, 390, 174, 490), fill="#F2F2F2")
    draw.text((204, 392), "Meme Skill", font=font(44), fill="white")
    draw.text((204, 452), handle, font=font(34), fill="#C8C8C8")
    draw.rounded_rectangle((950, 394, 1160, 478), radius=42, outline="white", width=3)
    draw_centered(draw, (950, 394, 1160, 478), "关注", "white", 36)

    card_y = 880
    card_h = 860
    draw.rectangle((0, card_y, w, card_y + card_h), fill="white")
    draw_text_lines(draw, (0, card_y + 18), title, "black", 48, w - 40, line_gap=6)

    image_box = (0, card_y + 220, w, card_y + card_h)
    img = Image.open(input_path)
    paste_cover(canvas, img, image_box)

    label_w, label_h = 370, 92
    lx, ly = 820, image_box[1] + 26
    draw.rectangle((lx, ly, lx + label_w, ly + label_h), fill="#F6D84D")
    draw_centered(draw, (lx + 12, ly + 8, lx + label_w - 12, ly + label_h - 8), punchline, "black", 36)

    footer_y = 2330
    draw.text((66, footer_y), "reply 7", font=font(36), fill="white")
    draw.text((330, footer_y), "repost 25", font=font(36), fill="white")
    draw.text((640, footer_y), "like 619", font=font(36), fill="white")
    draw.text((930, footer_y), "views 3.5K", font=font(36), fill="white")
    draw.text((66, 2520), "发布你的回复", font=font(38), fill="#777777")
    canvas.save(output_path, quality=94)


def main():
    parser = argparse.ArgumentParser(description="Compose platform-native meme layouts")
    parser.add_argument("image", help="Input image")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--style", choices=["sticker", "x-screenshot"], required=True)
    parser.add_argument("--caption", default="老实人被暗箭所伤")
    parser.add_argument("--title", default="普通宣传：写卖点\\n技术圈宣传：做成烂梗")
    parser.add_argument("--punchline", default="咔咔就是干！！！")
    parser.add_argument("--handle", default="@meme_skill")
    args = parser.parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    if args.style == "sticker":
        sticker_layout(args.image, args.output, args.caption)
    else:
        x_screenshot_layout(args.image, args.output, args.title.replace("\\n", "\n"), args.punchline, args.handle)
    print(f"Saved meme layout: {args.output}")


if __name__ == "__main__":
    main()
