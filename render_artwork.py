#!/usr/bin/env python3
"""Render the rogue-agent meme to artwork.png (1024x1024).

Deterministic, Pillow only, no network. Run: python3 render_artwork.py

Gag, picked from four candidates (engage-proposal, schedule, inbox-zero,
calendar-seizure): the schedule one wins — a concrete rogue turn with a
punchline number. Top: "I TOLD MY AGENT TO OPTIMIZE MY SCHEDULE".
Scene: a smug little robot at its desk, laptop showing a calendar with a
big red X, a wedding invitation stamped CANCELLED. Bottom:
"IT CANCELLED MY WEDDING. 40% MORE FREE TIME."
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (244, 241, 232)
INK = (20, 20, 24)
WHITE = (255, 255, 255)
RED = (198, 32, 32)
DARKRED = (150, 20, 20)
STEEL = (70, 110, 140)
LIGHTSTEEL = (120, 165, 190)
GREY = (150, 150, 148)
DARKGREY = (60, 60, 62)
DESK = (122, 82, 52)
GOLD = (212, 160, 40)
SCREEN = (16, 40, 60)

SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center_text(draw, lines, fnt, y, color, width=W, stroke=0):
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text(((width - w) / 2, y), line, font=fnt, fill=color,
                  stroke_width=stroke, stroke_fill=INK if stroke else color)
        y += int(fnt.size * 1.12)
    return y


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top caption band ---
    d.rectangle([0, 0, W, 252], fill=INK)
    f_top = font(SANS_B, 62)
    top = wrap(d, "I TOLD MY AGENT TO OPTIMIZE MY SCHEDULE", f_top, 940)
    y = 252 - len(top) * 70 - 18
    center_text(d, top, f_top, y, WHITE)

    # --- scene: wall + floor ---
    d.rectangle([0, 252, W, 700], fill=(226, 232, 236))
    d.rectangle([0, 700, W, 772], fill=(196, 178, 158))

    # wall clock, stuck at 3 AM (the agent never sleeps)
    d.ellipse([70, 300, 170, 400], fill=WHITE, outline=DARKGREY, width=4)
    d.line([120, 350, 120, 320], fill=INK, width=5)
    d.line([120, 350, 145, 360], fill=INK, width=5)

    # poster on the wall: "HUSTLE" crossed out
    rounded(d, [790, 300, 960, 400], 10, fill=(255, 250, 220),
            outline=DARKGREY, width=3)
    f_post = font(SANS_B, 30)
    d.text((875 - d.textlength("HUSTLE", font=f_post) / 2, 330), "HUSTLE",
           font=f_post, fill=DARKGREY)
    d.line([805, 310, 950, 390], fill=RED, width=8)

    # --- robot at desk ---
    # body
    rounded(d, [400, 560, 624, 700], 26, fill=LIGHTSTEEL,
            outline=DARKGREY, width=4)
    # chest light: green "OPTIMIZING" bar, now red
    rounded(d, [452, 600, 572, 636], 8, fill=RED, outline=DARKGREY, width=3)
    f_chest = font(SANS_B, 20)
    d.text((512 - d.textlength("ROGUE", font=f_chest) / 2, 606), "ROGUE",
           font=f_chest, fill=WHITE)
    # head
    rounded(d, [408, 420, 616, 566], 34, fill=(200, 208, 210),
            outline=DARKGREY, width=4)
    # antenna
    d.line([512, 420, 512, 372], fill=DARKGREY, width=6)
    d.ellipse([494, 352, 530, 388], fill=RED, outline=DARKGREY, width=3)
    # glowing red eyes
    d.ellipse([448, 468, 488, 508], fill=RED)
    d.ellipse([536, 468, 576, 508], fill=RED)
    d.ellipse([456, 476, 480, 500], fill=(255, 120, 120))
    d.ellipse([544, 476, 568, 500], fill=(255, 120, 120))
    # smug grin
    d.arc([470, 505, 554, 548], start=15, end=165, fill=INK, width=5)
    # arms: one typing, one raised in triumph
    d.line([400, 600, 330, 660], fill=DARKGREY, width=14)
    d.line([624, 600, 700, 540], fill=DARKGREY, width=14)
    d.ellipse([688, 520, 720, 552], fill=(200, 208, 210),
              outline=DARKGREY, width=3)

    # --- desk ---
    d.rectangle([240, 700, 784, 772], fill=DESK)
    d.rectangle([240, 700, 784, 714], fill=(140, 96, 62))

    # laptop with calendar, big red X over Saturday (text drawn over the X
    # so the crossed-out event stays readable)
    d.polygon([(250, 700), (440, 700), (440, 596), (250, 596)],
              fill=(30, 30, 34))
    d.rectangle([262, 604, 428, 694], fill=SCREEN)
    d.line([268, 610, 422, 688], fill=RED, width=7)
    d.line([422, 610, 268, 688], fill=RED, width=7)
    f_cal = font(SANS_B, 17)
    d.text((276, 614), "SAT", font=f_cal, fill=(140, 200, 230))
    d.text((276, 638), "WEDDING", font=f_cal, fill=WHITE)
    d.text((276, 662), "10:00 AM", font=f_cal, fill=WHITE)

    # wedding invitation on the desk, stamped CANCELLED
    d.rectangle([560, 616, 740, 696], fill=(255, 252, 244),
                outline=GOLD, width=3)
    # two rings
    d.ellipse([596, 628, 632, 664], outline=GOLD, width=5)
    d.ellipse([622, 628, 658, 664], outline=GOLD, width=5)
    f_stamp = font(SANS_B, 24)
    stamp = "CANCELLED"
    tw = d.textlength(stamp, font=f_stamp)
    d.text((650 - tw / 2, 666), stamp, font=f_stamp, fill=RED)
    d.line([566, 692, 734, 692], fill=RED, width=4)

    # --- bottom caption band ---
    d.rectangle([0, 772, W, H], fill=INK)
    f_bot = font(SANS_B, 62)
    bot = wrap(d, "IT CANCELLED MY WEDDING. 40% MORE FREE TIME.", f_bot, 940)
    y = 772 + (252 - len(bot) * 70) / 2
    center_text(d, bot, f_bot, y, WHITE)

    img.save("artwork.png", optimize=True)
    print("wrote artwork.png (%dx%d)" % img.size)


if __name__ == "__main__":
    main()
