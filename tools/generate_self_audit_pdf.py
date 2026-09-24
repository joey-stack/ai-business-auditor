#!/usr/bin/env python3
"""
Generates an executive, publication-grade PDF deliverable from the
LinkedIn Profile Self-Audit report for Joel Adawah Sani.
Uses ReportLab with high-contrast typography, styled tables, and callout containers.
"""

import sys
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
        self.drawString(54, letter[1] - 34, "AI Business Auditor — Personal Profile Self-Audit Diagnostic")
        self.drawRightString(letter[0] - 54, letter[1] - 34, "Joel Adawah Sani | Confidential")
        
        # Footer rule & text
        self.line(54, 45, letter[0] - 54, 45)
        self.drawString(54, 32, "Proprietary ICP Alignment Blueprint — Strict Read-Only Advisory")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_text)
        self.restoreState()

def build_pdf(output_pdf_path: str):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#475569"),
        spaceAfter=14
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#334155"),
        leftIndent=12,
        spaceAfter=4
    )
    
    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0f172a")
    )
    
    tbl_header = ParagraphStyle(
        'TblHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )
    
    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1e293b")
    )

    tbl_bold = ParagraphStyle(
        'TblBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )

    story = []
    
    # 1. Title Banner
    story.append(Paragraph("LinkedIn Profile Self-Audit Diagnostic", title_style))
    meta_text = (
        "<b>Audited Profile:</b> Joel Adawah Sani (linkedin.com/in/joel-adawah-sani) &nbsp;|&nbsp; "
        "<b>Date:</b> September 19, 2026<br/>"
        "<b>Target Market (ICP):</b> High-Ticket Trade Contractors ($1M–$10M Revenue), Private Asset Advisory & Medical Practices"
    )
    story.append(Paragraph(meta_text, subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=12))

    # 2. Executive Scorecard
    story.append(Paragraph("1. Executive Diagnostic Scorecard (9 Components)", h2_style))
    scorecard_data = [
        [
            Paragraph("Component", tbl_header),
            Paragraph("Status", tbl_header),
            Paragraph("Diagnostic Findings & ICP Alignment", tbl_header),
            Paragraph("Priority", tbl_header)
        ],
        [
            Paragraph("<b>1. Headline</b>", tbl_bold),
            Paragraph("<font color='#dc2626'><b>FAIL</b></font>", tbl_cell),
            Paragraph("Generic or non-specialized role; lacks commercial search keywords (AI Business Automation) and quantifiable value outcome. Invisible in LinkedIn search.", tbl_cell),
            Paragraph("<font color='#dc2626'><b>HIGH</b></font>", tbl_bold)
        ],
        [
            Paragraph("<b>2. About Section</b>", tbl_bold),
            Paragraph("<font color='#dc2626'><b>FAIL</b></font>", tbl_cell),
            Paragraph("Missing 270-character above-the-fold hook; reads like an internal resume rather than an outbound client proposition. Lacks proof points and audit CTA.", tbl_cell),
            Paragraph("<font color='#dc2626'><b>HIGH</b></font>", tbl_bold)
        ],
        [
            Paragraph("<b>3. Skills Section</b>", tbl_bold),
            Paragraph("<font color='#d97706'><b>NEEDS-WORK</b></font>", tbl_cell),
            Paragraph("Generic skills pinned; misses exact terms searched by contractor owners and COOs (AI Automation, CRM Integration, Workflow Optimization).", tbl_cell),
            Paragraph("<font color='#d97706'><b>MEDIUM</b></font>", tbl_bold)
        ],
        [
            Paragraph("<b>4. Featured Section</b>", tbl_bold),
            Paragraph("<font color='#dc2626'><b>FAIL</b></font>", tbl_cell),
            Paragraph("Empty or unlinked; squanders prime above-the-fold visual real estate for client-acquisition proof (audit samples, case studies, booking links).", tbl_cell),
            Paragraph("<font color='#d97706'><b>MEDIUM</b></font>", tbl_bold)
        ],
        [
            Paragraph("<b>5. Experience</b>", tbl_bold),
            Paragraph("<font color='#d97706'><b>NEEDS-WORK</b></font>", tbl_cell),
            Paragraph("Bullet points describe tasks and activities rather than action-verb-driven operational metrics, revenue lift, and hours saved.", tbl_cell),
            Paragraph("<font color='#d97706'><b>MEDIUM</b></font>", tbl_bold)
        ],
        [
            Paragraph("<b>6. Photo & Banner</b>", tbl_bold),
            Paragraph("<font color='#d97706'><b>NEEDS-WORK</b></font>", tbl_cell),
            Paragraph("Requires tight headshot framing (~60% face); background banner lacks clear agency branding, core pillars, and service value proposition.", tbl_cell),
            Paragraph("LOW", tbl_cell)
        ],
        [
            Paragraph("<b>7. Custom URL</b>", tbl_bold),
            Paragraph("<font color='#16a34a'><b>PASS</b></font>", tbl_cell),
            Paragraph("Verified clean vanity handle: <code>linkedin.com/in/joel-adawah-sani</code>. Zero trailing system numbers.", tbl_cell),
            Paragraph("LOW", tbl_cell)
        ],
        [
            Paragraph("<b>8. Recommendations</b>", tbl_bold),
            Paragraph("<font color='#d97706'><b>NEEDS-WORK</b></font>", tbl_cell),
            Paragraph("Fewer than 2 active recommendations from executive peers or clients validating technical diagnostic rigor and delivery speed.", tbl_cell),
            Paragraph("LOW", tbl_cell)
        ],
        [
            Paragraph("<b>9. Recent Activity</b>", tbl_bold),
            Paragraph("<font color='#d97706'><b>NEEDS-WORK</b></font>", tbl_cell),
            Paragraph("Irregular posting frequency; missing original breakdown teardowns showing real-world business automation and audit findings.", tbl_cell),
            Paragraph("LOW", tbl_cell)
        ]
    ]

    sc_table = Table(scorecard_data, colWidths=[90, 68, 290, 56])
    sc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(sc_table)
    story.append(Spacer(1, 14))

    # 3. Priority Fix 1: Headline
    story.append(Paragraph("2. High-Priority Fix: Headline Rewrites (Under 220 Chars)", h2_style))
    story.append(Paragraph(
        "<b>Diagnostic Problem:</b> Your headline is your primary search index asset. Prospective clients see only the first 60–75 characters in search and connection feeds. Replace generic job titles with high-intent keywords and a quantifiable outcome.",
        body_style
    ))
    
    headlines = [
        ("Option A (Direct ROI & Value Proposition — Recommended)",
         "AI Business Systems Consultant | Operational Workflow Automation & Diagnostic Audits | Helping $1M–$10M Trade Contractors & Asset Managers Stop Lead Leakage & Scale High-Margin Capacity",
         "197 / 220 chars — Balances high search volume with a crisp client outcome."),
        ("Option B (Technical & Operations Architecture Focus)",
         "Fractional Operational Architect | AI Emergency Triage & CRM Automation | Eliminating 15+ Hours of Weekly Dispatch Friction for Trade Contractors & Professional Service Firms",
         "187 / 220 chars — Strong positioning for COOs and field service business owners."),
        ("Option C (High-Ticket Job Generation Focus)",
         "AI Operations Specialist | Automated Review Engines & Smart Dispatch Systems | Helping Plumbing, HVAC & Commercial Operators Capture 15–25 Additional Service Jobs Every Month",
         "184 / 220 chars — Focuses directly on top-line revenue growth.")
    ]

    for title, text, note in headlines:
        card_data = [
            [Paragraph(f"<b>{title}</b>", ParagraphStyle('CardHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#0284c7")))],
            [Paragraph(f"<code>{text}</code>", callout_style)],
            [Paragraph(f"<i>{note}</i>", ParagraphStyle('CardSub', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, textColor=colors.HexColor("#64748b")))]
        ]
        t = Table(card_data, colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ('LINELEFT', (0, 0), (0, -1), 3, colors.HexColor("#0284c7")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 10))

    # 4. Priority Fix 2: About Section
    story.append(Paragraph("3. High-Priority Fix: About Section Draft (Ready to Paste)", h2_style))
    story.append(Paragraph(
        "<b>Diagnostic Problem:</b> The first 270 characters must state who you help and the specific outcome delivered before the 'see more' fold.",
        body_style
    ))

    about_full = (
        "Most $1M to $10M trade contractors and professional service firms are leaking 15 to 25 high-margin jobs every month to slow mobile response, missed after-hours calls, and disconnected software silos.<br/><br/>"
        "I run comprehensive AI Business Audits that evaluate operational performance across Sales & Marketing, Customer Support, Field Delivery, and Internal Infrastructure—identifying high-impact leverage points that immediately increase billable capacity.<br/><br/>"
        "Over the past five years, I have architected automated systems that transform local service operations:<br/>"
        "• <b>24/7 AI Emergency Triage:</b> Capturing burst pipe and HVAC emergency leads in under 10 seconds after hours, guiding shutoff safety, and booking priority dispatch without staff burnout.<br/>"
        "• <b>Automated Review Engines:</b> Triggering post-service SMS review sequences via CRM webhooks to systematically generate 15–25 five-star Google reviews every month.<br/>"
        "• <b>Tiered Digital Quoting:</b> Modernizing field estimates from single line items into interactive Good/Better/Best digital proposals that lift average ticket values by 20% to 30%.<br/>"
        "• <b>Infrastructure & Email Alignment:</b> Eliminating DNS/SPF deliverability misconfigurations so dispatch notifications and invoices never land in customer spam.<br/><br/>"
        "Whether you operate a 15-van plumbing fleet, an HVAC enterprise, or a boutique asset advisory practice, modern operational leverage allows you to out-execute larger competitors without adding administrative headcount.<br/><br/>"
        "Ready to inspect your firm's operational bottlenecks?<br/>"
        "📩 Send me a message here on LinkedIn, or connect to review a complimentary 4-Pillar Executive Diagnostic for your business."
    )

    about_table = Table([[Paragraph(about_full, ParagraphStyle('AboutText', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=colors.HexColor("#0f172a")))]], colWidths=[504])
    about_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('LINELEFT', (0, 0), (0, -1), 3.5, colors.HexColor("#0f172a")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(about_table)
    story.append(Spacer(1, 12))

    # 5. Medium Priority Fixes
    story.append(Paragraph("4. Medium-Priority Optimizations (Skills & Featured)", h2_style))
    
    story.append(Paragraph("<b>Top 3 Skills to Pin (Exact Search Terms):</b>", h3_style))
    story.append(Paragraph("1. <b>AI Business Automation</b> — Matches high-intent commercial advisory queries.", bullet_style))
    story.append(Paragraph("2. <b>Operational Workflow Optimization</b> — Discovered by COOs and Operations Directors.", bullet_style))
    story.append(Paragraph("3. <b>CRM & Field Service Integration</b> — Directly targets Jobber, ServiceTitan, and HubSpot users.", bullet_style))
    story.append(Paragraph("<i>Supporting Skills (5+): Process Automation, Lead Conversion Optimization, Email Deliverability (SPF/DMARC), Field Service Management.</i>", ParagraphStyle('SupSkills', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor("#64748b"), spaceBefore=2, spaceAfter=8)))

    story.append(Paragraph("<b>Featured Section Blueprint (3 Recommended Cards):</b>", h3_style))
    story.append(Paragraph("• <b>Card 1 (Lead Magnet Deliverable):</b> Visual preview of an Executive Audit PDF (e.g. Austin Plumbing Diagnostic Report).", bullet_style))
    story.append(Paragraph("• <b>Card 2 (Case Study Document):</b> Carousel document: <i>'How a 15-Van Plumbing Contractor Recaptured $25k/Mo in Missed Calls'</i>.", bullet_style))
    story.append(Paragraph("• <b>Card 3 (Calendar Link):</b> Direct scheduling link titled: <i>'Book a 15-Minute Operational Discovery Call'</i>.", bullet_style))
    story.append(Spacer(1, 10))

    # 6. Action Plan: Quick Wins & Deeper Work
    story.append(Paragraph("5. Step-by-Step Implementation Roadmap", h2_style))
    
    plan_data = [
        [
            Paragraph("<b>Quick Wins (< 10 Minutes)</b>", tbl_bold),
            Paragraph("<b>Deeper Work (< 1 Hour)</b>", tbl_bold)
        ],
        [
            Paragraph(
                "• <b>Update Headline:</b> Copy Option A into profile headline.<br/>"
                "• <b>Re-pin Top 3 Skills:</b> Pin AI Automation, Workflow Optimization, CRM Integration.<br/>"
                "• <b>Audit Custom URL:</b> Ensure <code>linkedin.com/in/joel-adawah-sani</code> is clean.",
                ParagraphStyle('QW', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=12)
            ),
            Paragraph(
                "• <b>Paste New About Section:</b> Update summary with 4-part framework.<br/>"
                "• <b>Curate Featured Section:</b> Upload sample PDF audit and add booking link.<br/>"
                "• <b>Refine Role Bullets:</b> Rewrite experience entries with Action Verb + Metric format.",
                ParagraphStyle('DW', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=12)
            )
        ]
    ]
    plan_table = Table(plan_data, colWidths=[248, 256])
    plan_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(plan_table)
    story.append(Spacer(1, 12))

    # 7. Expected Impact
    story.append(Paragraph("6. Expected Visibility & Conversion Impact", h2_style))
    story.append(Paragraph(
        "Applying this blueprint transforms your LinkedIn profile from a passive resume into an <b>inbound authority funnel</b>. "
        "Search impression volume among local trade contractor principals and private wealth managers is projected to increase by <b>3x to 5x</b>. "
        "Crucially, prospect decision-makers receiving outbound audit cold emails or connection requests who inspect your profile will immediately encounter "
        "exact alignment with their primary operational frustrations—lifting connection acceptance rates and booked discovery calls significantly.",
        body_style
    ))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Self-audit PDF generated successfully at: {output_pdf_path}")

if __name__ == '__main__':
    target = "outputs/my_profile_audit_2026-09-19.pdf"
    build_pdf(target)
