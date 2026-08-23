from __future__ import annotations

import json
import hashlib
import re
import sys
import zipfile
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
DOCX = (
    Path(sys.argv[1]).resolve()
    if len(sys.argv) > 1
    else ROOT / "25DTV_DKD3_22207056_24207030_RoundaboutTrafficLightController_Seminar.docx"
)
REPORT = ROOT / "build" / "roundabout_docx_qa.json"
HARDWARE_PHOTOS = [
    ROOT / "assets" / "seminar" / "hardware-front.jpg",
    ROOT / "assets" / "seminar" / "hardware-overview.jpg",
]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
EXPECTED = [
    "Lương Hải Long",
    "22207056",
    "Đoàn Minh Nhật",
    "24207030",
    "25DTV_DKD3",
    "ETC00002",
    "Bùi Trọng Tú",
    "2025-2026",
    "Physical prototype and bench verification",
    "Hardware bench-verification checklist",
    "https://youtu.be/cp_W2NxVCSE",
]
EXPECTED_MATH = [
    "Tth = 2 ln2 Rf C",
    "CLKsel = M′ CLKosc + M CLKman",
    "CLKman = Qm CLKosc",
    "Q+ = JQ′ + K′Q",
    "J3 = Q2",
    "K3 = Q2",
    "J2 = Q1Q0",
    "K2 = 1",
    "J1 = Q0",
    "K1 = Q0",
    "J0 = Q2′",
    "K0 = 1",
    "GAC = Q3Q2′ ;  YAC = Q3Q2 ;  RAC = Q3′",
    "GBD = Q3′Q2′ ;  YBD = Q3′Q2 ;  RBD = Q3",
]
BANNED = [
    "LmDp4KK5XG4",
    "roundabout_stable_counter_falstad_url",
    "circuit-20260523-1348",
]


def check(condition: bool, name: str, detail: str, results: list[dict]) -> None:
    results.append({"check": name, "pass": bool(condition), "detail": detail})


results: list[dict] = []
with zipfile.ZipFile(DOCX) as package:
    bad_member = package.testzip()
    check(bad_member is None, "ZIP package integrity", str(bad_member), results)
    relationships = package.read("word/_rels/document.xml.rels").decode("utf-8")
    document_xml = package.read("word/document.xml")
    relationships_xml = package.read("word/_rels/document.xml.rels")
    styles_xml = package.read("word/styles.xml").decode("utf-8")
    media = [name for name in package.namelist() if name.startswith("word/media/")]
    media_hashes = {
        hashlib.sha256(package.read(name)).hexdigest()
        for name in media
    }
    footer_xml = "\n".join(
        package.read(name).decode("utf-8")
        for name in package.namelist()
        if re.fullmatch(r"word/footer\d+\.xml", name)
    )

document = Document(DOCX)
visible_text = "\n".join(node.text or "" for node in document.element.iter(qn("w:t")))

for token in EXPECTED:
    check(token in visible_text, f"Required text: {token}", "present", results)
for token in BANNED:
    check(token.lower() not in (visible_text + relationships).lower(), f"Removed legacy source: {token}", "absent", results)
check("Signature" not in visible_text, "Academic-integrity signature table removed", "Signature label absent", results)

falstad_targets = re.findall(r'Target="([^"]*falstad\.com/circuit/circuitjs\.html\?ctz=[^"]+)"', relationships)
check(len(falstad_targets) >= 1 and len(set(falstad_targets)) == 1, "Only the new Falstad hyperlink", f"count={len(falstad_targets)}; unique={len(set(falstad_targets))}", results)
youtube_targets = re.findall(r'Target="([^"]*(?:youtu\.be|youtube\.com)/[^"]+)"', relationships)
check(youtube_targets == ["https://youtu.be/cp_W2NxVCSE"], "Only the new YouTube hyperlink", repr(youtube_targets), results)

rels_root = etree.fromstring(relationships_xml)
doc_root = etree.fromstring(document_xml)
styles_root = etree.fromstring(styles_xml.encode("utf-8"))
external_links = [
    (node.get("Id"), node.get("Target"))
    for node in rels_root
    if (node.get("Type") or "").endswith("/hyperlink") and node.get("TargetMode") == "External"
]
check(len(external_links) >= 9, "External reference hyperlinks", f"count={len(external_links)}", results)
check(all(target.startswith("https://") for _, target in external_links), "HTTPS-only external links", "all external targets use HTTPS", results)
word_ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
math_ns = {**word_ns, "m": "http://schemas.openxmlformats.org/officeDocument/2006/math"}
hyperlink_style = styles_root.xpath('.//w:style[@w:styleId="Hyperlink"]', namespaces=word_ns)
hyperlink_style_is_blue = bool(
    hyperlink_style
    and hyperlink_style[0].xpath('.//w:color[@w:val="0563C1"]', namespaces=word_ns)
    and hyperlink_style[0].xpath('.//w:u[@w:val="single"]', namespaces=word_ns)
)
blue_link_ids = []
for relationship_id, _ in external_links:
    nodes = doc_root.xpath(f'.//w:hyperlink[@r:id="{relationship_id}"]', namespaces=word_ns)
    if nodes and all(
        (
            node.xpath('.//w:color[@w:val="0563C1"]', namespaces=word_ns)
            or (hyperlink_style_is_blue and node.xpath('.//w:rStyle[@w:val="Hyperlink"]', namespaces=word_ns))
        )
        and (node.xpath('.//w:u', namespaces=word_ns) or hyperlink_style_is_blue)
        for node in nodes
    ):
        blue_link_ids.append(relationship_id)
