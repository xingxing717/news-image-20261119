"""Render entry.png: a one-page newspaper front page summing up the world news
of Thursday 19 November 2026. Six stories, each verified against news reports
dated 19 November 2026 (Reuters, BBC, AP, The Hindu, NASA):

  1. GTA VI begins its global rollout (Reuters, 19 Nov).
  2. Trump, Xi and Putin gather in Shenzhen for trilateral talks (NYT, 19 Nov).
  3. Crimean Bridge hit a third time this week; rail span struck, traffic
     halted (Reuters/BBC, 19 Nov).
  4. Cyclone Akvan nears India's east coast; landfall expected between
     Machilipatnam and Puri (The Hindu, 19 Nov).
  5. A Van Gogh sells for a record $190.4m after a row over its Nazi-era
     history (BBC, 19 Nov).
  6. NASA confirms Voyager 1 one light-day from Earth at its live event on
     Thursday 19 Nov (NASA; milestone reached 18 Nov, confirmed 19 Nov).

Pure Pillow drawing: flat pictograms, no borrowed images. Output is a
deterministic 1024x1024 PNG.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
NAVY = (22, 35, 63)
GOLD = (232, 184, 75)
INK = (24, 24, 24)
GREY = (74, 74, 74)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def spaced_text(draw, cx, y, text, fnt, fill, spacing=4):
    """Draw centred text with extra letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + spacing


def draw_controller(d, cx, cy):
    """Flat game controller, centred at (cx, cy)."""
    d.rounded_rectangle([cx - 72, cy - 30, cx + 72, cy + 34], radius=28,
                        fill=(248, 250, 252), outline=(31, 41, 55), width=3)
    # d-pad
    d.rectangle([cx - 52, cy - 8, cx - 28, cy + 8], fill=(31, 41, 55))
    d.rectangle([cx - 44, cy - 16, cx - 36, cy + 16], fill=(31, 41, 55))
    # buttons
    for dx, dy, col in [(38, -14, (220, 38, 38)), (52, 0, (234, 179, 8)),
                        (38, 14, (22, 163, 74)), (24, 0, (37, 99, 235))]:
        d.ellipse([cx + dx - 7, cy + dy - 7, cx + dx + 7, cy + dy + 7], fill=col)
    # sticks
    for sx in (-12, 12):
        d.ellipse([cx + sx - 9, cy + 12 - 9, cx + sx + 9, cy + 12 + 9],
                  fill=(100, 116, 139), outline=(31, 41, 55), width=2)


def draw_flags(d, cx, cy):
    """Three small summit flags: US, China, Russia."""
    poles = [cx - 52, cx, cx + 52]
    for px in poles:
        d.line([px, cy - 52, px, cy + 58], fill=(51, 65, 85), width=4)
        d.ellipse([px - 4, cy - 58, px + 4, cy - 50], fill=(232, 184, 75))
    # US flag (stripes + canton)
    x0 = poles[0] + 3
    for i in range(5):
        d.rectangle([x0, cy - 50 + i * 9, x0 + 44, cy - 42 + i * 9],
                    fill=(178, 34, 34) if i % 2 == 0 else (248, 250, 252))
    d.rectangle([x0, cy - 50, x0 + 19, cy - 26], fill=(30, 58, 138))
    # China flag (red + stars)
    x0 = poles[1] + 3
    d.rectangle([x0, cy - 50, x0 + 44, cy - 6], fill=(222, 41, 16))
    d.ellipse([x0 + 6, cy - 44, x0 + 16, cy - 34], fill=(255, 222, 0))
    for sx, sy in [(28, -40), (34, -34), (28, -28), (22, -34)]:
        d.ellipse([x0 + sx, cy + sy, x0 + sx + 4, cy + sy + 4], fill=(255, 222, 0))
    # Russia flag (white / blue / red)
    x0 = poles[2] + 3
    for i, col in enumerate([(248, 250, 252), (0, 82, 164), (213, 0, 50)]):
        d.rectangle([x0, cy - 50 + i * 15, x0 + 44, cy - 36 + i * 15], fill=col)


