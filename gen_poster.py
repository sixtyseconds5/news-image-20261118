"""Draw the 18 November 2026 world-news poster (1024x1024 PNG).

Every story below is a real event reported on Wednesday 18 November 2026
(sources: The Guardian, Hindustan Times, EIN Presswire, Jagran Josh,
The Times of India). The image is rendered once, locally, and committed
as entry.png; main.py only copies it to the grader's output directory.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 24, 34)
NAVY = (18, 33, 61)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
GREY = (90, 96, 110)
RULE = (180, 175, 160)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_text_block(draw, x, y, width, kicker, headline, deck,
                    kicker_size=17, head_size=25, deck_size=19,
                    head_font=SERIF_B, max_head_lines=3, max_deck_lines=4):
    """Kicker + headline + deck; returns the y below the block."""
    kf, hf, df = font(SANS_B, kicker_size), font(head_font, head_size), font(SANS, deck_size)
    draw.text((x, y), kicker, font=kf, fill=RED)
    y += kicker_size + 8
    for ln in wrap(draw, headline, hf, width)[:max_head_lines]:
        draw.text((x, y), ln, font=hf, fill=INK)
        y += head_size + 4
    y += 2
    for ln in wrap(draw, deck, df, width)[:max_deck_lines]:
        draw.text((x, y), ln, font=df, fill=(52, 56, 66))
        y += deck_size + 5
    return y


# ---------- small flat illustrations ----------

def ill_bridge(d, x, y, w, h):
    """Kerch bridge over the strait, blast plume on the deck."""
    d.rectangle([x, y, x + w, y + h], fill=(173, 205, 224))
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(38, 84, 124))
    d.rectangle([x, y + int(h * 0.62), x + w, y + int(h * 0.66)], fill=(120, 165, 195))
    # towers and cables
    for tx in (x + int(w * 0.28), x + int(w * 0.68)):
        d.rectangle([tx - 5, y + int(h * 0.18), tx + 5, y + int(h * 0.62)], fill=(70, 78, 90))
        d.line([tx, y + int(h * 0.18), x + 8, y + int(h * 0.60)], fill=(70, 78, 90), width=2)
        d.line([tx, y + int(h * 0.18), x + w - 8, y + int(h * 0.60)], fill=(70, 78, 90), width=2)
    d.rectangle([x, y + int(h * 0.56), x + w, y + int(h * 0.62)], fill=(52, 58, 68))
    # blast plume
    cx, cy = x + int(w * 0.52), y + int(h * 0.34)
    for r, col in ((46, (232, 116, 39)), (34, (240, 160, 60)), (22, (250, 210, 110))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for dx, dy in ((-58, 26), (52, 34), (-30, -30), (64, -6)):
        d.ellipse([cx + dx - 7, cy + dy - 7, cx + dx + 7, cy + dy + 7], fill=(120, 120, 120))
    # small boat
    d.polygon([(x + 30, y + h - 22), (x + 92, y + h - 22), (x + 80, y + h - 8), (x + 42, y + h - 8)],
              fill=(30, 30, 36))


def ill_radar(d, x, y, w, h):
    """Tanker at sea under a radar dome, drones overhead."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 54, 74))
    d.rectangle([x, y + int(h * 0.66), x + w, y + h], fill=(16, 42, 60))
    # tanker
    d.rectangle([x + 26, y + int(h * 0.58), x + w - 26, y + int(h * 0.74)], fill=(18, 18, 22))
    d.rectangle([x + w - 78, y + int(h * 0.40), x + w - 40, y + int(h * 0.58)], fill=(220, 220, 220))
    d.rectangle([x + w - 72, y + int(h * 0.34), x + w - 46, y + int(h * 0.40)], fill=(178, 34, 34))
    # radar dome + sweep arcs
    cx, cy = x + 62, y + int(h * 0.42)
    d.pieslice([cx - 34, cy - 34, cx + 34, cy + 6], 180, 360, fill=(240, 240, 235))
    for r in (48, 66):
        d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(250, 210, 110), width=3)
    # drones
    for dx, dy in ((150, 26), (196, 52), (238, 30)):
        d.ellipse([x + dx - 5, y + dy - 4, x + dx + 5, y + dy + 4], fill=(250, 210, 110))
        d.line([x + dx - 12, y + dy, x + dx + 12, y + dy], fill=(250, 210, 110), width=2)


