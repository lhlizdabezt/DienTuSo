from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ASSETS / "roundabout-motion.gif"


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def svg_hero():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="420" viewBox="0 0 1280 420" role="img" aria-label="Roundabout traffic-light controller project banner">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#071827"/>
      <stop offset="0.52" stop-color="#0b2942"/>
      <stop offset="1" stop-color="#0c4a4e"/>
    </linearGradient>
    <style>
      .eyebrow{font:700 16px Arial, sans-serif;letter-spacing:2px;fill:#67e8f9}
      .title{font:700 48px Arial, sans-serif;fill:#f8fafc}
      .sub{font:400 21px Arial, sans-serif;fill:#cbd5e1}
      .card-title{font:700 17px Arial, sans-serif;fill:#f8fafc}
      .card-copy{font:400 15px Arial, sans-serif;fill:#cbd5e1}
      .pill{font:700 14px Arial, sans-serif;fill:#e2e8f0}
      .small{font:600 14px Arial, sans-serif;fill:#bae6fd}
    </style>
  </defs>
  <rect width="1280" height="420" rx="28" fill="url(#bg)"/>
  <rect x="52" y="42" width="1176" height="336" rx="24" fill="#020617" opacity="0.34" stroke="#38bdf8" stroke-opacity="0.30"/>
  <text x="88" y="88" class="eyebrow">DIGITAL ELECTRONICS | ETC00002</text>
  <text x="88" y="146" class="title">Roundabout Traffic-Light Controller</text>
  <text x="88" y="184" class="sub">Ten-state gate-level sequencing for paired approaches A/C and B/D</text>
  <g transform="translate(88 218)">
    <rect width="318" height="84" rx="16" fill="#0f2940" stroke="#38bdf8" stroke-opacity="0.48"/>
    <text x="22" y="32" class="card-title">CLOCK CONTROL</text>
    <text x="22" y="58" class="card-copy">NE555 oscillator and manual step</text>
    <rect x="338" width="318" height="84" rx="16" fill="#0f2940" stroke="#38bdf8" stroke-opacity="0.48"/>
    <text x="360" y="32" class="card-title">JK STATE COUNTER</text>
    <text x="360" y="58" class="card-copy">Four flip-flops and ten valid states</text>
    <rect x="676" width="318" height="84" rx="16" fill="#0f2940" stroke="#38bdf8" stroke-opacity="0.48"/>
    <text x="698" y="32" class="card-title">OUTPUT DECODER</text>
    <text x="698" y="58" class="card-copy">Mutually exclusive green phases</text>
  </g>
  <g transform="translate(88 326)">
    <rect width="180" height="30" rx="15" fill="#164e63"/>
    <text x="22" y="20" class="pill">AUTO / MANUAL</text>
    <rect x="196" width="118" height="30" rx="15" fill="#164e63"/>
    <text x="222" y="20" class="pill">FALSTAD</text>
    <rect x="330" width="140" height="30" rx="15" fill="#164e63"/>
    <text x="355" y="20" class="pill">BREADBOARD</text>
    <text x="676" y="20" class="small">HCMUS FETEL | Class 25DTV_DKD3 | Academic year 2025-2026</text>
  </g>
</svg>
"""
    (ASSETS / "digital-logic-hero.svg").write_text(svg, encoding="utf-8")


def draw_light(draw, center, active, color):
    x, y = center
    fill = color if active else (38, 38, 38)
    outline = tuple(min(255, channel + 70) for channel in color) if active else (112, 112, 112)
    draw.ellipse((x - 15, y - 15, x + 15, y + 15), fill=fill, outline=outline, width=3)
    if active:
        draw.ellipse((x - 22, y - 22, x + 22, y + 22), outline=outline, width=2)


def draw_lane(draw, box, label, mode):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 4, y1 + 6, x2 + 4, y2 + 6), radius=18, fill=(8, 18, 40))
    draw.rounded_rectangle(box, radius=18, fill=(30, 41, 59), outline=(203, 213, 225), width=2)
    draw.text((x1 + 18, y1 + 16), label, font=CARD, fill=(248, 250, 252))
    draw_light(draw, (x1 + 32, y1 + 58), mode == "red", (239, 68, 68))
    draw_light(draw, (x1 + 72, y1 + 58), mode == "yellow", (250, 204, 21))
    draw_light(draw, (x1 + 112, y1 + 58), mode == "green", (34, 197, 94))


def frame(index):
    states = [
        (8, "A/C GREEN", "G", "R"),
        (9, "A/C GREEN", "G", "R"),
        (10, "A/C GREEN", "G", "R"),
        (11, "A/C GREEN", "G", "R"),
        (12, "A/C YELLOW", "Y", "R"),
        (0, "B/D GREEN", "R", "G"),
        (1, "B/D GREEN", "R", "G"),
        (2, "B/D GREEN", "R", "G"),
        (3, "B/D GREEN", "R", "G"),
        (4, "B/D YELLOW", "R", "Y"),
    ]
    approaches = [("A", 145, "AC"), ("C", 365, "AC"), ("B", 695, "BD"), ("D", 915, "BD")]
    frames = []

    for active_slot, (state, phase_label, ac_color, bd_color) in enumerate(states):
        image = Image.new("RGB", (1120, 620), (7, 24, 39))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((24, 24, 1096, 596), radius=28, fill=(248, 250, 252))
        draw.text((54, 48), "ROUNDABOUT TRAFFIC-LIGHT CONTROLLER", font=font(31, True), fill=(15, 23, 42))
        draw.text(
            (56, 91),
            "Ten-state 4-1-4-1 sequence | Gate-level JK logic | Automatic and manual clock",
            font=font(18),
            fill=(71, 85, 105),
        )

        draw.rounded_rectangle((54, 137, 1066, 224), radius=18, fill=(226, 232, 240))
        draw.text((82, 158), f"STATE {state:02d}", font=font(26, True), fill=(3, 105, 161))
        draw.text((300, 158), phase_label, font=font(26, True), fill=(15, 118, 110))
        draw.text(
            (82, 196),
            "Safety invariant: A/C and B/D are never green at the same time.",
            font=font(17),
            fill=(51, 65, 85),
        )

        for label, x, pair in approaches:
            active_color = ac_color if pair == "AC" else bd_color
            draw.rounded_rectangle((x - 80, 254, x + 80, 420), radius=20, fill=(30, 41, 59))
            draw.text((x - 55, 270), f"APPROACH {label}", font=font(16, True), fill=(226, 232, 240))
            draw_light(draw, (x, 319), active_color == "R", (239, 68, 68))
            draw_light(draw, (x, 357), active_color == "Y", (250, 204, 21))
            draw_light(draw, (x, 395), active_color == "G", (34, 197, 94))

        timeline_x = 55
        timeline_y = 468
        for slot, (number, _, _, _) in enumerate(states):
            left = timeline_x + slot * 102
            fill = (3, 105, 161) if slot == active_slot else (203, 213, 225)
            text_fill = (248, 250, 252) if slot == active_slot else (30, 41, 59)
            draw.rounded_rectangle((left, timeline_y, left + 82, timeline_y + 52), radius=12, fill=fill)
            draw.text((left + 12, timeline_y + 8), f"Q={number:02d}", font=font(17, True), fill=text_fill)

        draw.text(
            (55, 544),
            "Sequence: 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, then repeat.",
            font=font(17),
            fill=(71, 85, 105),
        )
        frames.append(image)

    frames[0].save(
        ASSETS / "roundabout-motion.gif",
        save_all=True,
        append_images=frames[1:],
        duration=700,
        loop=0,
        optimize=True,
    )


def make_preview():
    source = ROOT / "assets" / "seminar" / "falstad-overview.png"
    if not source.exists():
        return
    image = Image.open(source).convert("RGB")
    preview = ImageOps.contain(image, (1280, 720), method=Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (1280, 720), (15, 23, 42))
    x = (1280 - preview.width) // 2
    y = (720 - preview.height) // 2
    canvas.paste(preview, (x, y))
    canvas.save(ASSETS / "circuitjs-preview.png", quality=92)


if __name__ == "__main__":
    main()
