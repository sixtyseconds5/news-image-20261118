#!/usr/bin/env python3
"""Draw the 18 November 2026 newspaper poster and save it as entry.png.

A single-page front page, 1024x1024: navy masthead, one lead story with a
hand-drawn Shenzhen skyline, six grid stories each with a small flat
illustration, and an ALSO TODAY strip along the bottom. Everything is
drawn with Pillow shapes and DejaVu fonts; no image files are needed.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (247, 243, 234)
INK = (20, 24, 34)
NAVY = (18, 33, 61)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
GREY = (90, 96, 110)
DARK_SLATE = (44, 58, 88)

SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap measured with textlength; returns a list of lines."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def story_block(draw, x, y, width, kicker, headline, deck,
                kicker_size, head_size, deck_size):
    """One story block: red kicker, serif headline, two-line deck."""
    kf = font(SANS_BOLD, kicker_size)
    hf = font(SERIF_BOLD, head_size)
    df = font(SANS, deck_size)
    draw.text((x, y), kicker, font=kf, fill=RED)
    y += kicker_size + 8
    head_lines = wrap(draw, headline, hf, width)
    y = draw_lines(draw, head_lines, x, y, hf, INK, head_size + 5)
    y += 3
    deck_lines = wrap(draw, deck, df, width)[:2]
    draw_lines(draw, deck_lines, x, y, df, (58, 62, 74), deck_size + 5)
    return y


def lit_windows(draw, x, y, w, h, colour=(232, 196, 90)):
    """Scatter a few lit windows across a tower rectangle."""
    for row in range(2, h - 6, 14):
        for col in range(5, w - 5, 13):
            if (row * 7 + col * 3) % 5 == 0:
                draw.rectangle([x + col, y + row, x + col + 4, y + row + 5],
                               fill=colour)


def draw_lead_illustration(draw, x, y, w, h):
    """Shenzhen skyline at dusk, flags and a summit table below."""
    sky_h = h - 62
    draw.rectangle([x, y, x + w, y + sky_h], fill=(178, 198, 220))
    # Low sun, upper right.
    draw.ellipse([x + w - 78, y + 14, x + w - 22, y + 70], fill=(232, 178, 62))
    # Towers, left to right, with one tapered supertall in the middle.
    towers = [(0, 62, 52, 150), (56, 92, 46, 120), (106, 48, 48, 164),
              (200, 78, 46, 134), (250, 40, 52, 172), (306, 84, 46, 128),
              (356, 58, 48, 154), (408, 96, 22, 116)]
    for tx, ty, tw, th in towers:
        draw.rectangle([x + tx, y + ty, x + tx + tw, y + sky_h],
                       fill=DARK_SLATE)
        lit_windows(draw, x + tx, y + ty, tw, th)
    # Tapered supertall tower.
    cx = x + 178
    draw.polygon([(cx - 26, y + sky_h), (cx - 14, y + 18),
                  (cx + 14, y + 18), (cx + 26, y + sky_h)],
                 fill=(30, 40, 66))
    for wy in range(y + 30, y + sky_h - 8, 16):
        draw.rectangle([cx - 8, wy, cx + 8, wy + 5], fill=(232, 196, 90))
    draw.rectangle([cx - 2, y + 8, cx + 2, y + 18], fill=(30, 40, 66))
    # Flag band.
    fy = y + sky_h
    draw.rectangle([x, fy, x + w, y + h - 22], fill=(233, 226, 208))
    flag_w, flag_h = 132, 30
    # United States: stripes with a blue canton.
    fx = x + 8
    for i in range(7):
        draw.rectangle([fx, fy + 4 + i * 4, fx + flag_w, fy + 8 + i * 4],
                       fill=(178, 34, 34) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([fx, fy + 4, fx + 52, fy + 16], fill=(28, 48, 96))
    # China: red field, one large gold disc and small stars.
    fx = x + 148
    draw.rectangle([fx, fy + 4, fx + flag_w, fy + 4 + flag_h], fill=(222, 41, 16))
    draw.ellipse([fx + 14, fy + 10, fx + 34, fy + 30], fill=(255, 222, 0))
    for sx, sy in [(52, 10), (66, 16), (66, 26), (52, 30)]:
        draw.ellipse([fx + sx, fy + sy, fx + sx + 5, fy + sy + 5],
                     fill=(255, 222, 0))
    # Russia: white, blue and red horizontal bands.
    fx = x + 288
    for i, colour in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([fx, fy + 4 + i * 10, fx + flag_w, fy + 14 + i * 10],
                       fill=colour)
    # Summit table with three microphones.
    ty = y + h - 18
    draw.rectangle([x + 8, ty, x + w - 8, ty + 10], fill=(110, 72, 40))
    for mx in (x + 78, x + 215, x + 352):
        draw.line([mx, ty, mx, ty - 16], fill=INK, width=2)
        draw.ellipse([mx - 5, ty - 22, mx + 5, ty - 12], fill=INK)


def draw_nvidia(draw, x, y, w, h):
    """Server rack above a graphics card, with the big revenue figure."""
    draw.rectangle([x, y, x + w, y + h], fill=(8, 28, 20))
    # Server rack: rows of green status lights.
    draw.rectangle([x + 10, y + 8, x + w - 10, y + 40], outline=(90, 200, 120),
                   width=2)
    for row in range(3):
        for col in range(12):
            draw.rectangle([x + 16 + col * 22, y + 13 + row * 9,
                            x + 21 + col * 22, y + 18 + row * 9],
                           fill=(110, 230, 140))
    # Graphics card with three fans.
    draw.rectangle([x + 10, y + 46, x + w - 10, y + 74], outline=(110, 230, 140),
                   width=2)
    for cx in (x + 52, x + w // 2, x + w - 52):
        draw.ellipse([cx - 13, y + 50, cx + 13, y + 70],
                     outline=(110, 230, 140), width=2)
        draw.ellipse([cx - 3, y + 58, cx + 3, y + 64], fill=(110, 230, 140))
    fnt = font(SANS_BOLD, 27)
    text = "$115.84bn"
    tw = draw.textlength(text, font=fnt)
    draw.text((x + (w - tw) / 2, y + 78), text, font=fnt, fill=(110, 230, 140))


def draw_tanker(draw, x, y, w, h):
    """A tanker at sea under a radar dome, with interception bursts."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 44, 74))
    draw.rectangle([x, y + 74, x + w, y + h], fill=(10, 30, 54))
    # Radar dome arcs, upper left, concentric on the dome centre.
    rcx, rcy = x + 48, y + 58
    for r in (66, 52, 38):
        draw.arc([rcx - r, rcy - r, rcx + r, rcy + r],
                 start=205, end=335, fill=(232, 196, 90), width=3)
    draw.pieslice([x + 18, y + 40, x + 78, y + 76], start=180, end=360,
                  fill=(210, 220, 230))
    # Tanker hull and bridge.
    draw.rectangle([x + 84, y + 66, x + w - 14, y + 88], fill=(12, 12, 14))
    draw.rectangle([x + w - 66, y + 48, x + w - 30, y + 66], fill=(220, 220, 220))
    draw.rectangle([x + w - 60, y + 40, x + w - 36, y + 48], fill=(200, 60, 40))
    # Orange interception bursts and white missile trails.
    for bx, by, br in [(x + 190, y + 34, 11), (x + 236, y + 52, 9),
                       (x + 152, y + 20, 8)]:
        draw.ellipse([bx - br, by - br, bx + br, by + br],
                     fill=(245, 140, 30))
        draw.ellipse([bx - br // 2, by - br // 2, bx + br // 2, by + br // 2],
                     fill=(255, 210, 90))
    draw.line([x + 152, y + 20, x + 120, y + 52], fill=(255, 255, 255), width=2)
    draw.line([x + 236, y + 52, x + 262, y + 24], fill=(255, 255, 255), width=2)


def draw_parliament(draw, x, y, w, h):
    """Parliament building: dome, columns, Latvian flag on the dome."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    # Dome.
    draw.pieslice([x + w // 2 - 46, y + 2, x + w // 2 + 46, y + 66],
                  start=180, end=360, fill=(110, 126, 150))
    draw.rectangle([x + w // 2 - 2, y - 2, x + w // 2 + 2, y + 8], fill=GOLD)
    # Latvian flag on the dome: dark red, white, dark red.
    fx, fy = x + w // 2 + 14, y + 2
    draw.rectangle([fx, fy, fx + 34, fy + 5], fill=(155, 30, 40))
    draw.rectangle([fx, fy + 5, fx + 34, fy + 8], fill=(255, 255, 255))
    draw.rectangle([fx, fy + 8, fx + 34, fy + 13], fill=(155, 30, 40))
    # Entablature, columns and base.
    draw.rectangle([x + 14, y + 52, x + w - 14, y + 64], fill=(150, 142, 126))
    for i in range(6):
        cx = x + 28 + i * 50
        draw.rectangle([cx, y + 64, cx + 16, y + 96], fill=(245, 242, 234))
    draw.rectangle([x + 14, y + 96, x + w - 14, y + h - 4], fill=(150, 142, 126))


def draw_globe(draw, x, y, w, h):
    """A globe with red impact dots and small drone silhouettes."""
    draw.rectangle([x, y, x + w, y + h], fill=(222, 230, 224))
    cx, cy, r = x + w // 2, y + h // 2 + 4, 38
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 150, 205))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(40, 80, 140),
                 width=2)
    # Rough land masses.
    draw.ellipse([cx - 26, cy - 22, cx - 2, cy + 2], fill=(96, 180, 110))
    draw.ellipse([cx + 4, cy + 6, cx + 28, cy + 28], fill=(96, 180, 110))
    draw.ellipse([cx + 10, cy - 26, cx + 26, cy - 8], fill=(120, 190, 120))
    # Red impact dots with white rings.
    for dx, dy in [(cx - 16, cy - 12), (cx + 14, cy + 2), (cx - 4, cy + 18)]:
        draw.ellipse([dx - 8, dy - 8, dx + 8, dy + 8], fill=(255, 255, 255))
        draw.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=(200, 30, 30))
    # Drone silhouettes: small dark crosses with rotor bars.
    for dx, dy in [(x + 22, y + 16), (x + w - 26, y + 14)]:
        draw.rectangle([dx - 14, dy - 2, dx + 14, dy + 2], fill=INK)
        draw.rectangle([dx - 2, dy - 7, dx + 2, dy + 7], fill=INK)
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=INK)


def draw_cyclone(draw, x, y, w, h):
    """Cyclone spiral over the sea, coastline, track arrow toward land."""
    draw.rectangle([x, y, x + w, y + h], fill=(182, 208, 228))
    draw.rectangle([x, y + 72, x + w, y + h], fill=(28, 84, 140))
    # Coastline: green land sweeping in from the lower left.
    draw.polygon([(x, y + h), (x, y + 88), (x + 90, y + 78),
                  (x + 150, y + 92), (x + 170, y + h)], fill=(150, 178, 110))
    # Spiral: concentric arcs in white and pale blue.
    cx, cy = x + w // 2 + 28, y + 52
    for r, colour in [(46, (255, 255, 255)), (36, (210, 228, 244)),
                      (26, (255, 255, 255)), (16, (30, 90, 150)),
                      (7, (255, 255, 255))]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=4)
    # Track arrow pointing down-left toward the coastline.
    draw.line([cx - 30, cy + 34, x + 96, y + 84], fill=(255, 255, 255), width=3)
    draw.polygon([(x + 96, y + 84), (x + 110, y + 80), (x + 102, y + 94)],
                 fill=(255, 255, 255))


def draw_washington(draw, x, y, w, h):
    """Washington skyline: Capitol dome, Monument, warning triangle."""
    draw.rectangle([x, y, x + w, y + h], fill=(198, 214, 232))
    draw.ellipse([x + w - 52, y + 6, x + w - 18, y + 40], fill=(232, 178, 62))
    # Washington Monument, left.
    draw.polygon([(x + 34, y + 96), (x + 46, y + 22), (x + 58, y + 96)],
                 fill=(170, 176, 184))
    # Capitol: base, columns, white dome.
    draw.rectangle([x + 96, y + 78, x + w - 92, y + 96], fill=(245, 242, 234))
    for i in range(5):
        cx = x + 106 + i * 28
        draw.rectangle([cx, y + 62, cx + 10, y + 78], fill=(245, 242, 234))
    draw.rectangle([x + 96, y + 56, x + w - 92, y + 64], fill=(245, 242, 234))
    draw.pieslice([x + 150, y + 6, x + 226, y + 62], start=180, end=360,
                  fill=(255, 255, 255))
    draw.rectangle([x + 186, y + 0, x + 190, y + 10], fill=GOLD)
    # Green ground strip.
    draw.rectangle([x, y + 96, x + w, y + h], fill=(110, 150, 96))
    # Yellow warning triangle with an exclamation mark.
    tx, ty = x + w - 66, y + 58
    draw.polygon([(tx, ty), (tx + 52, ty), (tx + 26, ty + 44)],
                 fill=(240, 200, 30), outline=INK)
    draw.rectangle([tx + 24, ty + 12, tx + 28, ty + 30], fill=INK)
    draw.ellipse([tx + 23, ty + 33, tx + 29, ty + 39], fill=INK)


STORIES = [
    ("TECHNOLOGY", "Nvidia doubles sales; Board bars Huang",
     "Revenue $115.84bn, up 103%. Next: $130bn.", draw_nvidia),
    ("MIDDLE EAST", "Gulf on edge after drone scares",
     "Kuwait intercepts drones; Bahrain on alert.", draw_tanker),
    ("EUROPE", "Latvia approves a new government",
     "Saeima backs Kulbergs 57-34; his second cabinet.", draw_parliament),
    ("THE TOLL OF WAR", "UN: 372 killed in Ukraine in October",
     "Plus 1,981 hurt. In Sudan, 2,230 dead this year.", draw_globe),
    ("WEATHER", "Cyclone Akvan nears India's east coast",
     "Severe storm; landfall due Friday, 20 November.", draw_cyclone),
    ("UNITED STATES", "Iran plot 'taken very seriously'",
     "CNN reports a dirty-bomb plan; Iran denies it.", draw_washington),
]

STRIP_TEXT = ("Dhoni retires from the IPL, to mentor Chennai \u00b7 "
              "Amazon's $7bn for Indian renewables \u00b7 India re-elected "
              "to the ITU Council \u00b7 Trump deposition due by 22 January "
              "in $10bn BBC case")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead: navy bar, serif title, gold rule, gold date line.
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    title = font(SERIF_BOLD, 54)
    text = "THE WORLD IN ONE DAY"
    tw = draw.textlength(text, font=title)
    draw.text(((W - tw) / 2, 16), text, font=title, fill=(247, 243, 234))
    draw.line([32, 84, W - 32, 84], fill=GOLD, width=2)
    date_f = font(SANS_BOLD, 22)
    date_text = "WEDNESDAY \u00b7 18 NOVEMBER 2026"
    dw = draw.textlength(date_text, font=date_f)
    draw.text(((W - dw) / 2, 90), date_text, font=date_f, fill=GOLD)

    # Lead story: illustration left, text right.
    draw_lead_illustration(draw, 32, 132, 430, 248)
    story_block(draw, 482, 134, 510, "ASIA \u00b7 APEC",
                "APEC opens in Shenzhen as Trump lands in China",
                "Xi opens the summit as Trump lands. A Trump-Xi-Putin "
                "meeting is due Thursday.", 20, 34, 23)

    # Rule, then the 2 x 3 grid.
    draw.line([32, 396, W - 32, 396], fill=GREY, width=1)
    col_w = 308
    col_x = [32, 358, 684]
    row_y = [410, 668]
    for i, (kicker, headline, deck, artist) in enumerate(STORIES):
        row, col = divmod(i, 3)
        x = col_x[col]
        y = row_y[row]
        artist(draw, x, y, col_w, 108)
        story_block(draw, x, y + 120, col_w, kicker, headline, deck,
                    16, 25, 21)

    # Rule, then the ALSO TODAY strip at the bottom.
    draw.line([32, 928, W - 32, 928], fill=GREY, width=1)
    strip_f = font(SANS, 17)
    label_f = font(SANS_BOLD, 17)
    label = "ALSO TODAY  "
    lw = draw.textlength(label, font=label_f)
    draw.text((32, 942), label, font=label_f, fill=RED)
    strip_lines = wrap(draw, STRIP_TEXT, strip_f, W - 64 - lw)[:2]
    draw_lines(draw, strip_lines, 32 + lw, 942, strip_f, INK, 22)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