def ill_summit(d, x, y, w, h):
    """Three flags over a summit table: US, China, Russia."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    fw, fh = (w - 40) // 3, int(h * 0.52)
    # US flag (simplified)
    fx = x + 12
    for i in range(7):
        d.rectangle([fx, y + 14 + i * fh // 7, fx + fw, y + 14 + (i + 1) * fh // 7],
                    fill=(178, 34, 34) if i % 2 == 0 else (240, 240, 240))
    d.rectangle([fx, y + 14, fx + int(fw * 0.42), y + 14 + 3 * fh // 7], fill=(30, 50, 110))
    # China flag
    fx += fw + 8
    d.rectangle([fx, y + 14, fx + fw, y + 14 + fh], fill=(222, 41, 16))
    d.ellipse([fx + 10, y + 24, fx + 34, y + 48], fill=(250, 210, 60))
    # Russia flag
    fx += fw + 8
    for i, col in enumerate(((240, 240, 240), (0, 57, 166), (213, 0, 50))):
        d.rectangle([fx, y + 14 + i * fh // 3, fx + fw, y + 14 + (i + 1) * fh // 3], fill=col)
    # table + microphones
    ty = y + 14 + fh + 12
    d.rectangle([x + 16, ty, x + w - 16, ty + 10], fill=(90, 60, 40))
    for mx in (x + 70, x + w // 2, x + w - 70):
        d.line([mx, ty, mx, ty - 18], fill=(40, 40, 40), width=3)
        d.ellipse([mx - 5, ty - 26, mx + 5, ty - 16], fill=(40, 40, 40))


def ill_jets(d, x, y, w, h):
    """Two jets crossing a pale sky."""
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 235))
    d.ellipse([x + w - 62, y + 12, x + w - 12, y + 62], fill=(250, 210, 110))
    for cx, cy, s in ((x + 90, y + 58, 1.0), (x + 200, y + 30, 0.75)):
        L = int(52 * s)
        d.polygon([(cx - L, cy), (cx + L, cy - int(7 * s)), (cx + L, cy + int(7 * s))], fill=(70, 78, 90))
        d.polygon([(cx - int(8 * s), cy), (cx + int(14 * s), cy - int(20 * s)),
                   (cx + int(26 * s), cy - int(18 * s)), (cx + int(20 * s), cy)], fill=(90, 98, 110))
        d.polygon([(cx - int(8 * s), cy + 2), (cx + int(14 * s), cy + int(20 * s)),
                   (cx + int(26 * s), cy + int(18 * s)), (cx + int(20 * s), cy + 2)], fill=(90, 98, 110))
    d.line([x + 20, y + h - 26, x + w - 20, y + h - 26], fill=(255, 255, 255), width=2)
    d.line([x + 60, y + h - 14, x + w - 60, y + h - 14], fill=(255, 255, 255), width=2)


def ill_globe(d, x, y, w, h):
    """Globe with an arrow from Europe to a pin."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 222))
    cx, cy, r = x + w // 2, y + h // 2 + 4, min(w, h) // 2 - 14
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 156, 205))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 60, 90), width=3)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(255, 255, 255), width=2)
    # land blobs
    d.ellipse([cx - r + 8, cy - r + 18, cx - 10, cy - 6], fill=(96, 170, 90))
    d.ellipse([cx + 2, cy + 4, cx + r - 12, cy + r - 14], fill=(96, 170, 90))
    # red pin
    px, py = cx + r - 22, cy - r + 6
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(178, 34, 34))
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))


