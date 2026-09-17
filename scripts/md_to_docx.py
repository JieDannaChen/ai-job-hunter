# /// script
# requires-python = ">=3.9"
# dependencies = ["python-docx"]
# ///
"""
Markdown to DOCX Resume Converter

Converts a Markdown resume file into a professionally formatted Word document.
Supports both English and Chinese content with proper formatting.

Usage:
    uv run scripts/md_to_docx.py input.md [output.docx] [--theme classic|modern]

Themes:
    classic  - Original theme with neutral headings and separators (default)
    modern   - Modern blue theme with left accent bars on section headings,
               two-tone blue typography, and clean visual hierarchy
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Optional

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement


# ── Themes ───────────────────────────────────────────────────────────────────

THEMES = {
    "classic": {
        "colors": {
            "heading": RGBColor(0x2C, 0x3E, 0x50),
            "subheading": RGBColor(0x2D, 0x5A, 0x8E),
            "body": RGBColor(0x33, 0x33, 0x33),
            "muted": RGBColor(0x55, 0x55, 0x55),
            "light": RGBColor(0x77, 0x77, 0x77),
            "separator": RGBColor(0xCC, 0xCC, 0xCC),
            "table_header_bg": "2d5a8e",
            "table_alt_bg": "f0f4f8",
            "white": RGBColor(0xFF, 0xFF, 0xFF),
            "accent_bar": RGBColor(0x2D, 0x5A, 0x8E),
        },
        "fonts": {
            "body": "Calibri",
            "size_body": Pt(10),
            "size_h1": Pt(22),
            "size_h1_sub": Pt(12),
            "size_h2": Pt(12),
            "size_h3": Pt(11),
            "size_contact": Pt(9),
            "size_table": Pt(8.5),
            "size_table_header": Pt(9),
            "size_tech": Pt(9),
        },
        "h1_all_caps": False,
        "h2_left_bar": False,
        "h2_bottom_border": False,
        "subtitle_below_h1": False,
    },
    "modern": {
        "colors": {
            "heading": RGBColor(0x1A, 0x3A, 0x5C),      # Dark navy - section titles
            "subheading": RGBColor(0x2E, 0x7D, 0xB8),   # Medium blue - h3 / sub-modules
            "company": RGBColor(0x1A, 0x3A, 0x5C),      # Dark navy - company name
            "role": RGBColor(0x2E, 0x7D, 0xB8),         # Medium blue - role title
            "date_loc": RGBColor(0x5A, 0x6B, 0x7A),     # Muted - date/location
            "accent": RGBColor(0x2E, 0x7D, 0xB8),
            "accent_dark": RGBColor(0x1A, 0x3A, 0x5C),
            "body": RGBColor(0x2A, 0x2A, 0x2A),
            "muted": RGBColor(0x5A, 0x6B, 0x7A),
            "light": RGBColor(0x7A, 0x8A, 0x9A),
            "separator": RGBColor(0xC9, 0xD8, 0xE6),
            "table_header_bg": "1a3a5c",
            "table_alt_bg": "eef4fa",
            "white": RGBColor(0xFF, 0xFF, 0xFF),
            "accent_bar": RGBColor(0x2E, 0x7D, 0xB8),
        },
        "fonts": {
            "body": "Calibri",
            "size_body": Pt(10),
            "size_h1": Pt(26),
            "size_h1_sub": Pt(13),
            "size_h2": Pt(13),         # section titles (Professional Experience)
            "size_h3": Pt(10.5),       # sub-module titles
            "size_company": Pt(11.5),  # company name in experience
            "size_role": Pt(10.5),     # role title next to company
            "size_date_loc": Pt(9.5),  # date and location
            "size_contact": Pt(9.5),
            "size_table": Pt(8.5),
            "size_table_header": Pt(9),
            "size_tech": Pt(9),
        },
        "h1_all_caps": True,
        "h2_left_bar": True,
        "h2_bottom_border": True,
        "subtitle_below_h1": True,
    },
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def set_cell_shading(cell, color_hex: str):
    """Apply background shading to a table cell."""
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), color_hex)
    shading.set(qn("w:val"), "clear")
    cell._tc.get_or_add_tcPr().append(shading)


def add_run_with_bold_markers(paragraph, text: str, font_size=None, font_color=None):
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
        if font_color:
            run.font.color.rgb = font_color


def set_paragraph_left_border(paragraph, color_rgb, width_pt=4, space_pt=6):
    """Add a left border bar to a paragraph."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), str(int(width_pt * 8)))  # eighths of a point
    left.set(qn("w:space"), str(space_pt))
    left.set(qn("w:color"), "{:02x}{:02x}{:02x}".format(
        color_rgb[0] if isinstance(color_rgb, tuple) else color_rgb[0],
        color_rgb[1] if isinstance(color_rgb, tuple) else color_rgb[1],
        color_rgb[2] if isinstance(color_rgb, tuple) else color_rgb[2],
    ).upper())
    pBdr.append(left)
    pPr.append(pBdr)


