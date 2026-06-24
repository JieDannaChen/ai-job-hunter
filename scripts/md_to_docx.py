# /// script
# requires-python = ">=3.9"
# dependencies = ["python-docx"]
# ///
"""
Markdown to DOCX Resume Converter

Converts a Markdown resume file into a professionally formatted Word document.
Supports both English and Chinese content with proper formatting.

Usage:
    uv run scripts/md_to_docx.py input.md [output.docx]

If output path is omitted, writes to the same directory as input with .docx extension.
"""

import re
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# ── Theme ────────────────────────────────────────────────────────────────────

COLORS = {
    "heading": RGBColor(0x2C, 0x3E, 0x50),
    "subheading": RGBColor(0x2D, 0x5A, 0x8E),
    "body": RGBColor(0x33, 0x33, 0x33),
    "muted": RGBColor(0x55, 0x55, 0x55),
    "light": RGBColor(0x77, 0x77, 0x77),
    "separator": RGBColor(0xCC, 0xCC, 0xCC),
    "table_header_bg": "2d5a8e",
    "table_alt_bg": "f0f4f8",
    "white": RGBColor(0xFF, 0xFF, 0xFF),
}

FONTS = {
    "body": "Calibri",
    "size_body": Pt(10),
    "size_h1": Pt(22),
    "size_h2": Pt(12),
    "size_h3": Pt(11),
    "size_contact": Pt(9),
    "size_table": Pt(8.5),
    "size_table_header": Pt(9),
    "size_tech": Pt(9),
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def set_cell_shading(cell, color_hex: str):
    """Apply background shading to a table cell."""
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), color_hex)
    shading.set(qn("w:val"), "clear")
    cell._tc.get_or_add_tcPr().append(shading)


def add_run_with_bold_markers(paragraph, text: str, font_size=None):
    """Parse **bold** markers in text and add runs accordingly."""
    parts = re.split(r"(\*\*.*?\*\*)", text)
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        else:
            run = paragraph.add_run(part)
        if font_size:
            run.font.size = font_size


# ── Markdown Parser ─────────────────────────────────────────────────────────

class MarkdownSection:
    """Represents a parsed section of markdown content."""
    def __init__(self, level: int, title: str):
        self.level = level
        self.title = title
        self.content_lines: list[str] = []
        self.table_rows: list[list[str]] = []
        self.is_table = False


def parse_markdown(md_text: str) -> list[MarkdownSection]:
    """Parse markdown text into structured sections."""
    sections: list[MarkdownSection] = []
    current = MarkdownSection(0, "preamble")
    in_table = False
    table_rows: list[list[str]] = []

    for line in md_text.split("\n"):
        stripped = line.strip()

        # Heading
        if stripped.startswith("#"):
            # Flush table
            if table_rows:
                current.table_rows = table_rows
                current.is_table = True
                table_rows = []
                in_table = False

            sections.append(current)
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped.lstrip("# ").strip()
            current = MarkdownSection(level, title)
            continue

        # Table row
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            # Skip separator rows (|---|---|)
            if all(re.match(r"^[-:]+$", c) for c in cells):
                continue
            table_rows.append(cells)
            in_table = True
            continue

        # End of table
        if in_table and not stripped.startswith("|"):
            current.table_rows = table_rows
            current.is_table = True
            table_rows = []
            in_table = False

        # Separator (--- on its own line)
        if stripped == "---":
            current.content_lines.append("---SEPARATOR---")
            continue

        # Regular content
        if stripped:
            current.content_lines.append(stripped)

    # Flush final
    if table_rows:
        current.table_rows = table_rows
        current.is_table = True
    sections.append(current)

    return [s for s in sections if s.title or s.content_lines or s.table_rows]


# ── Document Builder ─────────────────────────────────────────────────────────

