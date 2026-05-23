from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def svg_hero():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="420" viewBox="0 0 1280 420" role="img" aria-label="Digital Logic Roundabout Controller">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#111827"/>
      <stop offset="0.48" stop-color="#172554"/>
      <stop offset="1" stop-color="#064e3b"/>
    </linearGradient>
    <filter id="soft" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000" flood-opacity="0.28"/>
    </filter>
    <style>
      .title{font:700 54px Arial, sans-serif;fill:#f8fafc}
      .sub{font:400 22px Arial, sans-serif;fill:#d1d5db}
      .tag{font:700 18px Arial, sans-serif;fill:#0f172a}
      .small{font:600 15px Arial, sans-serif;fill:#dbeafe}
      .label{font:700 15px Arial, sans-serif;fill:#f8fafc}
      .muted{font:400 14px Arial, sans-serif;fill:#cbd5e1}
    </style>
  </defs>
  <rect width="1280" height="420" rx="28" fill="url(#bg)"/>
  <path d="M0 330 C260 250 420 390 680 305 C890 235 1010 260 1280 190 L1280 420 L0 420 Z" fill="#0f766e" opacity="0.34"/>
  <g filter="url(#soft)">
    <rect x="52" y="52" width="520" height="316" rx="26" fill="#f8fafc" opacity="0.97"/>
    <text x="90" y="118" class="tag">ROUNDABOUT TRAFFIC LIGHT</text>
    <text x="90" y="168" font-family="Arial, sans-serif" font-size="42" font-weight="700" fill="#111827">Mod-12 Logic</text>
    <text x="90" y="210" font-family="Arial, sans-serif" font-size="22" fill="#334155">JK FF chain -> state decoder -> LED panel</text>
    <g transform="translate(90 254)">
      <rect width="112" height="42" rx="21" fill="#fee2e2"/><text x="24" y="27" class="tag">RESET</text>
      <rect x="130" width="150" height="42" rx="21" fill="#fef3c7"/><text x="155" y="27" class="tag">NIGHT</text>
      <rect x="300" width="168" height="42" rx="21" fill="#dcfce7"/><text x="326" y="27" class="tag">NORMAL</text>
    </g>
  </g>
  <g transform="translate(665 62)">
    <text x="0" y="26" class="title">Digital Logic Controller</text>
    <text x="2" y="66" class="sub">CircuitJS/Falstad simulation with Node.js logic verification</text>
    <g transform="translate(8 108)">
      <rect x="0" y="0" width="500" height="178" rx="20" fill="#020617" opacity="0.55" stroke="#38bdf8" stroke-opacity="0.55"/>
      <path d="M58 86 H180 M180 86 V46 H288 M180 86 V126 H288 M288 46 H430 M288 126 H430" stroke="#94a3b8" stroke-width="4" fill="none"/>
      <rect x="30" y="56" width="56" height="60" rx="10" fill="#1e293b" stroke="#e5e7eb"/>
      <text x="43" y="91" class="label">CLK</text>
      <rect x="248" y="22" width="88" height="52" rx="12" fill="#1e3a8a" stroke="#93c5fd"/>
      <text x="265" y="54" class="label">COUNT</text>
      <rect x="248" y="100" width="88" height="52" rx="12" fill="#14532d" stroke="#86efac"/>
      <text x="265" y="132" class="label">MODE</text>
      <circle cx="446" cy="46" r="13" fill="#22c55e"/><circle cx="446" cy="86" r="13" fill="#facc15"/><circle cx="446" cy="126" r="13" fill="#ef4444"/>
      <text x="24" y="162" class="muted">12 states: A green -> A yellow -> all red -> next lane</text>
    </g>
    <g transform="translate(8 318)">
      <text x="0" y="0" class="small">HCMUS FETEL | Digital Electronics | Luong Hai Long | 22207056</text>
    </g>
  </g>
</svg>
"""
    (ASSETS / "digital-logic-hero.svg").write_text(svg, encoding="utf-8")


def draw_light(draw, center, active, color):
    x, y = center
    fill = color if active else (38, 38, 38)
    outline = tuple(min(255, c + 70) for c in color) if active else (112, 112, 112)
    draw.ellipse((x - 15, y - 15, x + 15, y + 15), fill=fill, outline=outline, width=3)
    if active:
        draw.ellipse((x - 23, y - 23, x + 23, y + 23), outline=outline, width=2)


def make_motion_gif():
    states = [
        ("A xanh", "A", "G"),
        ("A vang", "A", "Y"),
        ("Toan do", None, "R"),
        ("B xanh", "B", "G"),
        ("B vang", "B", "Y"),
        ("Toan do", None, "R"),
        ("C xanh", "C", "G"),
        ("C vang", "C", "Y"),
        ("Toan do", None, "R"),
        ("D xanh", "D", "G"),
        ("D vang", "D", "Y"),
        ("Toan do", None, "R"),
    ]
    positions = {"A": (480, 160), "B": (706, 310), "C": (480, 430), "D": (254, 310)}
    frames = []
    for idx, (label, active_lane, active_color) in enumerate(states):
        img = Image.new("RGB", (960, 600), (15, 23, 42))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((28, 28, 932, 572), radius=28, fill=(248, 250, 252))
        draw.text((58, 54), "Dieu khien den giao thong vong xoay", font=font(32, True), fill=(17, 24, 39))
        draw.text((60, 96), "Bo dem mod-12 | JK flip-flop | State decoder | Emergency + night mode", font=font(18), fill=(71, 85, 105))

        draw.rounded_rectangle((192, 154, 768, 462), radius=32, outline=(100, 116, 139), width=10)
        for x, y in positions.values():
            draw.line((480, 314, x, y), fill=(148, 163, 184), width=5)
        draw.rounded_rectangle((400, 258, 560, 370), radius=20, fill=(226, 232, 240), outline=(100, 116, 139), width=3)
        draw.text((424, 274), "MOD-12", font=font(24, True), fill=(15, 23, 42))
        draw.text((424, 308), f"STATE {idx:02d}", font=font(22, True), fill=(37, 99, 235))
        draw.text((424, 340), label.upper(), font=font(16, True), fill=(15, 118, 110))

        for lane, (x, y) in positions.items():
            draw.rounded_rectangle((x - 62, y - 52, x + 62, y + 52), radius=18, fill=(30, 41, 59))
            draw.text((x - 40, y - 42), f"Huong {lane}", font=font(16, True), fill=(226, 232, 240))
            red_on = active_lane is None or (lane != active_lane)
            yellow_on = lane == active_lane and active_color == "Y"
            green_on = lane == active_lane and active_color == "G"
            if active_lane is None:
                yellow_on = False
                green_on = False
            draw_light(draw, (x - 36, y + 16), red_on, (239, 68, 68))
            draw_light(draw, (x, y + 16), yellow_on, (250, 204, 21))
            draw_light(draw, (x + 36, y + 16), green_on, (34, 197, 94))

        timeline_x = 68
        timeline_y = 506
        for s in range(12):
            fill = (37, 99, 235) if s == idx else (203, 213, 225)
            draw.rounded_rectangle((timeline_x + s * 66, timeline_y, timeline_x + s * 66 + 48, timeline_y + 18), radius=9, fill=fill)
            draw.text((timeline_x + s * 66 + 12, timeline_y + 25), str(s), font=font(14, True), fill=(30, 41, 59))
        draw.text((60, 548), "Chu ky: xanh -> vang -> toan do, lap lai cho 4 huong.", font=font(16), fill=(71, 85, 105))
        frames.append(img)

    frames[0].save(
        ASSETS / "roundabout-motion.gif",
        save_all=True,
        append_images=frames[1:],
        duration=650,
        loop=0,
        optimize=True,
    )


def make_preview():
    src = ROOT / "tools" / "circuitjs-local" / "test-artifacts" / "stable-counter-0.png"
    if not src.exists():
        return
    img = Image.open(src).convert("RGB")
    # Remove the right-side simulator controls so the circuit is readable in README.
    cropped = img.crop((0, 0, min(1435, img.width), img.height))
    preview = ImageOps.contain(cropped, (1280, 720), method=Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (1280, 720), (15, 23, 42))
    x = (1280 - preview.width) // 2
    y = (720 - preview.height) // 2
    canvas.paste(preview, (x, y))
    canvas.save(ASSETS / "circuitjs-preview.png", quality=92)


if __name__ == "__main__":
    svg_hero()
    make_motion_gif()
    make_preview()
    for file in sorted(ASSETS.iterdir()):
        print(f"{file.name}: {file.stat().st_size} bytes")