def ill_pentagon(d, x, y, w, h):
    """The Pentagon building on a lawn."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 214))
    cx, cy, r = x + w // 2, y + h // 2 + 8, min(w, h) // 2 - 12
    import math
    pts = []
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(150, 158, 168))
    r2 = r * 0.45
    pts2 = []
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        pts2.append((cx + r2 * math.cos(a), cy + r2 * math.sin(a)))
    d.polygon(pts2, fill=(214, 226, 214))
    d.polygon(pts2, outline=(120, 128, 138))
    d.text((x + 12, y + 8), "AUDIT: 9TH FAIL", font=font(SANS_B, 15), fill=(120, 30, 30))


def ill_chip(d, x, y, w, h):
    """AI chip with pins and traces."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 48))
    cx, cy, s = x + w // 2, y + h // 2, min(w, h) // 2 - 22
    for dx in (-s - 14, s + 8):
        for k in range(4):
            yy = cy - 36 + k * 24
            d.rectangle([cx + dx - 3, yy, cx + dx + 3, yy + 10], fill=(201, 162, 39))
    for dy in (-s - 14, s + 8):
        for k in range(4):
            xx = cx - 36 + k * 24
            d.rectangle([xx, cy + dy - 3, xx + 10, cy + dy + 3], fill=(201, 162, 39))
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(52, 68, 96))
    d.rectangle([cx - s + 12, cy - s + 12, cx + s - 12, cy + s - 12], outline=(201, 162, 39), width=3)
    d.text((cx - 18, cy - 12), "AI", font=font(SANS_B, 26), fill=(240, 240, 235))
    d.line([x + 14, y + h - 18, x + w - 60, y + h - 18], fill=(120, 140, 170), width=2)
    d.line([x + w - 60, y + h - 18, x + w - 60, y + h - 34], fill=(120, 140, 170), width=2)


def ill_parliament(d, x, y, w, h):
    """Parliament building: dome and columns."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 208))
    cx = x + w // 2
    d.rectangle([x + 30, y + h - 26, x + w - 30, y + h - 14], fill=(120, 116, 106))
    for i in range(5):
        px = x + 48 + i * (w - 96) // 4
        d.rectangle([px - 7, y + 44, px + 7, y + h - 26], fill=(250, 248, 242))
    d.rectangle([x + 30, y + 36, x + w - 30, y + 48], fill=(150, 146, 136))
    d.pieslice([cx - 34, y + 2, cx + 34, y + 70], 180, 360, fill=(90, 110, 130))
    d.rectangle([cx - 3, y - 2, cx + 3, y + 8], fill=(201, 162, 39))


def ill_storm(d, x, y, w, h):
    """Cyclone spiral over the sea."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 216, 228))
    d.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=(38, 84, 124))
    cx, cy = x + w // 2, y + int(h * 0.42)
    for r, col in ((64, (255, 255, 255)), (48, (220, 232, 240)), (32, (255, 255, 255)),
                   (18, (200, 220, 232))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(38, 84, 124))
    d.arc([cx - 78, cy - 30, cx + 78, cy + 30], 200, 340, fill=(255, 255, 255), width=5)
    d.arc([cx - 88, cy - 44, cx + 88, cy + 44], 160, 20, fill=(255, 255, 255), width=4)