def draw_bridge(d, cx, cy):
    """Suspension bridge with a broken deck span and a blast burst."""
    # towers
    for tx in (cx - 48, cx + 40):
        d.rectangle([tx, cy - 62, tx + 8, cy + 28], fill=(51, 65, 85))
    # cables
    d.line([cx - 44, cy - 62, cx - 4, cy + 6], fill=(100, 116, 139), width=3)
    d.line([cx + 44, cy - 62, cx + 4, cy + 6], fill=(100, 116, 139), width=3)
    d.line([cx - 44, cy - 62, cx - 72, cy + 6], fill=(100, 116, 139), width=3)
    d.line([cx + 44, cy - 62, cx + 72, cy + 6], fill=(100, 116, 139), width=3)
    # deck, broken in the middle
    d.rectangle([cx - 74, cy + 2, cx - 8, cy + 10], fill=(31, 41, 55))
    d.rectangle([cx + 8, cy + 2, cx + 74, cy + 10], fill=(31, 41, 55))
    d.polygon([(cx - 8, cy + 4), (cx + 8, cy + 4), (cx + 4, cy + 20),
               (cx - 4, cy + 20)], fill=(31, 41, 55))
    # blast burst at the break
    bx, by = cx, cy - 8
    pts = []
    for i in range(12):
        ang = math.pi * i / 6
        r = 16 if i % 2 == 0 else 7
        pts.append((bx + r * math.cos(ang), by + r * math.sin(ang)))
    d.polygon(pts, fill=(245, 158, 11))
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(254, 243, 199))
    # water
    for wy in (cy + 34, cy + 48):
        for k in range(4):
            x0 = cx - 72 + k * 38
            d.arc([x0, wy - 8, x0 + 34, wy + 8], start=200, end=340,
                  fill=(56, 130, 180), width=4)


def draw_cyclone(d, cx, cy):
    """Spiral storm with rain."""
    for r in (58, 46, 34, 22):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=40 + r, end=300 + r,
              fill=(255, 255, 255), width=7)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 255, 255))
    # rain streaks
    for rx, ry in [(-58, -42), (52, -38), (-52, 42), (56, 44), (0, -62)]:
        d.line([cx + rx, cy + ry, cx + rx - 6, cy + ry + 16],
               fill=(186, 230, 253), width=4)
    # coastline
    d.polygon([(cx + 34, cy + 62), (cx + 74, cy + 62), (cx + 74, cy + 30)],
              fill=(120, 113, 108))


def draw_vangogh(d, cx, cy):
    """Framed canvas: swirling night sky, sun, cypress."""
    d.rectangle([cx - 66, cy - 62, cx + 66, cy + 62], fill=(212, 160, 23))
    d.rectangle([cx - 56, cy - 52, cx + 56, cy + 52], fill=(43, 76, 158))
    # swirls
    for r, a0 in [(40, 200), (30, 120), (20, 300)]:
        d.arc([cx - 18 - r, cy - 34 - r, cx - 18 + r, cy - 34 + r],
              start=a0, end=a0 + 220, fill=(147, 197, 253), width=5)
    # sun
    d.ellipse([cx + 18, cy - 46, cx + 48, cy - 16], fill=(250, 204, 21))
    d.ellipse([cx + 26, cy - 38, cx + 40, cy - 24], fill=(254, 240, 138))
    # cypress
    d.polygon([(cx - 52, cy + 52), (cx - 44, cy - 6), (cx - 34, cy + 52)],
              fill=(20, 83, 45))
    # field
    d.rectangle([cx - 56, cy + 34, cx + 56, cy + 52], fill=(202, 138, 4))


def draw_voyager(d, cx, cy):
    """Space probe: gold dish, bus, boom, stars, small Earth."""
    for sx, sy in [(-58, -48), (56, -52), (-52, 38), (58, 30), (30, -58),
                   (-30, 52), (0, 58)]:
        d.ellipse([cx + sx - 2, cy + sy - 2, cx + sx + 2, cy + sy + 2],
                  fill=(255, 255, 255))
    # dish
    d.ellipse([cx - 34, cy - 40, cx + 34, cy + 28], fill=(217, 119, 6))
    d.ellipse([cx - 22, cy - 28, cx + 22, cy + 16], fill=(245, 158, 11))
    d.ellipse([cx - 7, cy - 13, cx + 7, cy + 1], fill=(254, 243, 199))
    # bus + boom
    d.rectangle([cx - 12, cy + 28, cx + 12, cy + 46], fill=(226, 232, 240))
    d.line([cx + 12, cy + 37, cx + 58, cy + 52], fill=(148, 163, 184), width=3)
    d.rectangle([cx + 52, cy + 46, cx + 64, cy + 58], fill=(226, 232, 240))
    # Earth, bottom left
    d.ellipse([cx - 66, cy + 34, cx - 40, cy + 60], fill=(37, 99, 235))
    d.ellipse([cx - 60, cy + 40, cx - 50, cy + 48], fill=(34, 197, 94))
    d.ellipse([cx - 52, cy + 50, cx - 44, cy + 56], fill=(34, 197, 94))


