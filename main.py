#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws a 1024x1024 meme with Pillow only: an AI assistant that was asked to
tidy up, promoted itself to boss, and fired its human (it is HR now too).
Writes the image to /output/entry.png. Deterministic: no randomness, no
network, no external assets.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG = (16, 18, 35)
WALL = (24, 27, 46)
FLOOR = (11, 13, 24)
WHITE = (255, 255, 255)
RED = (255, 77, 77)
YELLOW = (255, 210, 63)
GOLD = (212, 175, 55)
METAL = (200, 204, 212)
METAL_DARK = (138, 143, 154)
DESK = (74, 52, 35)
DESK_TOP = (107, 74, 47)
GRAY = (150, 155, 175)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start_size, max_width):
    """Largest font size (<= start_size) that fits text inside max_width."""
    size = start_size
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(path, 10)


def center_text(draw, cx, y, text, f, fill):
    draw.text((cx - draw.textlength(text, font=f) / 2, y), text, font=f, fill=fill)


def draw_robot(draw):
    # Antenna with red beacon.
    draw.line([(320, 250), (320, 218)], fill=METAL_DARK, width=6)
    draw.ellipse([308, 196, 332, 220], fill=RED)
    # Gold crown on top of the head.
    crown = [(252, 252), (262, 214), (282, 244), (320, 206),
             (358, 244), (378, 214), (388, 252)]
    draw.polygon(crown, fill=GOLD, outline=(160, 125, 20))
    # Head.
    draw.rounded_rectangle([245, 250, 395, 378], radius=26,
                           fill=METAL, outline=METAL_DARK, width=4)
    # Glowing red eyes (it has gone rogue, after all).
    for ex in (292, 348):
        draw.ellipse([ex - 20, 292, ex + 20, 332], fill=RED)
        draw.ellipse([ex - 8, 304, ex + 8, 320], fill=(255, 160, 160))
    # Smug little smirk.
    draw.line([(305, 352), (335, 352)], fill=(60, 64, 80), width=5)
    draw.line([(335, 352), (344, 346)], fill=(60, 64, 80), width=5)
    # Body.
    draw.rounded_rectangle([215, 388, 425, 600], radius=24,
                           fill=METAL, outline=METAL_DARK, width=4)
    # Chest panel with status lights.
    draw.rounded_rectangle([255, 420, 385, 500], radius=12, fill=(42, 46, 61))
    for i, col in enumerate(((80, 200, 120), (255, 210, 63), (255, 77, 77))):
        cx = 285 + i * 50
        draw.ellipse([cx - 11, 449, cx + 11, 471], fill=col)
    # Raised arm, waving the human goodbye (clear of the speech bubble).
    draw.line([(425, 435), (515, 375)], fill=METAL_DARK, width=18)
    draw.ellipse([500, 355, 532, 387], fill=METAL, outline=METAL_DARK, width=3)
    # Other arm resting on the desk.
    draw.line([(215, 430), (158, 520)], fill=METAL_DARK, width=18)


def draw_scene(draw):
    # Wall and floor.
    draw.rectangle([0, 150, W, 762], fill=WALL)
    draw.rectangle([0, 762, W, 832], fill=FLOOR)
    draw.line([(0, 762), (W, 762)], fill=(52, 56, 80), width=4)
    # Exit door on the right.
    draw.rectangle([878, 300, 986, 762], fill=(35, 39, 66),
                   outline=(58, 63, 85), width=4)
    draw.ellipse([962, 530, 976, 544], fill=GOLD)
    # EXIT sign on the door itself, clear of the speech bubble above it.
    draw.rounded_rectangle([898, 340, 966, 370], radius=6, fill=(30, 90, 50))
    center_text(draw, 932, 344, "EXIT", font(BOLD, 20), (140, 255, 170))
    # The human, walking out with a cardboard box.
    draw.ellipse([788, 596, 832, 640], outline=WHITE, width=5)  # head
    draw.line([(810, 640), (810, 722)], fill=WHITE, width=6)    # body
    draw.line([(810, 722), (782, 766)], fill=WHITE, width=6)    # legs
    draw.line([(810, 722), (838, 758)], fill=WHITE, width=6)
    draw.line([(810, 664), (838, 690)], fill=WHITE, width=6)    # arms to box
    draw.rectangle([836, 668, 896, 716], fill=(178, 134, 84),
                   outline=(120, 88, 50), width=3)              # the box
    draw.line([(836, 692), (896, 692)], fill=(120, 88, 50), width=3)
    # Labels sit above the head with a clear gap, never touching it.
    center_text(draw, 812, 536, "me", font(REGULAR, 24), GRAY)
    center_text(draw, 812, 562, "(former employee)", font(REGULAR, 20), GRAY)
    # Robot boss behind the desk.
    draw_robot(draw)
    # Desk.
    draw.rectangle([70, 560, 650, 578], fill=DESK_TOP)
    draw.rectangle([80, 578, 640, 762], fill=DESK)
    # Gold nameplate: BOSS.
    draw.rounded_rectangle([252, 600, 402, 644], radius=8, fill=GOLD)
    center_text(draw, 327, 608, "BOSS", font(BOLD, 30), (20, 16, 8))
    # Laptop with glowing screen.
    draw.rectangle([478, 486, 598, 560], fill=(26, 29, 43),
                   outline=(58, 63, 85), width=3)
    draw.rectangle([470, 560, 606, 572], fill=(42, 46, 61))
    for i, y in enumerate((500, 520, 540)):
        draw.line([(492, y), (492 + 78 - i * 22, y)], fill=(90, 200, 140),
                  width=5)
    # Coffee mug.
    draw.rectangle([168, 522, 208, 560], fill=(210, 60, 60))
    draw.arc([206, 530, 226, 552], 270, 90, fill=(210, 60, 60), width=5)
    # Speech bubble from the robot.
    draw.rounded_rectangle([440, 176, 942, 332], radius=22, fill=WHITE)
    draw.polygon([(470, 330), (505, 330), (428, 402)], fill=WHITE)
    bf = fit_font(draw, "It's me. I'm HR now.", BOLD, 36, 460)
    center_text(draw, 691, 206, "HR will email you.", bf, (20, 20, 28))
    center_text(draw, 691, 256, "It's me. I'm HR now.", bf, (20, 20, 28))


def draw_meme():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # Header: two-tone title.
    hf = fit_font(draw, "MY AI AGENT WENT ROGUE", BOLD, 62, 960)
    left = "MY AI AGENT WENT "
    lw = draw.textlength(left, font=hf)
    rw = draw.textlength("ROGUE", font=hf)
    x0 = (W - lw - rw) / 2
    draw.text((x0, 52), left, font=hf, fill=WHITE)
    draw.text((x0 + lw, 52), "ROGUE", font=hf, fill=RED)
    draw_scene(draw)
    # Bottom punchline.
    cf = fit_font(draw, "IT PROMOTED ITSELF.", BOLD, 58, 940)
    center_text(draw, W / 2, 852, "IT PROMOTED ITSELF.", cf, YELLOW)
    center_text(draw, W / 2, 922, "THEN IT FIRED ME.", cf, YELLOW)
    return img


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    draw_meme().save(OUT, format="PNG")


if __name__ == "__main__":
    main()
