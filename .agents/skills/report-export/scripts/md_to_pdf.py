"""
Local Markdown to PDF Converter for AI Business Auditor.
Attempts conversion via Pandoc first; if Pandoc is not installed, falls back
to Python ReportLab (zero cloud egress, pure local rendering).
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def convert_with_pandoc(md_path: str, pdf_path: str) -> bool:
    pandoc_bin = shutil.which("pandoc")
    if not pandoc_bin:
        return False
    try:
        cmd = [
            pandoc_bin,
            md_path,
            "-o", pdf_path,
            "--pdf-engine=weasyprint",
            "--toc"
        ]
        # Try default engine if weasyprint not present
        res = subprocess.run([pandoc_bin, md_path, "-o", pdf_path], capture_output=True, text=True)
        return res.returncode == 0
    except Exception:
        return False

def convert_with_reportlab(md_path: str, pdf_path: str):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Corporate Palette (Navy & Cool Slate)
    primary_color = colors.HexColor("#0f172a")
    accent_color = colors.HexColor("#2563eb")
    text_color = colors.HexColor("#334155")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=accent_color,
        spaceBefore=16,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=text_color,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        leftIndent=14,
        spaceAfter=4
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=text_color
    )

    table_hdr_style = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    def format_md_line(text):
        import re
        # Escape XML entities first
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # Convert Markdown formatting into safe ReportLab tags
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'(\b|\s)\*(.*?)\*(\b|\s)', r'\1<i>\2</i>\3', text)
        text = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text)
        return text

    story = []
    in_table = False
    table_data = []

    for raw_line in lines:
        line = raw_line.strip()

        # Handle Markdown Tables
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            # Skip markdown separator row |---|---|
            if all(set(c).issubset({'-', ':', ' '}) for c in cells):
                continue
            if not in_table:
                in_table = True
                table_data = []
            
            # Format row
            is_header = (len(table_data) == 0)
            row_flowables = [
                Paragraph(format_md_line(c), table_hdr_style if is_header else table_cell_style)
                for c in cells
            ]
            table_data.append(row_flowables)
            continue
        elif in_table:
            # Table ended
            in_table = False
            if table_data:
                col_width = (letter[0] - 108) / len(table_data[0])
                t = Table(table_data, colWidths=[col_width] * len(table_data[0]))
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), accent_color),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ]))
                story.append(t)
                story.append(Spacer(1, 10))

        if not line:
            story.append(Spacer(1, 4))
            continue

        if line.startswith("# "):
            story.append(Paragraph(format_md_line(line[2:]), title_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceAfter=10))
        elif line.startswith("## "):
            story.append(Paragraph(format_md_line(line[3:]), h1_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=6))
        elif line.startswith("### "):
            story.append(Paragraph(format_md_line(line[4:]), h2_style))
        elif line.startswith("- ") or line.startswith("* "):
            story.append(Paragraph(f"• {format_md_line(line[2:])}", bullet_style))
        elif line.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceBefore=8, spaceAfter=8))
        else:
            story.append(Paragraph(format_md_line(line), body_style))

    # Catch trailing table
    if in_table and table_data:
        col_width = (letter[0] - 108) / len(table_data[0])
        t = Table(table_data, colWidths=[col_width] * len(table_data[0]))
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ]))
        story.append(t)

    doc.build(story)

def main():
    if len(sys.argv) < 2:
        print("Usage: python md_to_pdf.py <input.md> [output.pdf]")
        sys.exit(1)

    md_path = sys.argv[1]
    if len(sys.argv) >= 3:
        pdf_path = sys.argv[2]
    else:
        pdf_path = str(Path(md_path).with_suffix(".pdf"))

    if not os.path.exists(md_path):
        print(f"Error: Markdown file not found: {md_path}")
        sys.exit(1)

    # 1. Attempt Executive Chromium/Edge Playwright Engine (McKinsey Standard)
    try:
        workspace_root = str(Path(__file__).resolve().parents[4])
        if workspace_root not in sys.path:
            sys.path.insert(0, workspace_root)
        from render_executive_pdf import parse_markdown_to_html, render_pdf
        import asyncio
        print("Rendering via Executive Playwright/Edge Engine (McKinsey Standard)...")
        html = parse_markdown_to_html(md_path)
        asyncio.run(render_pdf(html, pdf_path))
        print(f"Rendered Executive PDF via Chromium/Edge: {pdf_path}")
        return
    except Exception as e:
        print(f"Executive engine fallback due to: {e}")

    # 2. Attempt Pandoc
    if convert_with_pandoc(md_path, pdf_path):
        print(f"Rendered PDF via Pandoc: {pdf_path}")
        return

    # 3. Local Fallback (ReportLab)
    print("Pandoc binary not detected; rendering via local ReportLab engine...")
    convert_with_reportlab(md_path, pdf_path)
    print(f"Rendered PDF via ReportLab: {pdf_path}")

if __name__ == "__main__":
    main()