def ill_alert(d, x, y, w, h):
    """Warning triangle over a city skyline."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 196))
    base = y + h - 18
    for i, bh in enumerate((34, 52, 44, 62, 40)):
        bx = x + 22 + i * (w - 44) // 5
        d.rectangle([bx, base - bh, bx + 34, base], fill=(90, 98, 110))
    cx, cy = x + w // 2, y + int(h * 0.42)
    d.polygon([(cx, cy - 44), (cx - 46, cy + 34), (cx + 46, cy + 34)], fill=(201, 162, 39))
    d.polygon([(cx, cy - 44), (cx - 46, cy + 34), (cx + 46, cy + 34)], outline=(120, 90, 20), width=3)
    d.rectangle([cx - 4, cy - 20, cx + 4, cy + 8], fill=(30, 30, 30))
    d.ellipse([cx - 5, cy + 16, cx + 5, cy + 26], fill=(30, 30, 30))


# ---------- layout ----------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((W // 2, 16), "THE WORLD IN ONE DAY", font=font(SERIF_B, 54),
           fill=(247, 243, 234), anchor="ma")
    d.line([M, 88, W - M, 88], fill=GOLD, width=2)
    d.text((W // 2, 94), "WEDNESDAY  ·  18 NOVEMBER 2026", font=font(SANS_B, 24),
           fill=GOLD, anchor="ma")

    # lead story
    ly = 134
    ill_summit(d, M, ly, 430, 258)
    draw_text_block(d, M + 452, ly + 2, W - M - (M + 452), "ASIA · APEC",
                    "APEC opens in Shenzhen as Trump tours Asia",
                    "Leaders gather in China for the 18–19 November summit. Trump "
                    "holds Quad talks in Manila first, while Xi meets Canada's "
                    "Carney.",
                    kicker_size=19, head_size=32, deck_size=22,
                    max_head_lines=3, max_deck_lines=4)
    d.line([M, 404, W - M, 404], fill=RULE, width=2)

    # two rows of three stories
    col_w = (W - 2 * M - 2 * 24) // 3
    stories = [
        ("TECHNOLOGY", "Nvidia doubles sales; board bars Huang return",
         "Revenue hits $115.84bn, twice a year earlier. The board won't "
         "bring back Jensen Huang.", ill_chip),
        ("MIDDLE EAST", "Gulf on edge after drone scares",
         "Bahrain lifts an overnight threat warning; Kuwait's army says it "
         "intercepted drones.", ill_radar),
        ("EUROPE", "Latvia approves a new government",
         "The Saeima backs prime minister Kulbergs' cabinet in a "
         "confidence vote.", ill_parliament),
        ("THE TOLL OF WAR", "UN: 372 civilians killed in Ukraine in October",
         "The UN rights mission's October toll. In Sudan, the UN confirms "
         "over 2,230 civilian deaths.", ill_globe),
        ("WEATHER", "Cyclone Akvan builds over the Bay of Bengal",
         "India's weather office warns the storm is likely to intensify "
         "into a severe cyclone.", ill_storm),
        ("UNITED STATES", "Trump: Iran plot report taken 'very seriously'",
         "US officials say Iran is developing plans to target Trump "
         "officials in Washington.", ill_alert),
    ]
    row_ys = [420, 700]
    for i, (kicker, head, deck, ill) in enumerate(stories):
        row, col = divmod(i, 3)
        x = M + col * (col_w + 24)
        y = row_ys[row]
        ill(d, x, y, col_w, 108)
        draw_text_block(d, x, y + 118, col_w, kicker, head, deck,
                        kicker_size=15, head_size=23, deck_size=18,
                        max_head_lines=2, max_deck_lines=3)
    d.line([M, 968, W - M, 968], fill=RULE, width=2)

    # also-today strip
    y = 978
    d.text((M, y), "ALSO TODAY", font=font(SANS_B, 17), fill=RED)
    items = ("Dhoni retires from the IPL to mentor Chennai   ·   "
             "Amazon puts $7bn into Indian renewables   ·   "
             "India re-elected to the ITU Council   ·   "
             "Trump gets until 22 January in $10bn BBC case")
    lines = wrap(d, items, font(SANS, 17), W - 2 * M - 130)
    yy = y - 1
    for ln in lines[:2]:
        d.text((M + 130, yy), ln, font=font(SANS, 17), fill=(52, 56, 66))
        yy += 21

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
