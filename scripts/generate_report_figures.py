from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\DienTuSo")
OUT = ROOT / "assets" / "seminar"
OUT.mkdir(parents=True, exist_ok=True)

FONT_REGULAR = Path(r"C:\Windows\Fonts\times.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\timesbd.ttf")

INK = "#17232d"
NAVY = "#173b57"
BLUE = "#2f6690"
GREEN = "#2f7d4a"
PALE_GREEN = "#dff1e5"
AMBER = "#b26a00"
PALE_AMBER = "#fff0cc"
RED = "#a3332b"
LIGHT = "#f4f7f9"
MID = "#d8e0e6"
GRAY = "#66737d"
WHITE = "#ffffff"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size=size)


def centered(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, fnt, fill=INK) -> None:
    box = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=8, align="center")
    x, y = xy
    draw.multiline_text((x - (box[2] - box[0]) / 2, y - (box[3] - box[1]) / 2), text, font=fnt, fill=fill, spacing=8, align="center")


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], fill=NAVY, width=5) -> None:
    draw.line([start, end], fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    head = 18
    wing = 0.55
    p1 = (end[0] - head * math.cos(angle - wing), end[1] - head * math.sin(angle - wing))
    p2 = (end[0] - head * math.cos(angle + wing), end[1] - head * math.sin(angle + wing))
    draw.polygon([end, p1, p2], fill=fill)


def architecture_diagram() -> None:
    image = Image.new("RGB", (3200, 1320), WHITE)
    draw = ImageDraw.Draw(image)
    centered(draw, (1600, 78), "Overall architecture and clock-flow control", font(58, True), NAVY)

    def block(box, title, detail, color=NAVY):
        draw.rounded_rectangle(box, radius=22, fill=LIGHT, outline=color, width=5)
        x1, y1, x2, y2 = box
        centered(draw, ((x1 + x2) / 2, y1 + 54), title, font(36, True), color)
        centered(draw, ((x1 + x2) / 2, (y1 + y2) / 2 + 32), detail, font(29), INK)

    def branch_label(center_xy, text, color):
        cx, cy = center_xy
        text_box = draw.textbbox((0, 0), text, font=font(28, True))
        half_w = (text_box[2] - text_box[0]) // 2 + 18
        half_h = (text_box[3] - text_box[1]) // 2 + 12
        draw.rounded_rectangle(
            (cx - half_w, cy - half_h, cx + half_w, cy + half_h),
            radius=12,
            fill=WHITE,
            outline=color,
            width=3,
        )
        centered(draw, (cx, cy), text, font(28, True), color)

    pulse = (80, 485, 420, 705)
    selector = (540, 485, 920, 705)
    automatic = (1050, 220, 1490, 430)
    manual = (1030, 800, 1530, 1045)
    merge = (1680, 485, 2010, 705)
    counter = (2160, 450, 2570, 740)
    decoder = (2700, 435, 3140, 755)

    block(pulse, "Pulse generator", "NE555 astable\nclock source", GREEN)
    block(selector, "Mode selector", "2-to-1 multiplexer\nM = 0: automatic\nM = 1: manual", BLUE)
    block(automatic, "Automatic branch", "Clock passes directly\nwithout operator intervention", GREEN)
    block(manual, "Manual-control branch", "Operator request -> SR latch\nclock gate -> one controlled advance", AMBER)
    block(merge, "Selected clock", "CLK_sel", BLUE)
    block(counter, "Synchronous counter", "Four JK flip-flops\n10-state 4-1-4-1 cycle", NAVY)
    block(decoder, "Lamp decoder", "A/C and B/D\nred-yellow-green outputs", RED)

    arrow(draw, (420, 595), (540, 595))
    arrow(draw, (920, 555), (1050, 325))
    arrow(draw, (920, 635), (1020, 920), AMBER)
    arrow(draw, (1490, 325), (1680, 555), GREEN)
    arrow(draw, (1530, 920), (1680, 635), AMBER)
    arrow(draw, (2010, 595), (2160, 595))
    arrow(draw, (2570, 595), (2700, 595))

    branch_label((965, 385), "M = 0", GREEN)
    branch_label((865, 765), "M = 1", AMBER)
    arrow(draw, (1125, 1120), (1125, 1045), AMBER)
    draw.text((1170, 1082), "Traffic-operator enable", font=font(28, True), fill=AMBER)
    draw.text((102, 1175), "Safety invariant: A/C and B/D are never green simultaneously.", font=font(31, True), fill=RED)
    draw.text((102, 1225), "All state changes are synchronized by the selected falling clock edge used by the Falstad JK elements.", font=font(29), fill=GRAY)
    image.save(OUT / "01_overall_architecture.png")


STATE_ORDER = [8, 9, 10, 11, 12, 0, 1, 2, 3, 4]


def bits(state: int) -> tuple[int, int, int, int]:
    return tuple((state >> shift) & 1 for shift in (3, 2, 1, 0))


def phase(state: int) -> tuple[str, str, str]:
    if 8 <= state <= 11:
        return "A/C green", "B/D red", GREEN
    if state == 12:
        return "A/C yellow", "B/D red", AMBER
    if 0 <= state <= 3:
        return "A/C red", "B/D green", BLUE
    if state == 4:
        return "A/C red", "B/D yellow", AMBER
    raise ValueError(state)


def state_diagram() -> None:
    image = Image.new("RGB", (2600, 1760), WHITE)
    draw = ImageDraw.Draw(image)
    centered(draw, (1300, 80), "Optimized 10-state sequence (4-1-4-1)", font(60, True), NAVY)
    center = (1300, 920)
    rx, ry = 930, 610
    points = []
    for index, state in enumerate(STATE_ORDER):
        angle = -math.pi / 2 + index * 2 * math.pi / len(STATE_ORDER)
        points.append((int(center[0] + rx * math.cos(angle)), int(center[1] + ry * math.sin(angle))))

    for index, point in enumerate(points):
        nxt = points[(index + 1) % len(points)]
        vx, vy = nxt[0] - point[0], nxt[1] - point[1]
        length = math.hypot(vx, vy)
        start = (int(point[0] + 115 * vx / length), int(point[1] + 84 * vy / length))
        end = (int(nxt[0] - 115 * vx / length), int(nxt[1] - 84 * vy / length))
        arrow(draw, start, end, GRAY, 5)

    for point, state in zip(points, STATE_ORDER):
        ac, bd, color = phase(state)
        x, y = point
        draw.rounded_rectangle((x - 150, y - 93, x + 150, y + 93), radius=24, fill=WHITE, outline=color, width=6)
        centered(draw, (x, y - 36), f"S{state}: {state:04b}", font(33, True), color)
        centered(draw, (x, y + 27), f"{ac}\n{bd}", font(25), INK)

    centered(draw, (1300, 890), "One selected clock edge\nper transition", font(38, True), NAVY)
    centered(draw, (1300, 1030), "Unused binary states\n5, 6, 7, 13, 14, 15", font(27), GRAY)
    draw.text((180, 1650), "Grouping: 4 counts A/C green -> 1 count A/C yellow -> 4 counts B/D green -> 1 count B/D yellow.", font=font(31, True), fill=INK)
    image.save(OUT / "02_state_diagram.png")


def next_state(state: int) -> int:
    q3, q2, q1, q0 = bits(state)
    j3 = k3 = q2
    j2, k2 = q1 & q0, 1
    j1 = k1 = q0
    j0, k0 = 1 - q2, 1

    def jk(q, j, k):
        return (j & (1 - q)) | ((1 - k) & q)

    values = [jk(q3, j3, k3), jk(q2, j2, k2), jk(q1, j1, k1), jk(q0, j0, k0)]
    return sum(value << shift for value, shift in zip(values, (3, 2, 1, 0)))


def excitation(q: int, qn: int) -> tuple[str, str]:
    if q == 0 and qn == 0:
        return "0", "X"
    if q == 0 and qn == 1:
        return "1", "X"
    if q == 1 and qn == 0:
        return "X", "1"
    return "X", "0"


VALID = set(STATE_ORDER)
EXPR = {
    "J3": "J3 = Q2",
    "K3": "K3 = Q2",
    "J2": "J2 = Q1 Q0",
    "K2": "K2 = 1",
    "J1": "J1 = Q0",
    "K1": "K1 = Q0",
    "J0": "J0 = Q2'",
    "K0": "K0 = 1",
}


def excitation_maps() -> dict[str, dict[int, str]]:
    maps = {name: {state: "X" for state in range(16)} for name in EXPR}
    for state in STATE_ORDER:
        nxt = STATE_ORDER[(STATE_ORDER.index(state) + 1) % len(STATE_ORDER)]
        present = bits(state)
        future = bits(nxt)
        for index in range(4):
            j, k = excitation(present[index], future[index])
            bit_index = 3 - index
            maps[f"J{bit_index}"][state] = j
            maps[f"K{bit_index}"][state] = k
    return maps


def kmap_diagram() -> None:
    maps = excitation_maps()
    image = Image.new("RGB", (3000, 2200), WHITE)
    draw = ImageDraw.Draw(image)
    centered(draw, (1500, 70), "JK excitation Karnaugh maps", font(60, True), NAVY)
    gray = ["00", "01", "11", "10"]
    panel_w, panel_h = 700, 930
    origin_x, origin_y = 85, 150
    gap_x, gap_y = 35, 65
    cell = 112

    for panel_index, name in enumerate(EXPR):
        row_panel, col_panel = divmod(panel_index, 4)
        px = origin_x + col_panel * (panel_w + gap_x)
        py = origin_y + row_panel * (panel_h + gap_y)
        draw.rounded_rectangle((px, py, px + panel_w, py + panel_h), radius=20, fill="#fbfcfd", outline=MID, width=4)
        centered(draw, (px + panel_w / 2, py + 55), name, font(42, True), NAVY)
        draw.text((px + 40, py + 120), "Rows: Q3Q2", font=font(27, True), fill=INK)
        draw.text((px + 365, py + 120), "Columns: Q1Q0", font=font(27, True), fill=INK)
        grid_x, grid_y = px + 150, py + 220
        for col, label in enumerate(gray):
            centered(draw, (grid_x + col * cell + cell / 2, grid_y - 42), label, font(26, True), INK)
        for row, label in enumerate(gray):
            centered(draw, (grid_x - 48, grid_y + row * cell + cell / 2), label, font(26, True), INK)
        for row, rq in enumerate(gray):
            for col, cq in enumerate(gray):
                state = int(rq + cq, 2)
                value = maps[name][state]
                fill = PALE_GREEN if value == "1" else ("#eef1f3" if value == "X" else WHITE)
                box = (grid_x + col * cell, grid_y + row * cell, grid_x + (col + 1) * cell, grid_y + (row + 1) * cell)
                draw.rectangle(box, fill=fill, outline=GRAY, width=3)
                centered(draw, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), value, font(34, True), GREEN if value == "1" else GRAY)
        centered(draw, (px + panel_w / 2, py + 755), EXPR[name], font(34, True), RED)
        centered(draw, (px + panel_w / 2, py + 820), "X = don't care", font(24), GRAY)

    draw.text((100, 2120), "Gray ordering is used on both axes. Invalid counter states and irrelevant JK inputs are treated as don't-care cells.", font=font(29), fill=GRAY)
    image.save(OUT / "03_jk_karnaugh_maps.png")
    # Pair crops follow complete panel boundaries so adjacent titles and borders
    # cannot leak into the enlarged Word figures.
    image.crop((65, 130, 1540, 1100)).save(OUT / "03a_kmap_j3_k3.png")
    image.crop((1535, 130, 3000, 1100)).save(OUT / "03b_kmap_j2_k2.png")
    image.crop((65, 1125, 1540, 2095)).save(OUT / "03c_kmap_j1_k1.png")
    image.crop((1535, 1125, 3000, 2095)).save(OUT / "03d_kmap_j0_k0.png")


