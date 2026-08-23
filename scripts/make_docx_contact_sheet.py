import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "build" / "roundabout_docx_qa_v1"
OUTPUT = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else ROOT / "build" / "roundabout_docx_qa_v1_contact.png"
PAGE_SIZE = (230, 325)
LABEL_HEIGHT = 28
COLUMNS = 5
GAP = 18
MARGIN = 24


def natural_key(path):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.name)]


pages = sorted(SOURCE.glob("*.png"), key=natural_key)
if not pages:
    raise FileNotFoundError(f"No rendered PNG pages found in {SOURCE}")
rows = (len(pages) + COLUMNS - 1) // COLUMNS
width = MARGIN * 2 + COLUMNS * PAGE_SIZE[0] + (COLUMNS - 1) * GAP
height = MARGIN * 2 + rows * (PAGE_SIZE[1] + LABEL_HEIGHT) + (rows - 1) * GAP
sheet = Image.new("RGB", (width, height), "#d8dde3")
draw = ImageDraw.Draw(sheet)
font = ImageFont.load_default(size=18)

for index, page_path in enumerate(pages):
    row, column = divmod(index, COLUMNS)
    x = MARGIN + column * (PAGE_SIZE[0] + GAP)
    y = MARGIN + row * (PAGE_SIZE[1] + LABEL_HEIGHT + GAP)
    with Image.open(page_path) as page:
        thumbnail = page.convert("RGB")
        thumbnail.thumbnail(PAGE_SIZE, Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", PAGE_SIZE, "white")
        px = (PAGE_SIZE[0] - thumbnail.width) // 2
        py = (PAGE_SIZE[1] - thumbnail.height) // 2
        canvas.paste(thumbnail, (px, py))
        sheet.paste(canvas, (x, y))
    label = f"Page {index + 1:02d}"
    bbox = draw.textbbox((0, 0), label, font=font)
    draw.text(
        (x + (PAGE_SIZE[0] - (bbox[2] - bbox[0])) / 2, y + PAGE_SIZE[1] + 4),
        label,
        fill="#182330",
        font=font,
    )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
sheet.save(OUTPUT, optimize=True)
print(f"Created {OUTPUT} ({len(pages)} pages)")
