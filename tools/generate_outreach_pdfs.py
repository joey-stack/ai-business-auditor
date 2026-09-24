"""
Generates individual, beautifully formatted PDFs for each audited business's
customized outreach copy.
"""

import re
import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header rule & text
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, letter[1] - 40, letter[0] - 54, letter[1] - 40)
        self.drawString(54, letter[1] - 34, "AI Business Auditor — Legal Outreach & Prospect Intelligence")
        
        # Footer rule & text
        self.line(54, 45, letter[0] - 54, 45)
        self.drawString(54, 32, "Confidential B2B Strategy Document — CAN-SPAM, GDPR & TCPA Compliant")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_text)
        self.restoreState()

def format_xml(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(\b|\s)\*(.*?)\*(\b|\s)', r'\1<i>\2</i>\3', text)
    text = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', text)
    return text

def parse_businesses(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern to find each business section
    pattern = r'## (\d+)\.\s+([^\n]+)\n(.*?)(?=\n## \d+\.|\Z)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    businesses = []
    for num, title, body in matches:
        title_clean = title.replace("®", "").strip()
        slug = re.sub(r'[^a-z0-9]+', '_', title_clean.lower()).strip('_')
        businesses.append({
            "number": num,
            "title": title.strip(),
            "clean_title": title_clean,
            "slug": slug,
            "body": body.strip()
        })
    return businesses

def render_business_pdf(biz, output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    primary = colors.HexColor("#0f172a")     # Slate 900
    accent = colors.HexColor("#1d4ed8")      # Blue 700
    sub_accent = colors.HexColor("#0369a1")  # Sky 700
    text_dark = colors.HexColor("#1e293b")   # Slate 800
    bg_box = colors.HexColor("#f8fafc")      # Slate 50
    border_color = colors.HexColor("#cbd5e1")# Slate 300

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=sub_accent,
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=accent,
        spaceBefore=12,
        spaceAfter=6
    )

    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark
    )

    script_style = ParagraphStyle(
        'ScriptText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#0f172a")
    )

    email_body_style = ParagraphStyle(
        'EmailBodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=5
    )

    footer_style = ParagraphStyle(
        'FooterText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#475569")
    )

    story = []
    
    # Title Banner
    story.append(Paragraph(f"Customized Outreach: {format_xml(biz['title'])}", title_style))
    story.append(Paragraph("Diagnostic Intelligence & Legally Compliant Prospect Communication Blueprint", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent, spaceAfter=10))

    lines = biz['body'].split('\n')
    i = 0
    in_code = False
    code_lines = []

    # Extract metadata items (- **Key**: Value)
    meta_rows = []
    remaining_lines = []
    
    parsing_meta = True
    for line in lines:
        stripped = line.strip()
        if parsing_meta and stripped.startswith("- **") and ":" in stripped:
            match = re.match(r'-\s+\*\*([^*]+)\*\*:\s*(.*)', stripped)
            if match:
                k, v = match.groups()
                k_p = Paragraph(f"<b>{format_xml(k)}</b>", meta_style)
                v_p = Paragraph(format_xml(v), meta_style)
                meta_rows.append([k_p, v_p])
                continue
        elif parsing_meta and not stripped:
            continue
        else:
            parsing_meta = False
            remaining_lines.append(line)

    # Render Metadata Table
    if meta_rows:
        col_w1 = 130
        col_w2 = (letter[0] - 108) - col_w1
        t_meta = Table(meta_rows, colWidths=[col_w1, col_w2])
        t_meta.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_box),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(t_meta)
        story.append(Spacer(1, 10))

    # Process remaining content
    idx = 0
    while idx < len(remaining_lines):
        line = remaining_lines[idx].strip()

        if line.startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                # Format code block as an email draft box
                email_flowables = []
                # Separate main body from footer if --- is present
                full_text = "\n".join(code_lines)
                parts = full_text.split("\n---\n")
                
                body_part = parts[0]
                footer_part = parts[1] if len(parts) > 1 else ""

                for b_line in body_part.split("\n"):
                    b_str = b_line.strip()
                    if not b_str:
                        email_flowables.append(Spacer(1, 3))
                    elif re.match(r'^\d+\.\s+', b_str):
                        email_flowables.append(Paragraph(f"&nbsp;&nbsp;•&nbsp;{format_xml(b_str)}", email_body_style))
                    else:
                        email_flowables.append(Paragraph(format_xml(b_str), email_body_style))

                if footer_part:
                    email_flowables.append(Spacer(1, 4))
                    email_flowables.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#94a3b8"), spaceBefore=2, spaceAfter=4))
                    for f_line in footer_part.split("\n"):
                        f_str = f_line.strip()
                        if f_str and not f_str.startswith("---"):
                            email_flowables.append(Paragraph(format_xml(f_str), footer_style))

                t_email = Table([[email_flowables]], colWidths=[letter[0] - 108])
                t_email.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#94a3b8")),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ]))
                story.append(t_email)
                story.append(Spacer(1, 8))
            idx += 1
            continue

        if in_code:
            code_lines.append(remaining_lines[idx])
            idx += 1
            continue

        if line.startswith("### "):
            story.append(Paragraph(format_xml(line[4:]), h2_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=accent, spaceBefore=1, spaceAfter=6))
        elif line.startswith("> "):
            # Call script or quote block
            quote_text = []
            while idx < len(remaining_lines) and (remaining_lines[idx].strip().startswith("> ") or not remaining_lines[idx].strip()):
                if remaining_lines[idx].strip().startswith("> "):
                    quote_text.append(remaining_lines[idx].strip()[2:])
                idx += 1
            
            script_flowables = [
                Paragraph(format_xml(q), script_style) for q in quote_text if q
            ]
            t_script = Table([[script_flowables]], colWidths=[letter[0] - 108])
            t_script.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eff6ff")), # Alice blue
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#3b82f6")),     # Blue border
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(t_script)
            story.append(Spacer(1, 8))
            continue
        elif line.startswith("**Subject**:") or line.startswith("**To**:"):
            story.append(Paragraph(format_xml(line), meta_style))
            story.append(Spacer(1, 2))
        elif line.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceBefore=6, spaceAfter=6))
        elif line:
            story.append(Paragraph(format_xml(line), meta_style))
            story.append(Spacer(1, 3))

        idx += 1

    doc.build(story, canvasmaker=NumberedCanvas)

def main():
    md_path = "outputs/customized_outreach_copy.md"
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found.")
        return

    businesses = parse_businesses(md_path)
    print(f"Found {len(businesses)} businesses in {md_path}:")

    outputs_dir = Path("outputs")
    generated_files = []

    for biz in businesses:
        slug = biz['slug']
        out_md_path = outputs_dir / f"{slug}_outreach.md"
        out_pdf_path = outputs_dir / f"{slug}_outreach.pdf"

        # 1. Write individual Markdown file
        md_content = f"# Customized Outreach: {biz['title']}\n\n{biz['body']}\n"
        with open(out_md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # 2. Render individual PDF
        render_business_pdf(biz, str(out_pdf_path))
        print(f"[OK] Generated: {out_pdf_path.name} ({out_pdf_path.stat().st_size} bytes)")
        generated_files.append((biz['title'], str(out_md_path), str(out_pdf_path)))

    print("\nAll 7 outreach PDFs successfully generated!")

if __name__ == "__main__":
    main()
