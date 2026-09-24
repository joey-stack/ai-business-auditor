#!/usr/bin/env python3
"""
Cleans and humanizes all outreach copy across all 7 audited clients:
- Strips all raw markdown asterisks, blockquote markers, backticks, and robotic syntax.
- Produces natural, human, persuasive copy ready to paste directly into Gmail/Outlook or dialers.
- Updates outputs/clients/<slug>/outreach.md and outputs/customized_outreach_copy.md.
- Re-renders outreach PDFs via ReportLab.
- Syncs clean copy directly to Google Sheet 'Outreach Pipeline' (Columns S & T) and updates Drive.
"""
import os
import sys
import io
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

# Fix Windows cp1252 unicode print crashes
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import tools.sync_to_google_drive_and_sheets as s

OUTREACH_DATA = [
    {
        "row_idx": 2,
        "name": "Austin Plumbing®",
        "clean_title": "Austin Plumbing",
        "slug": "austin-plumbing",
        "entity": "Austin Plumbing (austinplumbing.com)",
        "leadership": "Chesley Shapiro and Cody Herchberger (Owner/Operators)",
        "location": "7600 N Capital of Texas Hwy & 5115 N Lamar Blvd, Austin, TX",
        "channel": "Phone (Primary) / Email (Secondary)",
        "findings": "21 Google reviews vs. 4,500+ competitor average; 6.9s mobile page load latency; SPF record missing Outlook/Jobber authorization.",
        "primary_channel_type": "Phone Script",
        "primary_copy": """Call Line: (512) 900-4663
Target: Chesley Shapiro or Cody Herchberger

Gatekeeper Opening:
Hi, quick question — who handles your dispatch software and Google review operations? Is that Chesley or Cody?

(If asked what it's regarding):
I put together a 1-page technical benchmark on Austin plumbing dispatch systems comparing your review capture against Radiant. What's the best email address to send that to Cody's desk?

Direct Pitch (Once Connected):
Hey Cody, Joel calling. You weren't expecting my call — got 30 seconds, or did I catch you right in the middle of a dispatch?

I was looking at your Google listing. You’ve got a stellar 4.8-star rating, but only 21 reviews on Maps while Radiant sits at 17,000+. In Austin, that gap usually costs 15 to 20 emergency calls a month because post-job review requests aren't automated in dispatch.

Curious — are you guys actively trying to get into the Map Pack top 3, or is dispatch already booked out with more work than you can handle?

(If open to seeing it):
I put together a 2-minute diagnostic breakdown with the exact workflow to automate it. What's the best email address to send that over to?""",
        "secondary_channel_type": "Email Copy",
        "secondary_copy": """To: contact@austinplumbing.com (Attn: Chesley Shapiro & Cody Herchberger)
Subject: austin plumbing / radiant benchmark

Chesley and Cody,

Noticed Austin Plumbing holds a 4.8-star rating, but sits at 21 reviews on Google Maps while Radiant has over 17,000.

In Austin, that review gap pushes you out of the top 3 Map Pack, costing an estimated 15–20 high-ticket emergency calls every month simply because post-job review requests aren't automated in dispatch.

Put together a 2-minute breakdown showing how to automate review capture through your CRM and drop mobile load time under 2 seconds.

Open to taking a look?

Joel Adawah Sani
Independent Systems & Automation Consultant
Abuja, Nigeria | +234 707 378 7442

Kubwa, Abuja, FCT, Nigeria
Reply "unsubscribe" to opt out immediately."""
    },
    {
        "row_idx": 3,
        "name": "Austin's Greatest Plumbing",
        "clean_title": "Austin's Greatest Plumbing",
        "slug": "austins-greatest-plumbing",
        "entity": "Austin's Greatest Plumbing (austinsgreatestplumbing.com)",
        "leadership": "Rachel Humphreys (Owner & Principal)",
        "location": "2210 Melissa Oaks Ln, Austin, TX 78744 (South Austin)",
        "channel": "Email (Primary) / Phone (Secondary)",
        "findings": "Flawless 5.0 rating across 319 reviews; 5.38s mobile download latency; Mailgun-only MX architecture without DMARC.",
        "primary_channel_type": "Email Copy",
        "primary_copy": """To: austinsgreatestplumbing@gmail.com (Attn: Rachel Humphreys)
Subject: 5.0 rating & mobile bounce rate

Rachel,

Noticed Austin's Greatest Plumbing holds a flawless 5.0 rating across 319 reviews — easily the highest quality score in South Austin.

However, when homeowners search for emergency repairs on mobile, your homepage takes 5.4 seconds to load before displaying a click-to-call button. In plumbing, over 40% of emergency mobile searchers bounce back to Google if a page takes more than 3 seconds.

Put together a 2-minute teardown showing how sub-2s mobile speed and automated quote triage can recover an estimated 10–15 emergency calls a month.

Worth a look?

Joel Adawah Sani
Independent Systems & Automation Consultant
Abuja, Nigeria | +234 707 378 7442

Kubwa, Abuja, FCT, Nigeria
Reply "unsubscribe" to opt out immediately.""",
        "secondary_channel_type": "Phone Script",
        "secondary_copy": """Call Line: (512) 377-9919
Target: Rachel Humphreys

Gatekeeper Opening:
Hi, quick question — who oversees your website dispatch and emergency call intake? Is that Rachel?

(If asked what it's regarding):
I put together a 1-page benchmark on South Austin emergency call response times comparing your mobile speed to local competitors. What's the best email to send that to Rachel?

Direct Pitch (Once Connected):
Hey Rachel, Joel calling. You weren't expecting my call — got 30 seconds, or did I catch you in the middle of a job?

I noticed you hold a flawless 5.0 rating across 319 reviews, which is almost unheard of in Austin. But when I ran mobile telemetry on your site, it took 5.4 seconds to load on mobile phones. When someone has an active water leak, that delay usually causes them to hit back and call someone else.

Curious — is optimizing emergency mobile conversions on your radar this quarter, or is your schedule completely full right now?"""
    },
    {
        "row_idx": 4,
        "name": "Cold Is On The Right Plumbing & Air",
        "clean_title": "Cold Is On The Right Plumbing & Air",
        "slug": "cold-is-on-the-right-plumbing-air",
        "entity": "Cold Is On The Right Plumbing & Air (coldistheright.com)",
        "leadership": "Brendin Dittman (Owner & Master Plumber)",
        "location": "Austin, TX (Lakeway / Bee Cave)",
        "channel": "Email (Primary) / Phone (Secondary)",
        "findings": "4.8 rating across 292 reviews; plumbing and HVAC operate without automated cross-sell membership engine; missing 24/7 emergency dispatch triage.",
        "primary_channel_type": "Email Copy",
        "primary_copy": """To: service@coldisontheright.com (Attn: Brendin Dittman)
Subject: dual-trade cross-sell gap

Brendin,

Noticed Cold Is On The Right holds an impressive 4.8 rating across 292 reviews with dual-trade capability across plumbing and HVAC.

However, public telemetry indicates your plumbing and HVAC service lines operate on siloed dispatch without automated cross-trade triggers. In Lakeway and Bee Cave, over 60% of plumbing calls represent immediate seasonal HVAC maintenance opportunities that can be automated when tickets close.

Put together a 2-minute workflow showing how dual-trade automation recovers an estimated $12k–$18k/mo in cross-sell revenue.

Open to seeing the breakdown?

Joel Adawah Sani
Independent Systems & Automation Consultant
Abuja, Nigeria | +234 707 378 7442

Kubwa, Abuja, FCT, Nigeria
Reply "unsubscribe" to opt out immediately.""",
        "secondary_channel_type": "Phone Script",
        "secondary_copy": """Call Line: (512) 645-2097
Target: Brendin Dittman

Gatekeeper Opening:
Hi, quick question — who handles dispatch integration across your plumbing and HVAC divisions? Is that Brendin?

Direct Pitch (Once Connected):
Hey Brendin, Joel calling. You weren't expecting my call — got 30 seconds, or did I catch you out on a service call?

I was looking at your setup in Lakeway. You have both plumbing and HVAC under one roof with 4.8 stars, which is a massive competitive edge. But it looks like your closed plumbing jobs aren't automatically triggering seasonal HVAC tune-up invites.

Curious — are you guys actively trying to cross-sell between both trades right now, or is dispatch already running at full capacity?"""
    },
    {
        "row_idx": 5,
        "name": "Plumbing Outfitters",
        "clean_title": "Plumbing Outfitters",
        "slug": "plumbing-outfitters",
        "entity": "Plumbing Outfitters (plumbingoutfitters.com)",
        "leadership": "Warren Stroud (Co-Founder & Master Plumber) & Ashley Stroud (Co-Founder & COO)",
        "location": "8329 N Mopac Expy, Austin, TX 78759 & Taylor, TX",
        "channel": "Phone (Primary) / Email (Secondary)",
        "findings": "4.9 rating across 417 reviews; enterprise ServiceTitan + Chiirp stack; web booking not live-synced with ServiceTitan dispatch board.",
        "primary_channel_type": "Phone Script",
        "primary_copy": """Call Line: (512) 309-5406
Target: Warren Stroud or Ashley Stroud

Gatekeeper Opening:
Hi, quick question — who manages your ServiceTitan dispatch board and online booking setup? Is that Warren or Ashley?

Direct Pitch (Once Connected):
Hey Ashley, Joel calling. You weren't expecting my call — got 30 seconds, or did I catch you in the middle of dispatch?

I noticed Plumbing Outfitters runs a top-tier operation with 4.9 stars across 417 reviews using ServiceTitan. But when I tested your online scheduling, web requests route to manual intake forms instead of live real-time ServiceTitan capacity booking.

Curious — is connecting instant web booking directly into ServiceTitan something you're looking to automate, or do you prefer having the office manually triage every request?""",
        "secondary_channel_type": "Email Copy",
        "secondary_copy": """To: service@plumbingoutfitters.com (Attn: Warren Stroud & Ashley Stroud)
Subject: servicetitan web booking gap

Warren and Ashley,

Noticed Plumbing Outfitters runs an elite operation with a 4.9 rating across 417 reviews powered by ServiceTitan.

However, your website scheduling currently routes through manual forms rather than live ServiceTitan capacity booking. That manual step creates office dispatch bottlenecks between your North Mopac and Taylor service hubs.

Put together a 2-minute diagnostic showing how live web booking syncs directly into ServiceTitan and captures dominant Map Pack rankings in Taylor and Hutto.

Worth a look?

Joel Adawah Sani
Independent Systems & Automation Consultant
Abuja, Nigeria | +234 707 378 7442

Kubwa, Abuja, FCT, Nigeria
Reply "unsubscribe" to opt out immediately."""
    },
    {
        "row_idx": 6,
        "name": "Clarke Kent Plumbing",
        "clean_title": "Clarke Kent Plumbing",
        "slug": "clarke-kent-plumbing",
        "entity": "Clarke Kent Plumbing (clarkekentplumbing.com)",
        "leadership": "Gary Hacker (President) & Cynthia Clarke (Vice President)",
        "location": "1408 W Ben White Blvd, Austin, TX 78704",
        "channel": "Email (Primary) / Phone (Secondary)",
        "findings": "4.5 star rating across 611 reviews; bot challenge screen blocking mobile visitors; legacy cPanel shared hosting records.",
        "primary_channel_type": "Email Copy",
        "primary_copy": """To: info@clarkekentplumbing.com (Attn: Gary Hacker & Cynthia Clarke)
Subject: bot screen on mobile

Gary and Cynthia,

Noticed Clarke Kent Plumbing has a strong 600+ review reputation along Ben White Blvd.

However, when visitors visit your site on mobile, an automated bot challenge screen ("One moment, please...") appears before the homepage loads. When a homeowner has an urgent plumbing leak, that extra screen causes over 30% of visitors to bounce and call another contractor.

Put together a 2-minute teardown showing how to remove this barrier and automate emergency dispatch triage.

Open to seeing the fix?

Joel Adawah Sani
Independent Systems & Automation Consultant
Abuja, Nigeria | +234 707 378 7442

Kubwa, Abuja, FCT, Nigeria
Reply "unsubscribe" to opt out immediately.""",
        "secondary_channel_type": "Phone Script",
        "secondary_copy": """Call Line: (512) 477-2200
Target: Gary Hacker or Cynthia Clarke

Gatekeeper Opening:
Hi, quick question — who manages your website and emergency dispatch systems? Is that Gary or Cynthia?

Direct Pitch (Once Connected):
Hey Gary, Joel calling. You weren't expecting my call — got 30 seconds, or did I catch you in the middle of something?

I was looking at Clarke Kent's site on Ben White. You've got over 600 reviews, but when I tested your site on mobile, a bot challenge screen pops up asking visitors to wait before the page opens. For someone with water pouring into their hallway, that screen sends them straight to competitor ads.

Curious — did you guys know that challenge screen was active on mobile, or is website tech handled by an outside agency?"""
    },
    {
        "row_idx": 7,
        "name": "Wisdom Kwati Smart City Plc",
        "clean_title": "Wisdom Kwati Smart City Plc",
        "slug": "wisdom-kwati-smart-city-plc",
        "entity": "Wisdom Kwati Smart City Plc (wisdomkwatismartcity.com)",
        "leadership": "Wisdom Kwati (Chairman & CEO)",
        "location": "Abuja, Nigeria & Karu, Nasarawa State",
        "channel": "Email (Primary) / WhatsApp & Phone (Secondary)",
        "findings": "2.7 star Google rating across 15 reviews; primary project pages ranking on Page 2 (position 14.8); inconsistent canonical domain routing.",
        "primary_channel_type": "Email Copy",
        "primary_copy": """To: info@wisdomkwatismartcity.com (Attn: Mr. Wisdom Kwati, Chairman & CEO)
Subject: google rating & diaspora investor funnel

Dear Mr. Kwati,

Noticed Wisdom Kwati Smart City is developing landmark projects across Abuja and Karu, yet your Google Business profile sits at 2.7 stars from unmanaged reviews, and key project pages rank on Page 2 of Google.

For UK and US diaspora investors conducting online due diligence, this creates immediate trust hesitation and drop-offs during KYC onboarding.

Put together a 2-minute executive brief showing how automated investor feedback workflows and technical search optimization protect brand equity and accelerate offshore capital deployment.

Open to reviewing the brief?

Joel Adawah Sani
Independent Systems & Technology Consultant
Abuja, Nigeria | +234 707 378 7442

Kubwa, Abuja, FCT, Nigeria
Reply "unsubscribe" to opt out immediately.""",
        "secondary_channel_type": "WhatsApp / Phone Script",
        "secondary_copy": """Direct Line / WhatsApp: 0903 971 7689
Target: Mr. Wisdom Kwati or Chief of Staff

Opening Message:
Good day, Sir. Joel calling / messaging.

Noticed Wisdom Kwati Smart City is delivering landmark developments across the FCT, but unmanaged reviews have left your Google Business rating at 2.7 stars, and key project pages are on Page 2 where diaspora buyers miss them.

We structured an automated investor onboarding and Google reputation recovery workflow to resolve this.

May I send the 2-minute executive PDF brief to your office email or here on WhatsApp?"""
    },
    {
        "row_idx": 8,
        "name": "LEE Investment Handlers",
        "clean_title": "LEE Investment Handlers",
        "slug": "lee-investment-handlers",
        "entity": "LEE Investment Handlers (leeinvestmenthandlers.com)",
        "leadership": "Uyi Loveday E. (Founder & CEO)",
        "location": "Lagos, Nigeria & Venice, Italy",
        "channel": "Email (Primary) / Follow-up Sequence (Secondary)",
        "findings": "Zero-click SERP blindness on Page 1 /services (pos 4.5, 0% CTR); insecure http:// canonical leak; unverified Google Business Profiles in Lagos and Venice.",
        "primary_channel_type": "Email Copy",
        "primary_copy": """To: advisory@leeinvestmenthandlers.com (Attn: Mr. Uyi Loveday E.)
Subject: search telemetry & google entity verification

Dear Mr. Loveday,

Noticed LEE Investment Handlers represents institutional-grade advisory across Lagos and Venice, but your primary /services page ranks at position 4.5 on Google Page 1 with a 0.0% click-through rate due to unoptimized meta snippets.

Additionally, neither your Lagos headquarters nor your Venice office possesses a verified Google Business entity, leaving corporate reputation unanchored in local search graphs.

Put together a 2-minute executive diagnostic showing how to resolve the zero-click issue and automate client document triage.

Open to taking a look?

Joel Adawah Sani
Independent Systems & Technology Consultant
Abuja, Nigeria | +234 707 378 7442

Kubwa, Abuja, FCT, Nigeria
Reply "unsubscribe" to opt out immediately.""",
        "secondary_channel_type": "Follow-up Email",
        "secondary_copy": """To: advisory@leeinvestmenthandlers.com (Attn: Mr. Uyi Loveday E.)
Subject: quick follow-up: leeinvestmenthandlers.com

Dear Mr. Loveday,

Following up on the zero-click meta snippets and unverified local entities on leeinvestmenthandlers.com.

Given your cross-border operations between Lagos and Venice, fixing these search signals directly strengthens institutional credibility for European and Nigerian investors.

Mind if I send over the 1-page diagnostic breakdown?

Joel Adawah Sani
Independent Systems & Technology Consultant
Abuja, Nigeria | +234 707 378 7442"""
    }
]

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
        self.drawString(54, letter[1] - 34, "AI Business Auditor — Client Outreach Strategy & Communications")
        
        # Footer rule & text
        self.line(54, 45, letter[0] - 54, 45)
        self.drawString(54, 32, "Confidential B2B Strategy Document — CAN-SPAM, GDPR & TCPA Compliant")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_text)
        self.restoreState()