class ResumeDocBuilder:
    """Builds a formatted DOCX from parsed markdown sections."""

    def __init__(self):
        self.doc = Document()
        self._setup_document()

    def _setup_document(self):
        """Configure page margins and default style."""
        for section in self.doc.sections:
            section.top_margin = Cm(1.5)
            section.bottom_margin = Cm(1.5)
            section.left_margin = Cm(2.0)
            section.right_margin = Cm(2.0)

        style = self.doc.styles["Normal"]
        style.font.name = FONTS["body"]
        style.font.size = FONTS["size_body"]
        style.font.color.rgb = COLORS["body"]
        style.paragraph_format.space_after = Pt(2)
        style.paragraph_format.space_before = Pt(1)
        style.paragraph_format.line_spacing = 1.15

    def add_h1(self, text: str):
        h = self.doc.add_heading(text, level=1)
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in h.runs:
            run.font.size = FONTS["size_h1"]
            run.font.color.rgb = COLORS["heading"]
        h.paragraph_format.space_after = Pt(2)

    def add_h2(self, text: str):
        h = self.doc.add_heading(text, level=2)
        for run in h.runs:
            run.font.size = FONTS["size_h2"]
            run.font.color.rgb = COLORS["heading"]
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(3)

    def add_h3(self, text: str):
        p = self.doc.add_paragraph()
        run = p.add_run(text)
        run.bold = True
        run.font.size = FONTS["size_h3"]
        run.font.color.rgb = COLORS["subheading"]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)

    def add_contact(self, text: str):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.size = FONTS["size_contact"]
        run.font.color.rgb = COLORS["muted"]
        p.paragraph_format.space_after = Pt(1)

    def add_separator(self):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run("\u2500" * 80)
        run.font.size = Pt(4)
        run.font.color.rgb = COLORS["separator"]

    def add_body(self, text: str):
        p = self.doc.add_paragraph()
        add_run_with_bold_markers(p, text, FONTS["size_body"])
        p.paragraph_format.space_after = Pt(3)

    def add_bullet(self, text: str):
        p = self.doc.add_paragraph(style="List Bullet")
        p.clear()
        add_run_with_bold_markers(p, text, FONTS["size_body"])
        p.paragraph_format.space_after = Pt(1)

    def add_table(self, rows: list[list[str]], has_header: bool = True):
        if not rows:
            return
        table = self.doc.add_table(rows=len(rows), cols=len(rows[0]))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        for row_idx, row_data in enumerate(rows):
            for col_idx, cell_text in enumerate(row_data):
                cell = table.rows[row_idx].cells[col_idx]
                cell.text = ""
                p = cell.paragraphs[0]

                if row_idx == 0 and has_header:
                    run = p.add_run(cell_text)
                    run.bold = True
                    run.font.size = FONTS["size_table_header"]
                    run.font.color.rgb = COLORS["white"]
                    set_cell_shading(cell, COLORS["table_header_bg"])
                else:
                    run = p.add_run(cell_text)
                    run.font.size = FONTS["size_table"]
                    if row_idx % 2 == 0 and has_header:
                        set_cell_shading(cell, COLORS["table_alt_bg"])

    def build_from_sections(self, sections: list[MarkdownSection]):
        """Build the document from parsed markdown sections."""
        is_first_h1 = True

        for section in sections:
            # Headings
            if section.level == 1:
                if is_first_h1:
                    self.add_h1(section.title)
                    is_first_h1 = False
                else:
                    self.add_h1(section.title)
            elif section.level == 2:
                self.add_h2(section.title)
            elif section.level >= 3:
                self.add_h3(section.title)

            # Tables
            if section.table_rows:
                self.add_table(section.table_rows)

            # Content lines
            for line in section.content_lines:
                if line == "---SEPARATOR---":
                    self.add_separator()
                elif line.startswith("- ") or line.startswith("* "):
                    self.add_bullet(line[2:])
                elif line.startswith("**") and line.endswith("**") and len(line) < 80:
                    # Standalone bold line -> sub-section label
                    self.add_h3(line.strip("* "))
                else:
                    self.add_body(line)

    def save(self, path: str):
        self.doc.save(path)


# ── Main ─────────────────────────────────────────────────────────────────────

def convert(input_path: str, output_path: str | None = None):
    """Convert a Markdown file to a formatted DOCX resume."""
    inp = Path(input_path)
    if not inp.exists():
        print(f"Error: Input file not found: {inp}")
        sys.exit(1)

    if output_path is None:
        output_path = str(inp.with_suffix(".docx"))

    md_text = inp.read_text(encoding="utf-8")
    sections = parse_markdown(md_text)

    builder = ResumeDocBuilder()
    builder.build_from_sections(sections)
    builder.save(output_path)

    print(f"Converted: {inp} -> {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/md_to_docx.py <input.md> [output.docx]")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
