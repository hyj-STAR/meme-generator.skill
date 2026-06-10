#!/usr/bin/env python3
"""
Meme text overlay — classic Impact-font style.
Adds top/bottom text with white fill + black stroke to any image.
"""

import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ModuleNotFoundError as exc:
    if exc.name != "PIL":
        raise
    print(
        "Missing dependency: Pillow. Install it with:\n"
        "  python3 -m pip install -r requirements.txt\n"
        "or:\n"
        "  python3 -m pip install Pillow",
        file=sys.stderr,
    )
    sys.exit(1)

# ── Font resolution ──────────────────────────────────────────────
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Impact.ttf",          # macOS
    "/System/Library/Fonts/PingFang.ttc",        # macOS CJK
    "/System/Library/Fonts/STHeiti Light.ttc",   # macOS CJK fallback
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
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
    if " " not in text.strip():
        lines = []
        current = ""
        for char in text:
            test = f"{current}{char}"
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = char
        if current:
            lines.append(current)
        return lines if lines else [text]

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
                  stroke_width_ratio=0.004, fill="white", stroke_fill="black",
                  top_y=None, bottom_y=None, uppercase=True):
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
        fill: Text fill color
        stroke_fill: Text outline color
        top_y: Optional top text y-position as fraction of image height
        bottom_y: Optional bottom text y-position as fraction of image height
        uppercase: Uppercase text for classic English memes

    Returns:
        Path to output image
    """
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size

    # Determine font size based on image dimensions
    font_size = max(int(h * font_size_ratio), 14)
    stroke_width = max(int(h * stroke_width_ratio), 2)

    font_file = find_font(font_path)
    if font_file is None or not isinstance(font_file, (str, bytes, os.PathLike)):
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
        if uppercase:
            top_text = top_text.upper()
        lines = wrap_text(draw, top_text, font, max_text_width)
        y_offset = int(h * top_y) if top_y is not None else margin
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            x = (w - tw) // 2
            draw_outlined_text(draw, (x, y_offset), line, font,
                               fill=fill, stroke=stroke_fill,
                               stroke_width=stroke_width)
            y_offset += bbox[3] - bbox[1] + 2

    # Draw bottom text
    if bottom_text:
        if uppercase:
            bottom_text = bottom_text.upper()
        lines = wrap_text(draw, bottom_text, font, max_text_width)
        # Measure total height of bottom text block
        total_h = 0
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            total_h += bbox[3] - bbox[1] + 2
        y_offset = int(h * bottom_y) if bottom_y is not None else h - margin - total_h
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            x = (w - tw) // 2
            draw_outlined_text(draw, (x, y_offset), line, font,
                               fill=fill, stroke=stroke_fill,
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
    parser.add_argument("-t", "--top", default="", help="Top text")
    parser.add_argument("-b", "--bottom", default="", help="Bottom text")
    parser.add_argument("-o", "--output", default=None, help="Output path")
    parser.add_argument("-f", "--font", default=None, help="Custom .ttf font path")
    parser.add_argument("--font-size", type=float, default=0.09,
                        help="Font size as fraction of image height (default 0.09)")
    parser.add_argument("--stroke", type=float, default=0.004,
                        help="Stroke width as fraction of image height (default 0.004)")
    parser.add_argument("--fill", default="white", help="Text fill color (default: white)")
    parser.add_argument("--stroke-fill", default="black",
                        help="Text outline color (default: black)")
    parser.add_argument("--top-y", type=float, default=None,
                        help="Top text y-position as fraction of image height")
    parser.add_argument("--bottom-y", type=float, default=None,
                        help="Bottom text y-position as fraction of image height")
    parser.add_argument("--no-uppercase", action="store_true",
                        help="Keep text casing. Recommended for Chinese memes.")

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
        fill=args.fill,
        stroke_fill=args.stroke_fill,
        top_y=args.top_y,
        bottom_y=args.bottom_y,
        uppercase=not args.no_uppercase,
    )


if __name__ == "__main__":
    main()
