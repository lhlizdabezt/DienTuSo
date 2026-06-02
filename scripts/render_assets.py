from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


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


TITLE = font(32, True)
SUB = font(16)
CARD = font(18, True)
SMALL = font(13)
STATE = font(24, True)


def draw_light(draw, center, active, color):
    x, y = center
    fill = color if active else (51, 65, 85)
    outline = tuple(min(255, c + 55) for c in color) if active else (148, 163, 184)
    draw.ellipse((x - 13, y - 13, x + 13, y + 13), fill=fill, outline=outline, width=3)


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
        ("Lane A green", "A", "green"),
        ("Lane A yellow", "A", "yellow"),
        ("All red", None, "red"),
        ("Lane B green", "B", "green"),
        ("Lane B yellow", "B", "yellow"),
        ("All red", None, "red"),
        ("Lane C green", "C", "green"),
        ("Lane C yellow", "C", "yellow"),
        ("All red", None, "red"),
        ("Lane D green", "D", "green"),
        ("Lane D yellow", "D", "yellow"),
        ("All red", None, "red"),
    ]
    label, active_lane, active_mode = states[index]
    img = Image.new("RGB", (960, 400), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((24, 22, 936, 378), radius=26, fill=(248, 250, 252))
    draw.text((52, 44), "Roundabout Traffic-Light Controller", font=TITLE, fill=(15, 23, 42))
    draw.text((54, 84), "Mod-12 counter, JK flip-flops, state decoder and CircuitJS simulation.", font=SUB, fill=(71, 85, 105))

    lane_boxes = {
        "A": (58, 132, 218, 230),
        "B": (278, 132, 438, 230),
        "C": (498, 132, 658, 230),
        "D": (718, 132, 878, 230),
    }
    for lane, box in lane_boxes.items():
        if active_lane is None:
            mode = "red"
        elif lane == active_lane:
            mode = active_mode
        else:
            mode = "red"
        draw_lane(draw, box, f"Lane {lane}", mode)

    draw.rounded_rectangle((58, 254, 878, 314), radius=18, fill=(226, 232, 240), outline=(100, 116, 139), width=3)
    draw.text((82, 271), "MOD-12 STATE", font=CARD, fill=(15, 23, 42))
    draw.text((256, 266), f"{index:02d}", font=STATE, fill=(37, 99, 235))
    draw.text((322, 273), label.upper(), font=CARD, fill=(15, 118, 110))

    draw.rounded_rectangle((58, 330, 878, 360), radius=14, fill=(226, 232, 240))
    draw.text((82, 338), "Cycle verified: green, yellow, all-red guard state, then next lane.", font=SMALL, fill=(71, 85, 105))
    return img


def main():
    frames = [frame(i) for i in range(12)]
    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=650, loop=0, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