def set_paragraph_bottom_border(paragraph, color_rgb, width_pt=0.75, space_pt=2):
    """Add a bottom border line to a paragraph."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(int(width_pt * 8)))
    bottom.set(qn("w:space"), str(space_pt))
    bottom.set(qn("w:color"), "{:02x}{:02x}{:02x}".format(
        color_rgb[0], color_rgb[1], color_rgb[2]
    ).upper())
    pBdr.append(bottom)
    pPr.append(pBdr)


def rgb_tuple(color):
    """Convert RGBColor to tuple."""
    if hasattr(color, "rgb"):
        c = color.rgb
        return (c[0], c[1], c[2])
    return (color[0], color[1], color[2])


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

        # Separator
        if stripped == "---":
            current.content_lines.append("---SEPARATOR---")
            continue

        # Italic line (company/role subline like *text*)
        if stripped.startswith("*") and stripped.endswith("*") and not stripped.startswith("**"):
            current.content_lines.append("---ITALIC---" + stripped.strip("*"))
            continue

        # Regular content
        if stripped:
            current.content_lines.append(stripped)

    if table_rows:
        current.table_rows = table_rows
        current.is_table = True
    sections.append(current)

    return [s for s in sections if s.title or s.content_lines or s.table_rows]


# ── Document Builder ─────────────────────────────────────────────────────────

class ResumeDocBuilder:
    """Builds a formatted DOCX from parsed markdown sections."""

    def __init__(self, theme: str = "classic"):
        self.theme_name = theme
        self.theme = THEMES.get(theme, THEMES["classic"])
        self.colors = self.theme["colors"]
        self.fonts = self.theme["fonts"]
        self.doc = Document()
        self._setup_document()
        self._is_first_h1 = True
        self._h1_subtitle_pending = None

    def _setup_document(self):
        """Configure page margins and default style."""
        for section in self.doc.sections:
            section.top_margin = Cm(1.5)
            section.bottom_margin = Cm(1.5)
            section.left_margin = Cm(2.0)
            section.right_margin = Cm(2.0)

        style = self.doc.styles["Normal"]
        style.font.name = self.fonts["body"]
        style.font.size = self.fonts["size_body"]
        style.font.color.rgb = self.colors["body"]
        style.paragraph_format.space_after = Pt(2)
        style.paragraph_format.space_before = Pt(1)
        style.paragraph_format.line_spacing = 1.15

    def add_h1(self, text: str):
        h = self.doc.add_paragraph()
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        display_text = text.upper() if self.theme["h1_all_caps"] else text
        run = h.add_run(display_text)
        run.bold = True
        run.font.size = self.fonts["size_h1"]
        run.font.color.rgb = self.colors["heading"]
        h.paragraph_format.space_after = Pt(1)
        h.paragraph_format.space_before = Pt(0)
        self._is_first_h1 = False

    def add_h2(self, text: str):
        h = self.doc.add_paragraph()
        run = h.add_run(text)
        run.bold = True
        run.font.size = self.fonts["size_h2"]
        run.font.color.rgb = self.colors["subheading"]
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(2)

        if self.theme["h2_left_bar"]:
            accent = self.colors.get("accent_dark", self.colors["subheading"])
            accent_tuple = (accent[0], accent[1], accent[2]) if hasattr(accent, "__getitem__") else accent
            set_paragraph_left_border(h, accent_tuple, width_pt=5, space_pt=7)

        if self.theme["h2_bottom_border"]:
            sep = self.colors.get("separator", self.colors["subheading"])
            sep_tuple = (sep[0], sep[1], sep[2]) if hasattr(sep, "__getitem__") else sep
            set_paragraph_bottom_border(h, sep_tuple, width_pt=0.5, space_pt=2)

    def add_h3(self, text: str):
        p = self.doc.add_paragraph()
        run = p.add_run(text)
        run.bold = True
        run.font.size = self.fonts.get("size_h3", self.fonts["size_h3"])
        run.font.color.rgb = self.colors["subheading"]
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(1)

    def add_company_role(self, company: str, role: str, date: str, location: str, desc: str = ""):
        """Add a formatted experience entry: company | role, date | location, description."""
        # Company and role on one line
        p = self.doc.add_paragraph()
        run = p.add_run(company)
        run.bold = True
        run.font.size = self.fonts.get("size_company", Pt(11.5))
        run.font.color.rgb = self.colors.get("company", self.colors["heading"])

        run2 = p.add_run("  |  ")
        run2.font.size = self.fonts.get("size_role", Pt(10.5))
        run2.font.color.rgb = self.colors.get("muted", self.colors["muted"])

        run3 = p.add_run(role)
        run3.bold = True
        run3.font.size = self.fonts.get("size_role", Pt(10.5))
        run3.font.color.rgb = self.colors.get("role", self.colors["subheading"])

        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(0)

        # Date and location on next line
        if date or location:
            p2 = self.doc.add_paragraph()
            date_loc = date
            if location:
                date_loc += "  |  " + location
            run = p2.add_run(date_loc)
            run.bold = True
            run.font.size = self.fonts.get("size_date_loc", Pt(9.5))
            run.font.color.rgb = self.colors.get("date_loc", self.colors["muted"])
            p2.paragraph_format.space_before = Pt(0)
            p2.paragraph_format.space_after = Pt(1)

        # Description (italic)
        if desc:
            p3 = self.doc.add_paragraph()
            run = p3.add_run(desc)
            run.italic = True
            run.font.size = self.fonts["size_body"]
            run.font.color.rgb = self.colors["muted"]
            p3.paragraph_format.space_before = Pt(0)
            p3.paragraph_format.space_after = Pt(2)

    def add_contact(self, text: str):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.size = self.fonts["size_contact"]
        run.font.color.rgb = self.colors["muted"]
        p.paragraph_format.space_after = Pt(1)

    def add_subtitle(self, text: str):
        """Add a subtitle line right below H1 (for modern theme)."""
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.bold = True
        run.font.size = self.fonts["size_h1_sub"]
        run.font.color.rgb = self.colors["subheading"]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)

    def add_italic_line(self, text: str):
        """Add an italic descriptive line (for company subheaders)."""
        p = self.doc.add_paragraph()
        run = p.add_run(text)
        run.italic = True
        run.font.size = self.fonts["size_body"]
        run.font.color.rgb = self.colors["muted"]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)

    def add_h4(self, text: str):
        """Add a sub-sub heading (for bullet group labels within experience)."""
        p = self.doc.add_paragraph()
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(10.5)
        run.font.color.rgb = self.colors["subheading"]
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(1)

    def add_separator(self):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        run = p.add_run("\u2500" * 80)
        run.font.size = Pt(4)
        run.font.color.rgb = self.colors["separator"]

    def add_body(self, text: str):
        p = self.doc.add_paragraph()
        add_run_with_bold_markers(p, text, self.fonts["size_body"])
        p.paragraph_format.space_after = Pt(3)

    def add_bullet(self, text: str):
        p = self.doc.add_paragraph(style="List Bullet")
        p.clear()
        add_run_with_bold_markers(p, text, self.fonts["size_body"])
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
                    run.font.size = self.fonts["size_table_header"]
                    run.font.color.rgb = self.colors["white"]
                    set_cell_shading(cell, self.colors["table_header_bg"])
                else:
                    run = p.add_run(cell_text)
                    run.font.size = self.fonts["size_table"]
                    if row_idx % 2 == 0 and has_header:
                        set_cell_shading(cell, self.colors["table_alt_bg"])

    def _looks_like_contact_line(self, text: str) -> bool:
        """Check if a line looks like contact info (phone, email, location, URLs)."""
        patterns = [
            r"\+?\d[\d\-\s()]{6,}",  # phone number
            r"[\w.+-]+@[\w.-]+\.[\w]+",  # email
            r"https?://",  # URL
            r"github\.com",  # GitHub
            r"linkedin\.com",  # LinkedIn
            r"portfolio",  # portfolio
            r"^Shanghai|^Beijing|^Shenzhen",  # city
            r"\|.*\|",  # pipe-separated contact items
        ]
        text_lower = text.lower()
        return any(re.search(p, text_lower) for p in patterns)

    def build_from_sections(self, sections: list[MarkdownSection]):
        """Build the document from parsed markdown sections."""
        in_header = False  # Track if we're still in the header area (h1 + contacts)

        for i, section in enumerate(sections):
            # Headings
            if section.level == 1:
                if self._is_first_h1:
                    self.add_h1(section.title)
                    in_header = True
                    # Check if next section is level 2 short (subtitle) - for modern theme
                    if self.theme["subtitle_below_h1"] and i + 1 < len(sections):
                        next_sec = sections[i + 1]
                        if next_sec.level == 2 and len(next_sec.title) < 80:
                            self.add_subtitle(next_sec.title)
                            next_sec._processed_as_subtitle = True
                    continue
                else:
                    in_header = False
                    self.add_h1(section.title)

            elif section.level == 2:
                if getattr(section, "_processed_as_subtitle", False):
                    pass
                else:
                    in_header = False
                    self.add_h2(section.title)

            elif section.level >= 3:
                in_header = False
                # In modern theme, detect "Company | Role | Date | Location" format
                if self.theme_name == "modern" and "|" in section.title and len(section.title) < 120:
                    parts = [p.strip() for p in section.title.split("|")]
                    company = parts[0]
                    role = parts[1] if len(parts) > 1 else ""
                    date = parts[2] if len(parts) > 2 else ""
                    location = parts[3] if len(parts) > 3 else ""
                    # Check if first content line is italic (description)
                    desc = ""
                    if section.content_lines and section.content_lines[0].startswith("---ITALIC---"):
                        desc = section.content_lines[0][len("---ITALIC---"):]
                        # Remove the italic line from content so it's not rendered twice
                        section.content_lines = section.content_lines[1:]
                    self.add_company_role(company, role, date, location, desc)
                else:
                    self.add_h3(section.title)

            # Tables
            if section.table_rows:
                in_header = False
                self.add_table(section.table_rows)

            # Content lines
            for line in section.content_lines:
                if line == "---SEPARATOR---":
                    in_header = False
                    self.add_separator()
                elif line.startswith("---ITALIC---"):
                    in_header = False
                    self.add_italic_line(line[len("---ITALIC---"):])
                elif line.startswith("- ") or line.startswith("* "):
                    in_header = False
                    self.add_bullet(line[2:])
                elif line.startswith("**") and line.endswith("**") and len(line) < 120:
                    in_header = False
                    self.add_h4(line.strip("* "))
                else:
                    if in_header and self.theme_name == "modern" and self._looks_like_contact_line(line):
                        self.add_contact(line)
                    else:
                        in_header = False
                        self.add_body(line)

    def save(self, path: str):
        self.doc.save(path)


# ── Main ─────────────────────────────────────────────────────────────────────

def convert(input_path: str, output_path: Optional[str] = None, theme: str = "classic"):
    """Convert a Markdown file to a formatted DOCX resume."""
    inp = Path(input_path)
    if not inp.exists():
        print(f"Error: Input file not found: {inp}")
        sys.exit(1)

    if output_path is None:
        output_path = str(inp.with_suffix(".docx"))

    md_text = inp.read_text(encoding="utf-8")
    sections = parse_markdown(md_text)

    builder = ResumeDocBuilder(theme=theme)
    builder.build_from_sections(sections)
    builder.save(output_path)

    print(f"Converted: {inp.name} -> {Path(output_path).name} (theme: {theme})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown resume to DOCX")
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("output", nargs="?", help="Output DOCX file (optional)")
    parser.add_argument("--theme", choices=["classic", "modern"], default="classic",
                        help="Visual theme (default: classic)")
    args = parser.parse_args()
    convert(args.input, args.output, args.theme)
