"""Draw the 22 November 2026 world-news image (1024x1024, deterministic).

Layout is a newspaper front page: masthead with the date, one big lead
story (COP31 climate talks collapse), four smaller panels (Bahrain, Mexico,
Ukraine, markets) and a bottom strip with two more stories.
Everything is drawn with PIL primitives; the output PNG is byte-stable.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (244, 239, 228)
INK = (18, 18, 18)
RED = (178, 34, 34)
GOLD = (232, 184, 75)
NAVY = (18, 59, 79)
LIGHT = (215, 227, 232)
GREY = (110, 110, 105)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading=1.18):
    """Draw lines starting at (x, y); return y after the last line."""
    lh = int(fnt.size * leading)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def centered(d, cx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)


def draw_globe(d, cx, cy, r):
    """A stylised Earth with a jagged crack across it."""
    ocean = (31, 111, 123)
    land = (143, 181, 115)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ocean)
    # continents: blobs kept inside the disc
    d.ellipse([cx - 78, cy - 62, cx - 8, cy + 2], fill=land)
    d.ellipse([cx + 12, cy - 30, cx + 72, cy + 38], fill=land)
    d.ellipse([cx - 42, cy + 42, cx + 22, cy + 88], fill=land)
    d.ellipse([cx - 88, cy + 8, cx - 48, cy + 52], fill=land)
    # meridians and parallels
    for rx in (38, 74):
        d.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=(58, 154, 168), width=2)
    for dy in (-48, 48):
        d.line([cx - r + 14, cy + dy, cx + r - 14, cy + dy], fill=(58, 154, 168), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(215, 227, 232), width=3)
    # the crack: a jagged lightning split across the globe
    crack = [
        (cx - 88, cy - 96), (cx - 52, cy - 58), (cx - 66, cy - 22),
        (cx - 26, cy + 8), (cx - 44, cy + 44), (cx - 6, cy + 78),
        (cx + 26, cy + 96),
    ]
    d.line(crack, fill=(255, 255, 255), width=9, joint="curve")
    d.line(crack, fill=(232, 184, 75), width=3, joint="curve")


def panel(d, x, y, w, h, bg, kicker, headline, sub, art):
    d.rectangle([x, y, x + w, y + h], fill=bg)
    pad = 18
    tx = x + pad
    ty = y + 14
    kf = font(FONT_BOLD, 19)
    sf = font(FONT_REG, 20)
    art_w = 108
    text_w = w - pad * 2 - art_w
    d.text((tx, ty), kicker, font=kf, fill=GOLD)
    ty += 28
    # shrink the headline until it fits on two lines
    size = 33
    while size > 24:
        hf = font(FONT_BOLD, size)
        if len(wrap(d, headline, hf, text_w)) <= 2:
            break
        size -= 2
    lines = wrap(d, headline, hf, text_w)
    ty = text_block(d, tx, ty, lines, hf, (255, 255, 255), leading=1.08)
    ty += 4
    slines = wrap(d, sub, sf, text_w)[:2]
    text_block(d, tx, ty, slines, sf, LIGHT, leading=1.15)
    art(d, x + w - art_w - 8, y + 18, art_w, h - 36)


def art_missiles(d, x, y, w, h):
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(38, 84, 96))
    for i, (sx, sy) in enumerate([(x + 8, y + 70), (x + 34, y + 84), (x + 62, y + 66)]):
        ex, ey = sx + 34, sy - 52
        d.arc([sx - 8, ey - 8, ex + 22, sy + 18], start=200, end=330,
              fill=(255, 170, 60), width=5)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 220, 120))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 255, 255))


def art_badge(d, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2 - 6
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = 46 if i % 2 == 0 else 19
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=GOLD, outline=(255, 255, 255))
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(20, 83, 45))
    d.text((cx - 4, cy - 13), "$", font=font(FONT_BOLD, 22), fill=(255, 255, 255))
    d.text((x + 8, y + h - 22), "WANTED", font=font(FONT_BOLD, 16), fill=GOLD)


def art_skyline(d, x, y, w, h):
    base = y + h - 12
    for bx, bw, bh in [(x + 2, 22, 62), (x + 28, 18, 84), (x + 50, 24, 54), (x + 78, 20, 74)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(148, 163, 184))
        for wy in range(base - bh + 8, base - 6, 14):
            d.rectangle([bx + 4, wy, bx + bw - 4, wy + 6], fill=(255, 220, 120))
    d.ellipse([x + 58, y + 2, x + 82, y + 26], fill=(203, 213, 225))
    d.ellipse([x + 70, y - 6, x + 96, y + 18], fill=(226, 232, 240))
    d.polygon([(x + 30, y + 34), (x + 38, y + 18), (x + 46, y + 34)],
              fill=(255, 120, 40))


def art_chart(d, x, y, w, h):
    pts = [(x + 6, y + 18), (x + 28, y + 30), (x + 48, y + 26),
           (x + 68, y + 52), (x + 88, y + 48), (x + 104, y + 78)]
    d.line(pts, fill=(255, 255, 255), width=5, joint="curve")
    d.polygon([(x + 104, y + 78), (x + 88, y + 72), (x + 100, y + 92)],
              fill=(255, 120, 90))
    d.text((x + 4, y + h - 24), "-3.7%", font=font(FONT_BOLD, 20), fill=(255, 150, 130))


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    centered(d, W // 2, 26, "THE WORLD IN ONE IMAGE",
             font(FONT_BOLD, 58), INK)
    d.rectangle([24, 104, W - 24, 108], fill=RED)
    centered(d, W // 2, 120, "SUNDAY, 22 NOVEMBER 2026",
             font(FONT_BOLD, 30), RED)

    # ---- lead story: COP31 collapse ----
    d.rectangle([24, 168, W - 24, 500], fill=NAVY)
    draw_globe(d, 196, 334, 108)
    tx = 348
    d.text((tx, 196), "CLIMATE  •  ANTALYA, TURKEY",
           font=font(FONT_BOLD, 21), fill=GOLD)
    d.text((tx, 226), "COP31", font=font(FONT_BOLD, 78), fill=(255, 255, 255))
    d.text((tx, 306), "COLLAPSED", font=font(FONT_BOLD, 78), fill=(255, 255, 255))
    sub = ("Climate summit ends with no deal as the EU rejects "
           "a text with no mention of fossil fuels.")
    lines = wrap(d, sub, font(FONT_REG, 25), W - 24 - tx - 28)
    text_block(d, tx, 398, lines, font(FONT_REG, 25), LIGHT, leading=1.22)

    # ---- four panels ----
    pw, ph, gap = 476, 160, 12
    panel(d, 24, 512, pw, ph, (122, 31, 31), "GULF  •  BAHRAIN",
          "IRAN STRIKES US BASES",
          "Missiles and drones hit Bahrain; two people hurt.",
          art_missiles)
    panel(d, 24 + pw + gap, 512, pw, ph, (20, 83, 45), "MEXICO  •  SINALOA",
          "'EL CHAPO ISIDRO' CAPTURED",
          "Cartel boss seized; 11 killed in the raid.",
          art_badge)
    panel(d, 24, 512 + ph + gap, pw, ph, (51, 65, 85), "UKRAINE  •  KRYVYI RIH",
          "MISSILE HITS KRYVYI RIH",
          "A boy, 7, and a woman, 20, killed; 60 wounded.",
          art_skyline)
    panel(d, 24 + pw + gap, 512 + ph + gap, pw, ph, (124, 45, 18), "MARKETS",
          "STOCKS SLIDE",
          "S&P 500 -3.7%, Nasdaq -5.3% in AI sell-off.",
          art_chart)

    # ---- bottom strip: two more stories ----
    d.line([24, 858, W - 24, 858], fill=INK, width=2)
    d.line([W // 2, 872, W // 2, 958], fill=(180, 175, 165), width=2)
    bf = font(FONT_BOLD, 22)
    kf = font(FONT_BOLD, 18)
    sf = font(FONT_REG, 19)
    d.text((24, 868), "WORLD COURT", font=kf, fill=RED)
    y = text_block(d, 24, 890, wrap(d, "MYANMAR GUILTY OF ROHINGYA GENOCIDE",
                                    bf, 452), bf, INK, leading=1.08)
    text_block(d, 24, y + 2, wrap(d, "First ruling of its kind against a state.",
                                  sf, 452), sf, (70, 70, 65))
    d.text((W // 2 + 18, 868), "TRADE", font=kf, fill=RED)
    y = text_block(d, W // 2 + 18, 890, wrap(d, "EU–INDONESIA SIGN LANDMARK DEAL",
                                             bf, 452), bf, INK, leading=1.08)
    text_block(d, W // 2 + 18, y + 2, wrap(d, "Tariffs scrapped on up to 98.5% of goods.",
                                           sf, 452), sf, (70, 70, 65))

    # ---- footer ----
    centered(d, W // 2, 994, "22 NOVEMBER 2026  —  THE WORLD'S NEWS IN ONE IMAGE",
             font(FONT_BOLD, 17), GREY)

    img.save(path, format="PNG")
    return path
