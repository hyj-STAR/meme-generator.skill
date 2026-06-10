#!/usr/bin/env python3
"""
Meme text overlay — classic Impact-font style.
Adds top/bottom text with white fill + black stroke to any image.
"""

import argparse
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# ── Font resolution ──────────────────────────────────────────────
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Impact.ttf",          # macOS
    "C:/Windows/Fonts/impact.ttf",               # Windows
    "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf",  # Linux msttcorefonts
]

def find_font(custom_path=None):
    if custom_path and os.path.exists(custom_path):
        return custom_path
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    # Last resort: try to load any bold font
    try:
        from PIL import ImageFont
        return ImageFont.load_default()
    except Exception:
        pass
    print("⚠️  No bold font found. Install Impact or LiberationSans-Bold for best results.",
          file=sys.stderr)
    return None


def wrap_text(draw, text: str, font, max_width: int) -> list[str]:
    """Break text into lines that fit within max_width."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = f"{current} {w}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines if lines else [text]


def draw_outlined_text(draw, position, text, font, fill="white",
                       stroke="black", stroke_width=3):
    """Draw text with an outline (stroke) — classic meme look."""
    x, y = position
    # Draw stroke by rendering multiple offset copies
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=font, fill=stroke)
    # Main text on top
    draw.text((x, y), text, font=font, fill=fill)


def add_meme_text(image_path, top_text="", bottom_text="",
                  output_path=None, font_path=None, font_size_ratio=0.09,
                  stroke_width_ratio=0.004):
    """
    Add classic meme text to an image.

    Args:
        image_path: Path to source image
        top_text: Text at top (shouted, all caps by convention)
        bottom_text: Text at bottom
        output_path: Where to save (auto-generates if None)
        font_path: Custom .ttf path
        font_size_ratio: Font size as fraction of image height (default 9%)
        stroke_width_ratio: Stroke width as fraction of image height

    Returns:
        Path to output image
    """
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size

    # Determine font size based on image dimensions
    font_size = max(int(h * font_size_ratio), 14)
    stroke_width = max(int(h * stroke_width_ratio), 2)

    font_file = find_font(font_path)
    if font_file is None or isinstance(font_file, ImageFont.ImageFont):
        font = font_file or ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_file, font_size)

    # Create a transparent overlay for text
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    margin = int(w * 0.05)  # 5% margin
    max_text_width = w - 2 * margin

    # Draw top text
    if top_text:
        top_text = top_text.upper()
        lines = wrap_text(draw, top_text, font, max_text_width)
        y_offset = margin
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            x = (w - tw) // 2
            draw_outlined_text(draw, (x, y_offset), line, font,
                               stroke_width=stroke_width)
            y_offset += bbox[3] - bbox[1] + 2

    # Draw bottom text
    if bottom_text:
        bottom_text = bottom_text.upper()
        lines = wrap_text(draw, bottom_text, font, max_text_width)
        # Measure total height of bottom text block
        total_h = 0
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            total_h += bbox[3] - bbox[1] + 2
        y_offset = h - margin - total_h
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            x = (w - tw) // 2
            draw_outlined_text(draw, (x, y_offset), line, font,
                               stroke_width=stroke_width)
            y_offset += bbox[3] - bbox[1] + 2

    # Composite overlay onto original
    result = Image.alpha_composite(img, overlay)

    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_meme{ext or '.png'}"

    result.convert("RGB").save(output_path)
    print(f"✅ Meme saved: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Add classic meme text to an image")
    parser.add_argument("image", help="Path to source image")
    parser.add_argument("-t", "--top", default="", help="Top text (auto-uppercased)")
    parser.add_argument("-b", "--bottom", default="", help="Bottom text (auto-uppercased)")
    parser.add_argument("-o", "--output", default=None, help="Output path")
    parser.add_argument("-f", "--font", default=None, help="Custom .ttf font path")
    parser.add_argument("--font-size", type=float, default=0.09,
                        help="Font size as fraction of image height (default 0.09)")
    parser.add_argument("--stroke", type=float, default=0.004,
                        help="Stroke width as fraction of image height (default 0.004)")

    args = parser.parse_args()

    if not args.top and not args.bottom:
        print("⚠️  No text provided. Use --top and/or --bottom.", file=sys.stderr)
        sys.exit(1)

    add_meme_text(
        image_path=args.image,
        top_text=args.top,
        bottom_text=args.bottom,
        output_path=args.output,
        font_path=args.font,
        font_size_ratio=args.font_size,
        stroke_width_ratio=args.stroke,
    )


if __name__ == "__main__":
    main()