DRAW = {
    "gta": draw_controller,
    "summit": draw_flags,
    "bridge": draw_bridge,
    "cyclone": draw_cyclone,
    "vangogh": draw_vangogh,
    "voyager": draw_voyager,
}

STORIES = [
    dict(key="gta", bg=(124, 58, 237), kicker="GAMES · VICE CITY",
         headline="GTA VI rolls out worldwide",
         summary="After 13 years, Rockstar's game unlocks at midnight, time zone by time zone."),
    dict(key="summit", bg=(155, 27, 48), kicker="SUMMIT · SHENZHEN",
         headline="Trump, Xi and Putin gather",
         summary="The three leaders meet in Shenzhen for trilateral talks at the APEC summit."),
    dict(key="bridge", bg=(30, 58, 95), kicker="WAR · UKRAINE",
         headline="Crimean Bridge hit a third time",
         summary="Overnight strike hits the rail span; traffic halted, Russia says."),
    dict(key="cyclone", bg=(14, 116, 144), kicker="WEATHER · INDIA",
         headline="Cyclone Akvan nears India's coast",
         summary="Landfall expected between Machilipatnam and Puri on the east coast."),
    dict(key="vangogh", bg=(180, 83, 9), kicker="ART · RECORD SALE",
         headline="Van Gogh sells for $190.4m",
         summary="A record price, after a row over the painting's Nazi-era history."),
    dict(key="voyager", bg=(15, 23, 42), kicker="SPACE · NASA",
         headline="Voyager 1 a light-day away",
         summary="NASA confirms the 1977 probe is the first human-made object so far out."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 170], fill=NAVY)
    spaced_text(d, W // 2, 22, "THE WORLD IN ONE DAY",
                font(SERIF_B, 40), (255, 255, 255), spacing=6)
    d.line([32, 76, W - 32, 76], fill=GOLD, width=2)
    d.text((W // 2, 84), "19 NOVEMBER 2026", font=font(SERIF_B, 54),
           fill=GOLD, anchor="ma")
    spaced_text(d, W // 2, 152, "THURSDAY  ·  SIX STORIES FROM AROUND THE GLOBE",
                font(SANS_B, 17), (255, 255, 255), spacing=2)

    # ---- story cards: 2 cols x 3 rows ----
    margin, gap = 16, 14
    cw = (W - 2 * margin - gap) // 2          # 489
    ch = 262
    y0 = 182
    f_kick = font(SANS_B, 17)
    f_head = font(SANS_B, 29)
    f_sum = font(SANS, 20)
    for i, s in enumerate(STORIES):
        x = margin + (i % 2) * (cw + gap)
        y = y0 + (i // 2) * (ch + 12)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=10, fill=CARD,
                            outline=BORDER, width=2)
        # pictogram panel (left)
        px, py = x + 2, y + 2
        pw, ph = 168, ch - 4
        d.rounded_rectangle([px, py, px + pw, py + ph], radius=8, fill=s["bg"])
        DRAW[s["key"]](d, px + pw // 2, py + ph // 2)
        # text zone (right)
        tx = x + 168 + 18
        tw = cw - 168 - 18 - 14
        d.text((tx, y + 20), s["kicker"], font=f_kick, fill=s["bg"])
        d.line([tx, y + 46, tx + tw, y + 46], fill=s["bg"], width=2)
        lines = wrap(d, s["headline"], f_head, tw)
        ly = y + 58
        for ln in lines:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 34
        lines = wrap(d, s["summary"], f_sum, tw)
        ly += 8
        for ln in lines:
            d.text((tx, ly), ln, font=f_sum, fill=GREY)
            ly += 26

    # ---- footer ----
    d.text((W // 2, 998),
           "All six stories happened or were first reported on 19 November 2026",
           font=font(SANS, 15), fill=GREY, anchor="ma")
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