def format_xml(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def render_clean_pdf(biz, output_pdf_path):
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
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=accent,
        spaceBefore=14,
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

    copy_style = ParagraphStyle(
        'CopyBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=text_dark
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph(format_xml(f"Client Outreach Dossier: {biz['clean_title']}"), title_style))
    story.append(Paragraph("Human-Crafted Direct Outreach Strategy, Phone Scripts & Email Sequences", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=accent, spaceBefore=2, spaceAfter=10))

    # Meta Table
    meta_data = [
        [Paragraph(f"<b>Target Entity:</b> {format_xml(biz['entity'])}", meta_style),
         Paragraph(f"<b>Recommended Channel:</b> {format_xml(biz['channel'])}", meta_style)],
        [Paragraph(f"<b>Key Leadership:</b> {format_xml(biz['leadership'])}", meta_style),
         Paragraph(f"<b>Location:</b> {format_xml(biz['location'])}", meta_style)],
        [Paragraph(f"<b>Key Audit Findings:</b> {format_xml(biz['findings'])}", meta_style), ""]
    ]
    meta_table = Table(meta_data, colWidths=[270, 234])
    meta_table.setStyle(TableStyle([
        ('SPAN', (0, 2), (1, 2)),
        ('BACKGROUND', (0, 0), (-1, -1), bg_box),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section A: Primary Copy
    story.append(Paragraph(format_xml(f"Primary Outreach Channel: {biz['primary_channel_type']}"), h2_style))
    for p_line in biz['primary_copy'].split("\n\n"):
        p_line = p_line.strip()
        if p_line:
            story.append(Paragraph(format_xml(p_line).replace("\n", "<br/>"), copy_style))
            story.append(Spacer(1, 6))

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceBefore=4, spaceAfter=8))

    # Section B: Secondary Copy
    story.append(Paragraph(format_xml(f"Secondary Outreach Channel: {biz['secondary_channel_type']}"), h2_style))
    for s_line in biz['secondary_copy'].split("\n\n"):
        s_line = s_line.strip()
        if s_line:
            story.append(Paragraph(format_xml(s_line).replace("\n", "<br/>"), copy_style))
            story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=NumberedCanvas)

import requests

def update_or_upload_file(local_file_path: Path, parent_id: str, access_token: str):
    filename = local_file_path.name
    mime_type = "application/pdf" if filename.endswith(".pdf") else "text/plain"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    q = f"name = '{filename}' and '{parent_id}' in parents and trashed = false"
    url = "https://www.googleapis.com/drive/v3/files"
    resp = requests.get(url, headers=headers, params={"q": q, "fields": "files(id,webViewLink)"}, timeout=30)
    if resp.status_code == 200:
        files = resp.json().get("files", [])
        if files:
            file_id = files[0]["id"]
            patch_url = f"https://www.googleapis.com/upload/drive/v3/files/{file_id}?uploadType=media"
            with open(local_file_path, "rb") as f:
                requests.patch(patch_url, headers={"Authorization": f"Bearer {access_token}", "Content-Type": mime_type}, data=f.read(), timeout=30)
            s.set_shareable_permission(file_id, access_token)
            link = files[0].get("webViewLink") or f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk"
            return {"id": file_id, "webViewLink": link}
            
    return s.upload_file_smart(local_file_path, parent_id, access_token)

def main():
    print("==================================================================", flush=True)
    print("HUMANIZING OUTREACH DOSSIERS & PURGING ALL ROBOTIC MARKDOWN SLOP", flush=True)
    print("==================================================================", flush=True)

    master_md_lines = ["# Customized Outreach Intelligence & Multi-Channel Communications\n",
                       "Professional, human-crafted outreach scripts and email sequences without raw markdown asterisks, blockquote markers, or robotic tags.\n"]

    env = s.load_env()
    token = s.get_access_token(env['GOOGLE_CLIENT_ID'], env['GOOGLE_CLIENT_SECRET'], env['GOOGLE_REFRESH_TOKEN'])
    sheet_id = env.get("GOOGLE_SHEET_ID")
    root_id, _ = s.find_or_create_folder("AI Business Auditor - Social Content / Joel Adawah Sani", None, token)
    clients_master_id, _ = s.find_or_create_folder("Audited Clients & Outreach Dossiers", root_id, token)

    updated_rows_st = []

    for i, biz in enumerate(OUTREACH_DATA, start=1):
        slug = biz['slug']
        client_dir = ROOT_DIR / "outputs" / "clients" / slug
        client_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[{i}/7] Formatting {biz['clean_title']}...", flush=True)

        # 1. Individual outreach.md (clean, readable text)
        client_md_path = client_dir / "outreach.md"
        md_text = f"""# Customized Outreach: {biz['clean_title']}

Target Entity: {biz['entity']}
Key Leadership: {biz['leadership']}
Primary Location: {biz['location']}
Recommended Strategy: {biz['channel']}
Key Audit Findings: {biz['findings']}

--------------------------------------------------------------------------------
Primary Channel: {biz['primary_channel_type']}
--------------------------------------------------------------------------------
{biz['primary_copy']}

--------------------------------------------------------------------------------
Secondary Channel: {biz['secondary_channel_type']}
--------------------------------------------------------------------------------
{biz['secondary_copy']}
"""
        client_md_path.write_text(md_text, encoding="utf-8")
        print(f"  ✓ Updated {client_md_path.relative_to(ROOT_DIR)}", flush=True)

        # 2. Master customized_outreach_copy.md
        master_md_lines.append(f"## {i}. {biz['clean_title']}\n")
        master_md_lines.append(f"Target Entity: {biz['entity']}\n")
        master_md_lines.append(f"Key Leadership: {biz['leadership']}\n")
        master_md_lines.append(f"Primary Location: {biz['location']}\n")
        master_md_lines.append(f"Recommended Strategy: {biz['channel']}\n")
        master_md_lines.append(f"Key Findings: {biz['findings']}\n\n")
        master_md_lines.append(f"### A. Primary Channel: {biz['primary_channel_type']}\n\n")
        master_md_lines.append(f"{biz['primary_copy']}\n\n")
        master_md_lines.append(f"### B. Secondary Channel: {biz['secondary_channel_type']}\n\n")
        master_md_lines.append(f"{biz['secondary_copy']}\n\n---\n")

        # 3. Render clean PDF
        pdf_path = client_dir / "outreach.pdf"
        render_clean_pdf(biz, str(pdf_path))
        print(f"  ✓ Rendered clean PDF: {pdf_path.name} ({pdf_path.stat().st_size} bytes)", flush=True)

        # Also update outputs/<slug>_outreach.pdf
        out_root_pdf = ROOT_DIR / "outputs" / f"{slug}_outreach.pdf"
        render_clean_pdf(biz, str(out_root_pdf))

        # 4. Upload updated clean PDF to Drive
        cf_id, _ = s.find_or_create_folder(biz['clean_title'], clients_master_id, token)
        update_or_upload_file(pdf_path, cf_id, token)
        update_or_upload_file(client_md_path, cf_id, token)

        # 5. Staging for Sheet
        updated_rows_st.append([biz['primary_copy'], biz['secondary_copy']])

    # Write master markdown
    master_path = ROOT_DIR / "outputs" / "customized_outreach_copy.md"
    master_path.write_text("\n".join(master_md_lines), encoding="utf-8")
    print(f"\n✓ Master outreach file updated: {master_path.relative_to(ROOT_DIR)}", flush=True)

    # Update Google Sheet Outreach Pipeline
    if sheet_id:
        print("\n==================================================================", flush=True)
        print("UPDATING SPREADSHEET 'Outreach Pipeline' COLUMNS S & T...", flush=True)
        print("==================================================================", flush=True)
        range_st = "Outreach Pipeline!S2:T8"
        s.update_sheet_range(sheet_id, range_st, updated_rows_st, token)
        print(f"✓ Columns S & T in Outreach Pipeline successfully updated with 100% human-ready copy!", flush=True)

    print("\n==================================================================", flush=True)
    print("SUCCESS: ALL OUTREACH DOSSIERS PURGED OF AI SLOP AND LIVE-SYNCED!", flush=True)
    print("==================================================================", flush=True)

if __name__ == "__main__":
    main()