def timing_diagram() -> None:
    samples = STATE_ORDER + [STATE_ORDER[0]]
    labels = ["Q3", "Q2", "Q1", "Q0", "G_AC", "Y_AC", "R_AC", "G_BD", "Y_BD", "R_BD"]

    def outputs(state: int) -> list[int]:
        q3, q2, _, _ = bits(state)
        return [q3, q2, bits(state)[2], bits(state)[3], q3 & (1 - q2), q3 & q2, 1 - q3, (1 - q3) & (1 - q2), (1 - q3) & q2, q3]

    image = Image.new("RGB", (3000, 1900), WHITE)
    draw = ImageDraw.Draw(image)
    centered(draw, (1500, 70), "One complete counter cycle and decoded lamp phases", font(58, True), NAVY)
    left, right = 310, 2860
    top, row_h = 235, 135
    step = (right - left) / len(STATE_ORDER)
    wave_font = font(27, True)

    for index, state in enumerate(STATE_ORDER):
        x = left + index * step
        fill = PALE_GREEN if 8 <= state <= 11 or 0 <= state <= 3 else PALE_AMBER
        draw.rectangle((x, 145, x + step, 1840), fill=fill)
        centered(draw, (x + step / 2, 190), f"S{state}\n{state:04b}", font(24, True), INK)
        draw.line((x, 145, x, 1840), fill=MID, width=2)
    draw.line((right, 145, right, 1840), fill=MID, width=2)

    for row, label in enumerate(labels):
        base = top + row * row_h
        draw.text((85, base + 25), label, font=wave_font, fill=INK)
        draw.line((left, base + 90, right, base + 90), fill=MID, width=2)
        values = [outputs(state)[row] for state in samples]
        pts = []
        for index in range(len(samples)):
            x = left + index * step
            y = base + (18 if values[index] else 82)
            if index > 0:
                pts.append((x, base + (18 if values[index - 1] else 82)))
            pts.append((x, y))
        color = NAVY if row < 4 else (GREEN if label.startswith("G") else AMBER if label.startswith("Y") else RED)
        draw.line(pts, fill=color, width=6)

    centered(draw, (left + 2.5 * step, 1780), "A/C green window", font(29, True), GREEN)
    centered(draw, (left + 4.5 * step, 1780), "A/C yellow", font(26, True), AMBER)
    centered(draw, (left + 7.0 * step, 1780), "B/D green window", font(29, True), BLUE)
    centered(draw, (left + 9.5 * step, 1780), "B/D yellow", font(26, True), AMBER)
    image.save(OUT / "04_timing_diagram.png")


def write_analysis_data() -> None:
    rows = []
    maps = excitation_maps()
    for state in STATE_ORDER:
        nxt = STATE_ORDER[(STATE_ORDER.index(state) + 1) % len(STATE_ORDER)]
        ac, bd, _ = phase(state)
        row = {
            "state": state,
            "present": f"{state:04b}",
            "next": f"{nxt:04b}",
            "ac": ac,
            "bd": bd,
        }
        for name in EXPR:
            row[name] = maps[name][state]
        rows.append(row)
    all_transitions = {state: next_state(state) for state in range(16)}
    payload = {"state_order": STATE_ORDER, "rows": rows, "all_transitions": all_transitions, "expressions": EXPR}
    (OUT / "counter_analysis.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    architecture_diagram()
    state_diagram()
    kmap_diagram()
    timing_diagram()
    write_analysis_data()
    print(f"Generated report figures and counter data in {OUT}")
