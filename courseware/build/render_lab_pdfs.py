#!/usr/bin/env python3
"""Render every Markdown file in a labs/ or activities/ tree to a same-basename PDF."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    Image as RLImage,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

BLUE = colors.HexColor("#1F6FEB")
TEAL = colors.HexColor("#10B981")
INK = colors.HexColor("#161B26")
GREY = colors.HexColor("#5B6372")
LINE = colors.HexColor("#D9E2EC")
LIGHT = colors.HexColor("#F5F8FC")


def font_names() -> tuple[str, str]:
    candidates = [
        (Path("/Library/Fonts/Arial.ttf"), Path("/Library/Fonts/Arial Bold.ttf")),
        (Path("/System/Library/Fonts/Supplemental/Arial.ttf"), Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")),
    ]
    for regular, bold in candidates:
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont("CourseArial", str(regular)))
            pdfmetrics.registerFont(TTFont("CourseArialBold", str(bold)))
            return "CourseArial", "CourseArialBold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = font_names()


def ascii_dashes(text: str) -> str:
    return (
        text.replace("\u2010", "-")
        .replace("\u2011", "-")
        .replace("\u2012", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
        .replace("\u00b7", "|")
    )


def inline_markup(text: str) -> str:
    text = ascii_dashes(text)
    links: list[tuple[str, str]] = []

    def stash_link(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        if target.lower().endswith(".md"):
            target = target[:-3] + ".pdf"
        links.append((label, target))
        return f"@@LINK{len(links)-1}@@"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", stash_link, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", rf'<font name="{FONT}">\1</font>', text)
    for i, (label, target) in enumerate(links):
        text = text.replace(
            f"@@LINK{i}@@",
            f'<link href="{html.escape(target, quote=True)}" color="#1F6FEB"><u>{html.escape(ascii_dashes(label))}</u></link>',
        )
    return text


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ActivityTitle", parent=base["Title"], fontName=FONT_BOLD, fontSize=21,
            leading=25, textColor=INK, alignment=TA_LEFT, spaceAfter=9, keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "ActivityH2", parent=base["Heading2"], fontName=FONT_BOLD, fontSize=15,
            leading=19, textColor=BLUE, spaceBefore=9, spaceAfter=5, keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "ActivityH3", parent=base["Heading3"], fontName=FONT_BOLD, fontSize=12,
            leading=15, textColor=TEAL, spaceBefore=9, spaceAfter=5, keepWithNext=True,
        ),
        "h4": ParagraphStyle(
            "ActivityH4", parent=base["Heading4"], fontName=FONT_BOLD, fontSize=10.5,
            leading=13, textColor=INK, spaceBefore=7, spaceAfter=4, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "ActivityBody", parent=base["BodyText"], fontName=FONT, fontSize=9.6,
            leading=13.2, textColor=INK, spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "ActivitySmall", parent=base["BodyText"], fontName=FONT, fontSize=8.3,
            leading=11, textColor=GREY, spaceAfter=4,
        ),
        "list": ParagraphStyle(
            "ActivityList", parent=base["BodyText"], fontName=FONT, fontSize=9.4,
            leading=13, textColor=INK, leftIndent=2 * mm, firstLineIndent=0, spaceAfter=2,
        ),
        "number": ParagraphStyle(
            "ActivityNumber", parent=base["BodyText"], fontName=FONT, fontSize=9.4,
            leading=12.5, textColor=INK, leftIndent=0, firstLineIndent=0, spaceAfter=2,
        ),
        "callout": ParagraphStyle(
            "ActivityCallout", parent=base["BodyText"], fontName=FONT, fontSize=9.2,
            leading=13, textColor=INK, backColor=LIGHT, borderColor=LINE,
            borderWidth=0.6, borderPadding=7, spaceBefore=4, spaceAfter=8,
        ),
        "code": ParagraphStyle(
            "ActivityCode", parent=base["BodyText"], fontName="Courier", fontSize=8.2,
            leading=10.6, textColor=INK, spaceBefore=0, spaceAfter=0,
        ),
        "cell": ParagraphStyle(
            "ActivityCell", parent=base["BodyText"], fontName=FONT, fontSize=8.6,
            leading=11.5, textColor=INK, spaceAfter=0,
        ),
        "cellhead": ParagraphStyle(
            "ActivityCellHead", parent=base["BodyText"], fontName=FONT_BOLD, fontSize=8.6,
            leading=11.5, textColor=INK, spaceAfter=0,
        ),
    }


def writing_lines(count: int = 4):
    out = []
    for _ in range(count):
        out.extend([Spacer(1, 6 * mm), HRFlowable(width="100%", thickness=0.45, color=LINE)])
    out.append(Spacer(1, 2 * mm))
    return out


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_divider(line: str) -> bool:
    return bool(re.fullmatch(r"\|?[\s:\-|]+\|[\s:\-|]*", line.strip())) and "-" in line


def table_block(rows: list[list[str]], st, width: float):
    """Render a markdown table as a real table so cells never collapse into prose."""
    cols = max(len(r) for r in rows)
    data = []
    for n, row in enumerate(rows):
        row = row + [""] * (cols - len(row))
        style = st["cellhead"] if n == 0 else st["cell"]
        data.append([Paragraph(inline_markup(c) or "&nbsp;", style) for c in row])
    table = Table(data, colWidths=[width / cols] * cols, hAlign="LEFT", repeatRows=1)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def target_image_ratio(path: Path) -> float:
    from PIL import Image
    with Image.open(path) as im: return im.height/im.width

def blocks(markdown: str, source: Path, width: float = 170 * mm):
    filename=source.name
    st = styles()
    out = []
    list_items: list[ListItem] = []

    def flush_list():
        nonlocal list_items
        if list_items:
            out.append(ListFlowable(list_items, bulletType="bullet", bulletFontName=FONT, bulletFontSize=8, leftIndent=14, bulletOffsetY=1))
            out.append(Spacer(1, 2 * mm))
            list_items = []

    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i].rstrip()
        line = raw.strip()
        if not line:
            flush_list(); i += 1; continue
        match_image=re.match(r"^!\[([^]]*)\]\(([^)]+)\)$",line)
        if match_image:
            flush_list()
            target=(source.parent/match_image.group(2)).resolve()
            if not target.is_file(): raise FileNotFoundError(target)
            out.append(RLImage(str(target),width=width,height=width*target_image_ratio(target)))
            out.append(Paragraph(inline_markup(match_image.group(1)),st["small"]))
            i+=1; continue
        if line.startswith("```"):
            flush_list()
            i += 1
            buf: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(ascii_dashes(lines[i].rstrip()))
                i += 1
            i += 1  # consume the closing fence
            while buf and not buf[-1].strip():
                buf.pop()
            if buf:
                # Preformatted keeps the exact spacing; the wrapper table paints the
                # tinted panel so the prompt reads as one copy-paste block.
                panel = Table([[Preformatted("\n".join(buf), st["code"], maxLineLength=95)]], colWidths=[width], hAlign="LEFT")
                panel.setStyle(TableStyle([
                    ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                    ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]))
                out.append(panel)
                out.append(Spacer(1, 3 * mm))
            continue
        if line.startswith("|") and i + 1 < len(lines) and is_divider(lines[i + 1]):
            flush_list()
            rows = [split_row(line)]
            i += 2  # header + divider
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            out.append(table_block(rows, st, width))
            out.append(Spacer(1, 3 * mm))
            continue
        if line.startswith("# "):
            flush_list(); out.append(Paragraph(inline_markup(line[2:]), st["title"])); out.append(HRFlowable(width="100%", thickness=1.6, color=TEAL, spaceAfter=5)); i += 1; continue
        if line.startswith("## "):
            flush_list(); out.append(Paragraph(inline_markup(line[3:]), st["h2"])); i += 1; continue
        if line.startswith("### "):
            flush_list(); out.append(Paragraph(inline_markup(line[4:]), st["h3"])); i += 1
            if "submission-template" in filename and (i >= len(lines) or not lines[i].strip() or lines[i].lstrip().startswith("###")):
                out.extend(writing_lines(4))
            continue
        if line.startswith("#### "):
            flush_list(); out.append(Paragraph(inline_markup(line[5:]), st["h4"])); i += 1; continue
        if line.startswith("> "):
            flush_list(); out.append(Paragraph(inline_markup(line[2:]), st["callout"])); i += 1; continue
        checkbox = re.match(r"^- \[([ xX])\]\s*(.*)$", line)
        if checkbox:
            flush_list()
            mark = "[x]" if checkbox.group(1).lower() == "x" else "[ ]"
            out.append(Paragraph(f"{mark}&nbsp;&nbsp;{inline_markup(checkbox.group(2))}", st["body"])); i += 1; continue
        if line == "-":
            flush_list(); out.extend(writing_lines(2)); i += 1; continue
        bullet = re.match(r"^-\s+(.*)$", line)
        if bullet:
            text = bullet.group(1).strip()
            if not text:
                flush_list(); out.extend(writing_lines(1))
            else:
                list_items.append(ListItem(Paragraph(inline_markup(text), st["list"]), leftIndent=10))
            i += 1; continue
        number = re.match(r"^(\d+)\.\s+(.*)$", line)
        if number:
            flush_list(); out.append(Paragraph(f"<b>{number.group(1)}.</b>&nbsp;&nbsp;{inline_markup(number.group(2))}", st["number"])); i += 1; continue

        flush_list()
        paragraph = line
        while i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            if not nxt or re.match(r"^(#{1,4}\s|[-*]\s|\d+\.\s|>\s)", nxt):
                break
            paragraph += " " + nxt
            i += 1
        out.append(Paragraph(inline_markup(paragraph), st["body"]));
        if "submission-template" in filename and re.fullmatch(r"\*\*Response:\*\*", line):
            out.extend(writing_lines(5))
        i += 1
    flush_list()
    return out


class LabDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, title: str, course_code: str):
        super().__init__(
            filename, pagesize=A4, leftMargin=17 * mm, rightMargin=17 * mm,
            topMargin=20 * mm, bottomMargin=15 * mm, title=title,
            author="Tertiary Infotech Academy Pte Ltd",
        )
        self.course_code = course_code
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
        self.addPageTemplates(PageTemplate(id="activity", frames=[frame], onPage=self.decorate))

    def decorate(self, canvas, doc):
        canvas.saveState()
        w, h = A4
        canvas.setFillColor(BLUE)
        canvas.rect(0, h - 7 * mm, w, 7 * mm, fill=1, stroke=0)
        canvas.setFont(FONT_BOLD, 8.5)
        canvas.setFillColor(GREY)
        canvas.drawString(17 * mm, h - 14 * mm, f"{self.course_code} | Lab Resource")
        canvas.setStrokeColor(LINE)
        canvas.line(17 * mm, 14 * mm, w - 17 * mm, 14 * mm)
        canvas.setFont(FONT, 8)
        canvas.drawString(17 * mm, 9 * mm, "Tertiary Infotech Academy Pte Ltd")
        canvas.drawRightString(w - 17 * mm, 9 * mm, f"Page {doc.page}")
        canvas.restoreState()


def course_code_for(root: Path) -> str:
    root_readme = root / "README.md"
    if root_readme.exists():
        m = re.search(r"\bTGS-\d+\b", root_readme.read_text(encoding="utf-8"))
        if m:
            return m.group(0)
    return "WSQ COURSEWARE"


def render(source: Path, course_code: str) -> Path:
    markdown = source.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", markdown, re.M)
    title = ascii_dashes(title_match.group(1)) if title_match else source.stem.replace("-", " ").title()
    target = source.with_suffix(".pdf")
    doc = LabDocTemplate(str(target), title, course_code)
    doc.build(blocks(markdown, source, doc.width))
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="activities", help="activities/ or labs/ directory")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Hands-on directory not found: {root}")
    sources = sorted(root.rglob("*.md"))
    if not sources:
        raise SystemExit(f"No Markdown files found under {root}")
    code = course_code_for(root)
    for source in sources:
        target = render(source, code)
        print(f"rendered {target.relative_to(root.parent)}")
    missing = [p for p in sources if not p.with_suffix(".pdf").exists()]
    if missing:
        raise SystemExit(f"Missing PDF counterparts: {missing}")
    print(f"PASS: {len(sources)} Markdown files -> {len(sources)} same-basename PDFs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