check(len(blue_link_ids) == len(external_links), "Blue underlined external links", f"{len(blue_link_ids)}/{len(external_links)}", results)
check("PAGE" in footer_xml, "Footer page-number field", "PAGE field present", results)
check(len(media) >= 22, "Embedded visual assets", f"media={len(media)}", results)
for hardware_photo in HARDWARE_PHOTOS:
    photo_hash = hashlib.sha256(hardware_photo.read_bytes()).hexdigest()
    check(photo_hash in media_hashes, f"Embedded original hardware photograph: {hardware_photo.name}", "SHA-256 match", results)

math_nodes = doc_root.xpath(".//m:oMath", namespaces=math_ns)
math_texts = ["".join(node.xpath(".//m:t/text()", namespaces=math_ns)) for node in math_nodes]
normalize_math = lambda value: re.sub(r"\s+", " ", value.replace("′", "'")).strip()
normalized_math_texts = {normalize_math(value) for value in math_texts}
for expression in EXPECTED_MATH:
    check(normalize_math(expression) in normalized_math_texts, f"Native Word equation: {expression}", "present as OMML", results)
check(len(math_nodes) >= 70, "Native Word math coverage", f"OMML objects={len(math_nodes)}", results)
check(len(doc_root.xpath(".//m:f", namespaces=math_ns)) >= 5, "Professional stacked fractions", "OMML fractions present", results)
check(len(doc_root.xpath(".//m:sSub", namespaces=math_ns)) >= 100, "Mathematical subscripts", "OMML subscripts present", results)
check(len(doc_root.xpath(".//m:sSup", namespaces=math_ns)) >= 5, "Mathematical superscripts", "OMML superscripts present", results)
check(len(doc_root.xpath(".//m:sSubSup", namespaces=math_ns)) >= 8, "Complemented subscripted signals", "OMML subscript/superscript structures present", results)

plain_formula_fragments: list[str] = []
for paragraph in doc_root.xpath(".//w:p", namespaces=math_ns):
    plain = "".join(
        node.text or ""
        for node in paragraph.xpath(".//w:t[not(ancestor::m:oMath) and not(ancestor::w:hyperlink)]", namespaces=math_ns)
    ).strip()
    if "=" in plain:
        plain_formula_fragments.append(plain)
check(not plain_formula_fragments, "No keyboard-typed equations remain", repr(plain_formula_fragments), results)

figure_numbers = {int(value) for value in re.findall(r"Figure (\d+)\.", visible_text)}
table_numbers = {int(value) for value in re.findall(r"Table (\d+)\.", visible_text)}
check(figure_numbers == set(range(1, 23)), "Figure numbering", str(sorted(figure_numbers)), results)
check(table_numbers == set(range(1, 18)), "Table numbering", str(sorted(table_numbers)), results)

main_sections = list(document.sections)[1:]
margin_ok = all(
    abs(section.top_margin.inches - 0.7874) < 0.01
    and abs(section.bottom_margin.inches - 0.7874) < 0.01
    and abs(section.left_margin.inches - 0.9843) < 0.01
    and abs(section.right_margin.inches - 0.7874) < 0.01
    for section in main_sections
)
check(margin_ok, "Faculty margins", "top/bottom/right=2.0 cm; left=2.5 cm", results)
check(
    all(abs(section.page_width.inches - 8.2677) < 0.01 and abs(section.page_height.inches - 11.6929) < 0.01 for section in document.sections),
    "A4 page size",
    "210 x 297 mm",
    results,
)

narrative = []
for paragraph in doc_root.xpath("./w:body/w:p", namespaces=math_ns):
    paragraph_text = "".join(paragraph.xpath(".//w:t/text() | .//m:t/text()", namespaces=math_ns)).strip()
    has_hanging_indent = bool(paragraph.xpath("./w:pPr/w:ind[@w:hanging]", namespaces=math_ns))
    has_numbering = bool(paragraph.xpath("./w:pPr/w:numPr", namespaces=math_ns))
    paragraph_style = paragraph.xpath("string(./w:pPr/w:pStyle/@w:val)", namespaces=math_ns)
    if (
        len(paragraph_text) >= 100
        and not paragraph_text.startswith("DESIGN, SIMULATION, AND HARDWARE VERIFICATION")
        and not paragraph_text.startswith("Keywords:")
        and not has_hanging_indent
        and not has_numbering
        and paragraph_style not in {"Caption", "Heading1", "Heading2", "Heading3"}
    ):
        narrative.append(paragraph)
indented = [
    paragraph
    for paragraph in narrative
    if paragraph.xpath("string(./w:pPr/w:ind/@w:firstLine)", namespaces=math_ns) == "709"
]
check(len(indented) == len(narrative) and len(indented) >= 45, "Narrative first-line indent", f"{len(indented)}/{len(narrative)} at 1.25 cm", results)

check('w:ascii="Times New Roman"' in styles_xml, "Body typeface", "Times New Roman", results)
check('w:sz w:val="26"' in styles_xml, "Body type size", "13 pt", results)

payload = {
    "artifact": str(DOCX),
    "status": "PASS" if all(item["pass"] for item in results) else "FAIL",
    "checks_passed": sum(item["pass"] for item in results),
    "checks_total": len(results),
    "results": results,
}
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(payload, indent=2, ensure_ascii=False))
raise SystemExit(0 if payload["status"] == "PASS" else 1)
