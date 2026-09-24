#!/usr/bin/env python3
"""
Full 60-Day LinkedIn Content & Carousel Engine Generator.
- Generates 60_day_calendar.md in outputs/linkedin_content/posts_copy/
- Syncs the full 60-day schedule (25 posts + 4 featured assets with rotation schedule) to Google Sheets
- Sets up formatting, widths, colors, and frozen headers
"""
import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

def load_env():
    p = Path(".env")
    env = {}
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

def get_access_token(client_id, client_secret, refresh_token):
    token_url = "https://oauth2.googleapis.com/token"
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }).encode("utf-8")
    req = urllib.request.Request(token_url, data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        tokens = json.loads(resp.read().decode("utf-8"))
        return tokens.get("access_token")

def batch_update_spreadsheet(sheet_id, requests, token):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate"
    payload = json.dumps({"requests": requests}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def update_range(sheet_id, range_a1, values, access_token):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{urllib.parse.quote(range_a1)}?valueInputOption=USER_ENTERED"
    payload = json.dumps({"range": range_a1, "values": values}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        method="PUT"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def build_data():
    headers = [
        "Post # / Asset",
        "Scheduled Date & Timing",
        "Post Format / Type",
        "Content Pillar / Topic",
        "Publish Status",
        "Hook Line / Headline",
        "Full Ready-to-Paste Copy (Text / Description)",
        "Asset to Attach / Local Path",
        "Target Goal / CTA",
        "LinkedIn Step-by-Step Instructions"
    ]

    featured_section_rows = [
        # Sub-header for Featured Section
        [
            "FEATURED SECTION ROTATION SCHEDULE (Always Pinned on Profile)",
            "Active Rotation Cadence",
            "Executive Showcase Assets",
            "Core Profile Conversion Engine",
            "LIVE ENGINE",
            "How to Rotate Featured Assets Over 60 Days",
            "MONTH 1 (Days 1–30): Focus on Single-Trade Plumbing Fleet ($822k Model) + 15-Min Booking Link + Post #1 Pinned.\n"
            "MONTH 2 (Days 31–60): Rotate Summit Mechanical ($486k Dual-Trade Model) to Slot #1, keep Apex in Slot #2, keep Booking Link in Slot #3, rotate Post #8 or #10 to Slot #4.\n\n"
            "This rotation keeps your profile fresh for returning prospects while presenting two distinct trade models!",
            "All assets located in outputs/clients/ and outputs/linkedin_content/carousels/",
            "Converts profile visitors into audit discovery calls with zero NDA or client confidentiality risk.",
            "Review rows below for exact copy and files to upload."
        ],
        # Featured Asset 1
        [
            "FEATURED ASSET #1 (Showcase Audit)",
            "Days 1–30: Slot #1\nDays 31–60: Slot #2",
            "Document / PDF Carousel",
            "Plumbing Fleet Diagnostic ($822k Model)",
            "READY TO UPLOAD",
            "Executive Systems Diagnostic: 15-Van Trade Fleet (Sample Deliverable)",
            "TITLE (Paste into Title field):\n"
            "Executive Systems Diagnostic: 15-Van Trade Fleet (Sample Deliverable)\n\n"
            "DESCRIPTION (Paste into Description field — 435 / 500 chars):\n"
            "Institutional 4-Pillar Diagnostic evaluating revenue leakage, dispatch workflows, and digital infrastructure for a 15-van service fleet ($822k annual loss model).\n\n"
            "Key Findings Inside:\n"
            "• $54k/mo lost to 6.9s mobile latency (52% bounce penalty)\n"
            "• $14.5k/mo lost to after-hours call abandonment\n"
            "• $18k/mo lost to single-tier flat estimates\n"
            "• Deloitte Effort vs. Impact Matrix & 90-Day Roadmap\n\n"
            "By Joel Adawah Sani | Principal Business Systems Consultant",
            "PDF File: outputs/clients/apex-home-services/audit_sample.pdf\n"
            "(HTML Preview: outputs/clients/apex-home-services/audit_sample.html)",
            "Demonstrates institutional Big-4 audit standard; highlights $822k revenue leakage model without NDA risk.",
            "1. In LinkedIn profile, scroll to 'Featured' -> click '+' -> 'Add media'\n"
            "2. Upload 'outputs/clients/apex-home-services/audit_sample.pdf'\n"
            "3. Copy Title & Description from Column G\n"
            "4. Click 'Save' — renders as interactive swipeable carousel!"
        ],
        # Featured Asset 2
        [
            "FEATURED ASSET #2 (Showcase Audit)",
            "Days 1–30: Standby / Slot #2\nDays 31–60: Slot #1 (Hero)",
            "Document / PDF Carousel",
            "Dual-Trade HVAC & Plumbing ($486k Model)",
            "READY TO UPLOAD",
            "Executive Diagnostic: Dual-Trade Plumbing & HVAC Fleet (Sample)",
            "TITLE (Paste into Title field):\n"
            "Executive Diagnostic: Dual-Trade Plumbing & HVAC Fleet (Sample)\n\n"
            "DESCRIPTION (Paste into Description field — 450 / 500 chars):\n"
            "Institutional 4-Pillar Diagnostic evaluating revenue leakage, dispatch workflows, and dual-trade cross-sell for an 18-van mechanical contractor ($486k annual loss model).\n\n"
            "Key Findings Inside:\n"
            "• $18k/mo uncaptured dual-trade maintenance memberships\n"
            "• $14.5k/mo after-hours emergency call abandonment\n"
            "• $8k/mo forfeited in single-tier equipment estimates\n"
            "• Deloitte Effort vs. Impact Prioritization Matrix\n\n"
            "By Joel Adawah Sani | Principal Business Systems Consultant",
            "PDF File: outputs/clients/summit-mechanical-services/audit_sample.pdf\n"
            "(HTML Preview: outputs/clients/summit-mechanical-services/audit_sample.html)",
            "Demonstrates dual-trade HVAC & Plumbing consulting capability; shows $486k cross-sell recovery model.",
            "1. In Featured section, click '+' -> 'Add media'\n"
            "2. Upload 'outputs/clients/summit-mechanical-services/audit_sample.pdf'\n"
            "3. Paste Title & Description from Column G\n"
            "4. Click 'Save'"
        ],
        # Featured Asset 3
        [
            "FEATURED ASSET #3 (Conversion Link)",
            "Days 1–60: Always Pinned (Slot #3)",
            "External URL Booking Card",
            "Direct Calendar Scheduling",
            "SETUP LINK",
            "Schedule a 15-Minute Operational Discovery Call",
            "TITLE (Paste into Title field):\n"
            "Schedule a 15-Minute Operational Discovery Call\n\n"
            "DESCRIPTION (Paste into Description field — 201 / 500 chars):\n"
            "Book a 1-on-1 walkthrough with Joel Adawah Sani to review your firm's operational bottlenecks, inspect lead leakage, and receive a customized 4-Pillar Executive Diagnostic for your service enterprise.",
            "Link Card: Paste your Calendly / Cal.com / HubSpot URL\n"
            "(e.g. calendly.com/your-name/discovery-call)",
            "Converts warm profile visitors and audit readers into booked 1-on-1 discovery calls.",
            "1. In Featured section, click '+' -> 'Add a link'\n"
            "2. Paste booking URL\n"
            "3. Paste Title & Description from Column G\n"
            "4. Click 'Save'"
        ],
        # Featured Asset 4
        [
            "FEATURED ASSET #4 (Pinned Authority Post)",
            "Days 1–30: Slot #4 (Post #1)\nDays 31–60: Slot #4 (Post #10)",
            "Published Feed Post",
            "Operational Case Study & Teardown",
            "READY TO POST",
            "Case Study: Stopping After-Hours Lead Leakage in Service Trades ($15k–$30k/mo)",
            "TITLE:\n"
            "Case Study: Stopping After-Hours Lead Leakage in Service Trades ($15k–$30k/mo)\n\n"
            "DESCRIPTION:\n"
            "Detailed operational breakdown analyzing why 9:00 PM emergency calls are abandoned and how automated triage and 10-second SMS response recaptures 10–15 high-margin jobs monthly without increasing administrative headcount.\n\n"
            "(See Post #1 below for the full post copy!)",
            "Live LinkedIn Post",
            "Drives social proof and authority directly from the feed into the Featured section.",
            "1. Publish Scheduled Post #1 to your feed\n"
            "2. Click the '...' (three dots) on the live post\n"
            "3. Click 'Feature on top of profile' (Star icon)"
        ]
    ]

    # Separator
    separator_row = [
        "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"
    ]

    # Part 2: 25 Date-Mapped Posts across 60 Days (3 posts per week)
    posts = [
        # Post 1 (Day 2)
        [
            "POST #1 (Day 2)",
            "Week 1: Tuesday 8:15 AM EST",
            "PDF Document Carousel (6 Slides)",
            "Speed-to-Lead & Response Latency",
            "READY TO POST",
            "Water is pouring through the ceiling at 9:00 PM.",
            "Water is pouring through the ceiling at 9:00 PM.\n\n"
            "They call the first 3 plumbing contractors on Google Maps. The first company that answers or replies by SMS within 60 seconds captures the $3,500 emergency replacement job.\n\n"
            "In our recent diagnostic audits of $2M–$5M trade fleets, we found businesses leaking $14,500 every single month from unassisted after-hours call abandonment.\n\n"
            "Here is the 3-step automated triage stack we install to capture those jobs automatically without burning out dispatchers:\n"
            "1. Instant SMS acknowledgment with water shutoff valve safety instructions.\n"
            "2. Urgency triage to classify genuine emergencies vs next-day routine requests.\n"
            "3. Priority dispatch alerting on-call technicians directly in the CRM calendar.\n\n"
            "Speed to lead isn't marketing—it's operational architecture.\n\n"
            "What's your current after-hours response time?\n\n"
            "#FieldService #TradeContractors #OperationalEfficiency #WorkflowAutomation",
            "PDF Carousel: outputs/linkedin_content/carousels/carousel_1_speed_to_lead.pdf",
            "Drive awareness around after-hours response latency; attach 6-slide carousel.",
            "1. Open LinkedIn -> 'Start a post'\n2. Click document icon ('Add a document')\n3. Upload 'carousel_1_speed_to_lead.pdf'\n4. Document title: 'The 9:00 PM Burst Pipe: Why Latency Kills Revenue'\n5. Paste copy from Column G -> Click 'Post'\n6. Pin to Featured (Slot #4)!"
        ],
        # Post 2 (Day 4)
        [
            "POST #2 (Day 4)",
            "Week 1: Thursday 9:00 AM EST",
            "Strategic Framework Breakdown",
            "Choice Architecture & Pricing",
            "READY TO POST",
            "Single-price estimates leave 25% margin on the table.",
            "Single-price estimates leave 25% margin on the table.\n\n"
            "When you present a customer with a single flat quote, their subconscious asks a binary question: \"Should I buy this, or should I shop around?\"\n\n"
            "When you switch field technicians to an interactive Good / Better / Best digital proposal:\n"
            "• Option 1 (Standard): Solves the immediate mechanical failure.\n"
            "• Option 2 (Enhanced): Adds extended 2-year warranty + preventative maintenance.\n"
            "• Option 3 (Premium): High-efficiency system upgrade + priority seasonal dispatch.\n\n"
            "Their brain shifts from a binary decision to choice architecture: \"Which of these three options is the best fit for my home?\"\n\n"
            "In our trade diagnostics, this single workflow adjustment consistently lifts average ticket sizes by 22% with zero extra marketing spend.\n\n"
            "I've pinned a complete 4-page sample audit in my Featured section showing the financial model behind this. Take a look.\n\n"
            "#PricingStrategy #HVAC #ContractorGrowth #OperationsConsulting",
            "Text Post with reference to Featured section document",
            "Drives profile visits to inspect the pinned audit in Featured section.",
            "1. Copy text from Column G\n2. Post on Thursday morning (8:45–9:15 AM EST)\n3. Reply to comments within 30 minutes"
        ],
        # Post 3 (Day 7)
        [
            "POST #3 (Day 7)",
            "Week 1: Sunday 6:30 PM EST",
            "Contrarian System Insight",
            "Operational Mindset & Growth",
            "READY TO POST",
            "You don't need more leads. You need fewer leaks.",
            "You don't need more leads. You need fewer leaks.\n\n"
            "Over the past 6 months, almost every trade contractor and service business owner who reached out to me said the same thing:\n"
            "\"Joel, we need more leads. Should we spend more on Google Ads or Facebook ads?\"\n\n"
            "When we run the numbers on their existing inbound volume, we find:\n"
            "• 35% of mobile visitors bounce because the site takes 6+ seconds to load on mobile.\n"
            "• 25% of evening calls go straight to an unmonitored voicemail.\n"
            "• Quoting is done on paper or flat single-item invoices, leaving 20% of upsell ticket value on the table.\n\n"
            "Spending $5,000 more on advertising when your operational funnel is leaking is like pouring water into a bucket with three holes in the bottom.\n\n"
            "Plug the operational leaks first. Then turn on the faucet.\n\n"
            "Ready to find the leaks in your firm's workflows? DM me \"AUDIT\" or schedule a 15-minute operational discovery call via my Featured link.\n\n"
            "#OperationsConsulting #BusinessSystems #TradeContractors #GrowthStrategy",
            "Text Only",
            "Prepares founders for Monday morning operational review; drives inbound DMs.",
            "1. Copy text from Column G\n2. Post on Sunday evening (6:00–7:00 PM EST)\n3. Monitor inbound messages"
        ],
        # Post 4 (Day 9)
        [
            "POST #4 (Day 9)",
            "Week 2: Tuesday 8:15 AM EST",
            "PDF Document Carousel (6 Slides)",
            "Dual-Trade Cross-Sell Silos",
            "READY TO POST",
            "The $216k trade cross-sell gap hiding in plain sight.",
            "The $216k trade cross-sell gap hiding in plain sight.\n\n"
            "If your company holds both plumbing and HVAC licenses, why are 88% of your plumbing customers calling someone else when their AC unit dies?\n\n"
            "In a recent audit of an 18-van dual-trade contractor, we identified $18,000/month ($216,000/year) in leaked revenue simply because the two departments operated as isolated software islands.\n\n"
            "Plumbing technicians were not prompted to inspect HVAC filters. HVAC maintenance plans were never offered to water heater replacement customers.\n\n"
            "The operational fix requires zero added headcount:\n"
            "1. CRM webhook automation that detects single-trade accounts upon invoice sign-off.\n"
            "2. Automated seasonal cross-sell sequences offering complimentary multi-point inspections.\n"
            "3. Unified recurring membership agreements that lock in year-round customer retention.\n\n"
            "Cross-selling isn't about pushing products—it's about connecting disconnected software workflows.\n\n"
            "#DualTrade #PlumbingAndHVAC #FieldServiceManagement #RecurringRevenue",
            "PDF Carousel: outputs/linkedin_content/carousels/carousel_3_dual_trade_cross_sell.pdf",
            "Demonstrates dual-trade consulting depth; attaches 6-slide carousel.",
            "1. Open LinkedIn -> 'Add a document'\n2. Upload 'carousel_3_dual_trade_cross_sell.pdf'\n3. Document title: 'The $216,000 Dual-Trade Cross-Sell Silo'\n4. Paste text from Column G -> Click 'Post'"
        ],
        # Post 5 (Day 11)
        [
            "POST #5 (Day 11)",
            "Week 2: Thursday 9:00 AM EST",
            "Video / Reel Script & Teardown",
            "DNS Infrastructure & Deliverability",
            "VIDEO SCRIPT READY",
            "Why your $12,000 equipment quotes land in spam.",
            "Why your $12,000 equipment quotes land in spam.\n\n"
            "You send a detailed commercial proposal or invoice from your CRM or Microsoft 365 / Google Workspace. Three days later, the client says: \"I never got it.\"\n\n"
            "When we audit contractor IT infrastructure, 7 out of 10 times we find an unauthenticated legacy SPF record or missing DMARC enforcement.\n\n"
            "If your domain's SPF record has a neutral \"?all\" mechanism or omits your active CRM sending IP, modern inbox filters (Gmail, Outlook) automatically quarantine your emails.\n\n"
            "The financial fallout:\n"
            "• Delayed payment cycles\n"
            "• Lost commercial proposals\n"
            "• Customer payment disputes\n\n"
            "Fixing your DNS records (SPF, DKIM, DMARC p=quarantine) takes less than 120 minutes and restores 99.8%+ inbox deliverability.\n\n"
            "Don't let DNS misconfigurations silently choke your cash flow.\n\n"
            "#EmailDeliverability #ITInfrastructure #BusinessSystems #CyberSecurity",
            "Video Script: outputs/linkedin_content/reels_and_video_scripts/reels_and_video_scripts.md (#2)",
            "Record 50s selfie video following Script #2, or post as high-engagement text post.",
            "1. Record 50-second phone video using Script #2 in reels_and_video_scripts.md\n2. Upload video with text from Column G\n3. (Alternatively: Post as text-only if video is not ready)"
        ],
        # Post 6 (Day 14)
        [
            "POST #6 (Day 14)",
            "Week 2: Sunday 6:30 PM EST",
            "Contrarian Metric Analysis",
            "KPI Rigor & Unit Economics",
            "SCHEDULED",
            "The most dangerous trade metric: Revenue per Truck.",
            "The most dangerous trade metric: Revenue per Truck.\n\n"
            "A contractor can boast $350k revenue per van, but if their dispatch response latency is 45 minutes, they are burning through $20,000/mo in paid Google Ads leads just to keep those trucks rolling.\n\n"
            "When you measure:\n"
            "1. First-touch response latency (Target: < 60s)\n"
            "2. Off-hours call salvage rate (Target: > 40%)\n"
            "3. Digital proposal option adoption (Target: > 55% choosing Tier 2/3)\n\n"
            "Your existing fleet generates 25% more gross margin with ZERO additional overhead.\n\n"
            "Measure the handoffs, not just the tailpipes.\n\n"
            "#BusinessMetrics #UnitEconomics #ContractorLeadership #Operations",
            "Text Only",
            "Provocative management insight prompting founders to rethink operational KPIs.",
            "1. Copy text from Column G\n2. Post Sunday evening at 6:30 PM EST\n3. Engage with trade executives"
        ],
        # Post 7 (Day 16)
        [
            "POST #7 (Day 16)",
            "Week 3: Tuesday 8:15 AM EST",
            "PDF Document Carousel (5 Slides)",
            "Institutional Diagnostic Framework",
            "READY TO POST",
            "Inside a 4-Pillar Systems Audit for a $5M fleet.",
            "Inside a 4-Pillar Systems Audit for a $5M fleet.\n\n"
            "Most business audits are full of vague consulting buzzwords: \"Improve synergy,\" \"Adopt AI,\" \"Streamline processes.\"\n\n"
            "When we audit a $1M–$10M service enterprise, we use a rigid 4-step reasoning scaffold:\n"
            "1. Evidence: Observed telemetry from DNS records, server response latency, review velocity, and CRM intake routes.\n"
            "2. Expected State: The operational benchmark for a top-decile enterprise of this scale.\n"
            "3. Gap Magnitude: The measured distance between reality and benchmark.\n"
            "4. Dollarized Leakage: The exact monthly and annual revenue forfeited across each bottleneck.\n\n"
            "In our latest diagnostic of a 15-van contractor, this model uncovered $822,000 in annualized revenue leakage ($68,500/month).\n\n"
            "Curious what this deliverable looks like?\n\n"
            "I've uploaded the complete 4-page anonymized sample audit right to my Featured section above. Feel free to review it and compare it against your own operations.\n\n"
            "#BusinessAudit #ManagementConsulting #OperationsArchitecture #McKinseyStandard",
            "PDF Carousel: outputs/linkedin_content/carousels/carousel_4_four_pillar_audit.pdf",
            "Validates diagnostic rigor; attaches 5-slide methodology carousel.",
            "1. Open LinkedIn -> 'Add a document'\n2. Upload 'carousel_4_four_pillar_audit.pdf'\n3. Document title: 'Inside a 4-Pillar Executive Diagnostic'\n4. Paste text from Column G -> Click 'Post'"
        ],
        # Post 8 (Day 18)
        [
            "POST #8 (Day 18)",
            "Week 3: Thursday 9:00 AM EST",
            "Interactive LinkedIn Poll",
            "Emergency Intake Benchmarking",
            "SCHEDULED",
            "Who answers your dispatch line at 8:30 PM?",
            "Who answers your dispatch line at 8:30 PM?\n\n"
            "We recently audited 25 regional service contractors and found that 68% of after-hours calls go straight to an unmonitored voicemail box, surrendering high-ticket jobs to instant competitors.\n\n"
            "Vote below to see how your operational intake compares with industry peers 👇\n\n"
            "#FieldService #Contractors #EmergencyDispatch #OperationsPoll",
            "LinkedIn Native Poll (4 Options):\n1. Unmonitored Voicemail (Listen at 8 AM)\n2. Traditional Answering Service (Take message)\n3. Automated SMS & Safety Triage (< 10s)\n4. Owner/Dispatcher Personal Cell",
            "High-engagement poll; uncovers prospective contractors who struggle with after-hours dispatch.",
            "1. Open LinkedIn -> Click 'Create a poll'\n2. Question: 'What happens when an emergency call comes in at 8:30 PM?'\n3. Add the 4 options from Column H\n4. Paste body copy from Column G -> Click 'Post'"
        ],
        # Post 9 (Day 21)
        [
            "POST #9 (Day 21)",
            "Week 3: Sunday 6:30 PM EST",
            "Reputation Engine Breakdown",
            "Google Map Pack & Review Deficit",
            "SCHEDULED",
            "A 4.8-star rating means zero without review velocity.",
            "A 4.8-star rating means zero without review velocity.\n\n"
            "In trade contracting, the Google Local Map Pack captures over 70% of high-intent mobile search clicks.\n\n"
            "When a regional market leader holds 4,500+ reviews and your business holds under 300, Google's local algorithm surrenders the top 3 placements to your competitor—even if your field craftsmanship is vastly superior.\n\n"
            "Why do established contractors have so few reviews?\n\n"
            "Because they rely on field technicians remembering to ask: \"Hey, could you leave us a review?\"\n\n"
            "Technicians are focused on fixing pipes and compressors, not asking for reviews.\n\n"
            "The automated solution:\n"
            "Connect CRM job completion webhooks to trigger an automated SMS review request exactly 45 minutes after the technician marks the job complete.\n\n"
            "Clients who install this review capture engine systematically generate 15–25 verified 5-star reviews every single month on autopilot.\n\n"
            "Take human memory out of your reputation engine.\n\n"
            "#LocalSEO #GoogleMaps #ContractorMarketing #ReputationManagement",
            "Text Only",
            "Breaks down the automated SMS review capture engine.",
            "1. Copy text from Column G\n2. Post on Sunday evening at 6:30 PM EST"
        ],
        # Post 10 (Day 23)
        [
            "POST #10 (Day 23)",
            "Week 4: Tuesday 8:15 AM EST",
            "PDF Document Carousel (5 Slides)",
            "Choice Architecture & Field Quoting",
            "READY TO POST",
            "The psychology of contractor quoting: 3 choices.",
            "Why single-price estimates leave 20% to 25% of margin on the table for mechanical contractors.\n\n"
            "When you present a customer with a single flat quote, their subconscious asks a binary question: \"Should I buy this, or should I shop around?\"\n\n"
            "When you switch field technicians to an interactive Good / Better / Best digital proposal:\n"
            "• Option 1 (Standard): Solves the immediate mechanical failure.\n"
            "• Option 2 (Enhanced): Adds extended 2-year warranty + preventative maintenance.\n"
            "• Option 3 (Premium): High-efficiency system upgrade + priority seasonal dispatch.\n\n"
            "Their brain shifts from a binary decision to choice architecture: \"Which of these three options is the best fit for my home?\"\n\n"
            "In our trade diagnostics, this single workflow adjustment consistently lifts average ticket sizes by 22% with zero extra marketing spend.\n\n"
            "I've pinned a complete 4-page sample audit in my Featured section showing the financial model behind this. Take a look.\n\n"
            "#PricingStrategy #HVAC #ContractorGrowth #OperationsConsulting",
            "PDF Carousel: outputs/linkedin_content/carousels/carousel_2_choice_architecture.pdf",
            "Drives direct profile visits; attaches 5-slide choice architecture carousel.",
            "1. Open LinkedIn -> 'Add a document'\n2. Upload 'carousel_2_choice_architecture.pdf'\n3. Title: 'Why Single-Price Estimates Forfeit 22% Margin'\n4. Paste text from Column G -> Click 'Post'\n5. Pin as Featured Asset #4!"
        ],
        # Post 11 (Day 25)
        [
            "POST #11 (Day 25)",
            "Week 4: Thursday 9:00 AM EST",
            "Video / Reel Script & Walkthrough",
            "Speed-to-Lead Test",
            "VIDEO SCRIPT READY",
            "Run this 60-second test on your phones tonight.",
            "Run this 60-second test on your phones tonight.\n\n"
            "Have someone call your office number from a personal phone.\n\n"
            "Does an active dispatcher answer? Does an automated text immediately reply with water shutoff safety instructions?\n\n"
            "Or does it ring 5 times and hit a generic voicemail that says: \"Leave a message and we'll call you back tomorrow at 8:00 AM\"?\n\n"
            "When a homeowner has an emergency leak or dead AC unit, they don't leave voicemails. Over 80% hang up within 6 seconds and call the next contractor on Google Maps.\n\n"
            "In a recent audit of a 15-van plumbing fleet, this single bottleneck was leaking $14,500 every month in surrendered jobs.\n\n"
            "You don't need to hire night staff. You need automated intake triage.\n\n"
            "What happened when you tested your line?\n\n"
            "#ContractorOperations #SpeedToLead #FieldService #Automation",
            "Video Script: outputs/linkedin_content/reels_and_video_scripts/reels_and_video_scripts.md (#1)",
            "Record 50-second phone video using Script #1, or post as high-engagement text post.",
            "1. Record 50-second video from Script #1\n2. Upload with copy from Column G\n3. Engage with commenters discussing after-hours triage"
        ],
        # Post 12 (Day 28)
        [
            "POST #12 (Day 28)",
            "Week 4: Sunday 6:30 PM EST",
            "Technical Web Diagnostic",
            "Mobile TTFB & Bounce Penalties",
            "SCHEDULED",
            "A 6.9-second load time burns 52% of your ad spend.",
            "A 6.9-second load time burns 52% of your ad spend.\n\n"
            "Over 82% of emergency plumbing and HVAC searches happen on a smartphone while the customer is actively looking at a leaking pipe or sweating in a 90°F living room.\n\n"
            "If your website takes 6.9 seconds to load:\n"
            "• Google data shows over 50% of distressed homeowners hit the back button before the first image loads.\n"
            "• For a contractor getting 1,500 mobile visits/mo, that is 465 abandoned sessions.\n"
            "• At a conservative 2% emergency conversion rate, you are forfeiting 9 replacement jobs every month.\n\n"
            "That's $54,000 in gross revenue lost every single month ($648,000/year) just from unoptimized WordPress plugins and missing server object caching.\n\n"
            "Sub-2 second mobile loading isn't an IT detail. It's a six-figure revenue engine.\n\n"
            "#CoreWebVitals #TechnicalSEO #MobileSpeed #ContractorRevenue",
            "Text Only",
            "Connects website technical performance directly to dollarized monthly revenue loss.",
            "1. Copy text from Column G\n2. Post on Sunday evening at 6:30 PM EST"
        ],
        # Post 13 (Day 30)
        [
            "POST #13 (Day 30)",
            "Week 5: Tuesday 8:15 AM EST",
            "Deep-Dive Case Study",
            "Dual-Trade Cross-Sell Case Study",
            "SCHEDULED",
            "How Summit Mechanical unlocked $486k in cross-sells.",
            "Case Study Breakdown: How an 18-van mechanical contractor uncovered $486,000 in uncaptured dual-trade capacity.\n\n"
            "When we conducted the 4-Pillar Diagnostic for Summit Mechanical (Plumbing & HVAC), we found an enterprise with stellar 4.8-star reviews and top-tier master licensing.\n\n"
            "Yet their growth was hitting a plateau. Why?\n\n"
            "1. $216k/yr uncaptured cross-sell: 1,200 single-trade customers were never offered dual-trade maintenance agreements.\n"
            "2. $174k/yr emergency leakage: Unassisted voicemail after 6 PM during weather spikes.\n"
            "3. $96k/yr flat quoting: Single-item replacement proposals leaving 20% margin on the table.\n\n"
            "By implementing automated cross-sell webhooks and 24/7 SMS intake, their projected payback horizon is under 14 business days.\n\n"
            "I've made the full 4-page diagnostic deliverable available to read in my Featured section above. Check it out.\n\n"
            "#CaseStudy #DualTrade #HVACBusiness #OperationsConsulting",
            "Directs to Featured Section Asset #2 (Summit Mechanical PDF)",
            "Drives profile traffic to read the newly rotated Summit Mechanical showcase deliverable.",
            "1. Rotate Summit Mechanical to Slot #1 in Featured Section\n2. Post text from Column G\n3. Direct readers to the Featured section"
        ],
        # Post 14 (Day 32)
        [
            "POST #14 (Day 32)",
            "Week 5: Thursday 9:00 AM EST",
            "Operational Framework",
            "Deloitte Effort vs. Impact Prioritization",
            "SCHEDULED",
            "The Deloitte Effort vs Impact Matrix for trade fleets.",
            "When contractors try to fix their operations, they usually make one fatal mistake:\n\n"
            "They try to overhaul their entire dispatch system, CRM, and website all at once.\n\n"
            "Six months later, they are burned out, $40,000 in the hole, and nothing is finished.\n\n"
            "In our diagnostics, we use the Deloitte Effort vs. Impact Prioritization Matrix:\n\n"
            "PHASE 1: TACTICAL QUICK WINS (< 30 DAYS)\n"
            "• Automated Review Engine: Low effort (3 days), Setup ~$500, Payback < 14 days.\n"
            "• SPF/DMARC DNS Repair: Low effort (2 hours), Setup ~$250, Immediate risk elimination.\n"
            "• 3-Tier Quoting Templates: Medium effort (1 week), Setup ~$1,500, Payback < 14 days.\n\n"
            "Total Phase 1 setup: Under $2,250. Value recovery: $75,000+ in 90 days.\n\n"
            "Fix the high-impact, low-effort bottlenecks first to fund larger structural transformations.\n\n"
            "#ManagementConsulting #PrioritizationMatrix #ContractorGrowth #Strategy",
            "Text Only with bullet framework",
            "Educates founders on sequencing operational fixes for quick capital payback.",
            "1. Copy text from Column G\n2. Post on Thursday morning at 9:00 AM EST"
        ],
        # Post 15 (Day 35)
        [
            "POST #15 (Day 35)",
            "Week 5: Sunday 6:30 PM EST",
            "Systems Philosophy",
            "Software vs Workflows",
            "SCHEDULED",
            "More software won't fix a broken dispatch workflow.",
            "More software won't fix a broken dispatch workflow.\n\n"
            "Contractors love buying software. They have ServiceTitan, Jobber, Housecall Pro, Zapier, HubSpot, Mailchimp, and three different messaging widgets.\n\n"
            "Yet their office staff still spends 15 hours a week re-typing customer addresses, copy-pasting dispatch notes, and manually texting technicians.\n\n"
            "Why?\n\n"
            "Because software is not a workflow.\n\n"
            "A tool is just a database. A workflow is the automated bridge connecting:\n"
            "• When Job Signs Off -> Trigger Review SMS\n"
            "• When Invoice Exceeds $3,000 -> Trigger Warranty Follow-up\n"
            "• When Single-Trade Customer Is Tagged -> Schedule Cross-Sell Offer\n\n"
            "Before you buy another $300/month software subscription, map out the handoffs between the tools you already own.\n\n"
            "#SaaS #OperationsArchitecture #WorkflowAutomation #FieldService",
            "Text Only",
            "Addresses software bloat in mid-market service firms.",
            "1. Copy text from Column G\n2. Post on Sunday evening at 6:30 PM EST"
        ],
        # Post 16 (Day 37)
        [
            "POST #16 (Day 37)",
            "Week 6: Tuesday 8:15 AM EST",
            "Technical Teardown",
            "Review Velocity Architecture",
            "SCHEDULED",
            "How to get 25 verified Google reviews every month.",
            "How to get 25 verified Google reviews every month.\n\n"
            "Here is the exact automation sequence we install for trade contractors:\n\n"
            "Step 1: Technician completes job in CRM and collects customer signature.\n"
            "Step 2: CRM webhook fires 'job.completed' payload to our automation gateway.\n"
            "Step 3: A 45-minute delay timer initiates (allows homeowner to inspect work and relax).\n"
            "Step 4: Personalized SMS triggers: \"Hi [First Name], thanks for choosing [Company] today! Could you take 20 seconds to share your experience with technician [Tech Name]? [Direct GBP Review Link]\"\n"
            "Step 5: If review is logged, system updates CRM profile to 'Advocate' status.\n\n"
            "Results across client fleets:\n"
            "• Review conversion jumps from 4% to 28%.\n"
            "• 15 to 25 verified 5-star reviews added every 30 days.\n"
            "• Google Map Pack placement moves from page 2 to top 3 within 90 days.\n\n"
            "Automate the ask. Own the Map Pack.\n\n"
            "#GoogleReviews #ReputationAutomation #LocalSEO #ServiceContractors",
            "Text Only with Step-by-Step Architecture",
            "Provides transparent technical breakdown of review automation.",
            "1. Copy text from Column G\n2. Post on Tuesday morning at 8:15 AM EST"
        ],
        # Post 17 (Day 39)
        [
            "POST #17 (Day 39)",
            "Week 6: Thursday 9:00 AM EST",
            "Video / Reel Script",
            "Pricing Psychology Hack",
            "VIDEO SCRIPT READY",
            "Stop sending flat quotes. Give customers 3 choices.",
            "Stop sending flat quotes. Give customers 3 choices.\n\n"
            "When you show a homeowner one price—say $5,500—their brain asks a binary question: \"Should I buy this, or should I get a second quote from someone else?\"\n\n"
            "But when you present a 3-tier Good / Better / Best proposal:\n"
            "• Tier 1: Standard replacement\n"
            "• Tier 2: Upgraded efficiency + 5-year warranty\n"
            "• Tier 3: Premium unit + whole-home filtration + annual membership\n\n"
            "Their brain completely shifts. Now they ask:\n"
            "\"Which of these three is the best fit for my home?\"\n\n"
            "Over 60% of homeowners choose Tier 2 or Tier 3. That’s a 22% average ticket lift without spending a dime on marketing.\n\n"
            "Choice architecture works. Stop quoting single prices.\n\n"
            "#PricingStrategy #ContractorSales #HVAC #OperationsHacks",
            "Video Script: outputs/linkedin_content/reels_and_video_scripts/reels_and_video_scripts.md (#3)",
            "Record 45-second video from Script #3, or post as text post.",
            "1. Record 45-second video using Script #3\n2. Upload with copy from Column G\n3. Engage with trade sales managers"
        ],
        # Post 18 (Day 42)
        [
            "POST #18 (Day 42)",
            "Week 6: Sunday 6:30 PM EST",
            "Strategic Reflection",
            "Building Software Moats",
            "SCHEDULED",
            "Why single-trade fleets are losing to dual-trade.",
            "Why single-trade fleets are losing to dual-trade.\n\n"
            "Consider two 15-van plumbing contractors in the same city:\n\n"
            "Company A: Relies on manual dispatchers, paper quotes, and unmonitored night voicemails. They spend $15k/mo on advertising to maintain revenue.\n\n"
            "Company B: Has automated < 10s SMS emergency triage, automated technician GPS tracking, 3-tier digital proposals, and automated post-service review capture.\n\n"
            "Company B converts 35% more leads, closes 22% higher ticket values, commands 4,000+ Google reviews, and operates at 8% higher net margins.\n\n"
            "In 2026 and beyond, your competitive moat is your operational architecture.\n\n"
            "How resilient is your firm's operational stack?\n\n"
            "#ContractorMoat #BusinessTransformation #LogisticsArchitecture #FutureOfTrades",
            "Text Only",
            "Inspires business owners to think about long-term enterprise valuation.",
            "1. Copy text from Column G\n2. Post Sunday evening at 6:30 PM EST"
        ],
        # Post 19 (Day 44)
        [
            "POST #19 (Day 44)",
            "Week 7: Tuesday 8:15 AM EST",
            "Seasonal Volatility & Weather",
            "Disaster & Peak Weather Triage",
            "SCHEDULED",
            "First freeze hits: does your dispatch collapse?",
            "First freeze hits: does your dispatch collapse?\n\n"
            "In the home services industry, revenue isn't linear—it's driven by severe weather volatility.\n\n"
            "When a sudden freeze hits or temperatures spike above 100°F, call volume doesn't increase by 20%—it surges by 400% in 3 hours.\n\n"
            "What happens to a contractor relying on traditional phone dispatch?\n"
            "• Office lines jam.\n"
            "• Callers sit on hold for 8 minutes, then hang up.\n"
            "• Minor water leaks or AC capacitor failures are treated with the same urgency as major pipe bursts.\n"
            "• High-margin replacement jobs are forfeited to competitors who answer instantly.\n\n"
            "Automated conversational intake triage solves this by instantly greeting callers via SMS/Voice, providing immediate shut-off instructions to protect the home, and auto-categorizing calls by severity.\n\n"
            "Prepare your digital dispatch infrastructure before the next weather event strikes.\n\n"
            "#EmergencyDispatch #HVACService #PlumbingContractor #DisasterResilience",
            "Text Only",
            "Generates urgency around seasonal weather preparation and automated triage.",
            "1. Copy text from Column G\n2. Post on Tuesday morning at 8:15 AM EST"
        ],
        # Post 20 (Day 46)
        [
            "POST #20 (Day 46)",
            "Week 7: Thursday 9:00 AM EST",
            "Interactive LinkedIn Poll",
            "Quoting Close Rate Benchmark",
            "SCHEDULED",
            "What is your real close rate on replacement quotes?",
            "What is your real close rate on replacement quotes?\n\n"
            "Across the contractors we audit, close rates on single flat-price estimates average 32%. Contractors using interactive 3-tier Good/Better/Best proposals average 54%.\n\n"
            "Vote below to benchmark your firm against industry averages 👇\n\n"
            "#ContractorPoll #SalesPerformance #HVACSales #PlumbingEstimates",
            "LinkedIn Native Poll (4 Options):\n1. Under 30% (Standard flat quoting)\n2. 30% – 45% (Some follow-up)\n3. 45% – 60% (Using tiered proposals)\n4. Over 60% (Top-decile sales execution)",
            "High-engagement poll revealing quoting efficiency across the network.",
            "1. Open LinkedIn -> 'Create a poll'\n2. Add question and 4 options from Column H\n3. Paste copy from Column G -> Click 'Post'"
        ],
        # Post 21 (Day 49)
        [
            "POST #21 (Day 49)",
            "Week 7: Sunday 6:30 PM EST",
            "Contrarian Operations Insight",
            "Headcount vs Systems",
            "SCHEDULED",
            "Stop hiring more dispatchers to fix missed calls.",
            "Stop hiring more dispatchers to fix missed calls.\n\n"
            "When trade contractors experience customer support bottlenecks, the default reaction is: \"We need to hire another CSR or night dispatcher.\"\n\n"
            "That adds $45,000 to $60,000 in annual payroll, plus payroll taxes, training, and management overhead.\n\n"
            "Yet three months later, response times are still sluggish.\n\n"
            "Why?\n\n"
            "Because 70% of customer inquiries are repetitive, low-complexity tasks:\n"
            "• \"When will the technician arrive?\"\n"
            "• \"How do I shut off the main water valve?\"\n"
            "• \"Can I get a copy of my invoice?\"\n\n"
            "Automating routine inquiries with real-time GPS tracking SMS and self-serve invoice portals frees up your existing CSRs to focus on high-ticket commercial dispatch.\n\n"
            "Scale systems before you scale headcount.\n\n"
            "#OperationsLeadership #HiringMistakes #BusinessEfficiency #Automation",
            "Text Only",
            "Challenges traditional headcount scaling in favor of workflow automation.",
            "1. Copy text from Column G\n2. Post Sunday evening at 6:30 PM EST"
        ],
        # Post 22 (Day 51)
        [
            "POST #22 (Day 51)",
            "Week 8: Tuesday 8:15 AM EST",
            "Suburban SEO Architecture",
            "Hyper-Local Dominance",
            "SCHEDULED",
            "County-wide targeting burns your high-margin leads.",
            "County-wide targeting burns your high-margin leads.\n\n"
            "In affluent suburban corridors, homeowners don't search: \"Plumber Austin TX.\"\n\n"
            "They search: \"Emergency water heater repair Lakeway\" or \"Rough Hollow HVAC service.\"\n\n"
            "When we audit contractor websites, 8 out of 10 have a single 'Service Areas' page listing 25 cities in plain text.\n\n"
            "Google's local algorithm completely ignores this.\n\n"
            "The architecture that wins:\n"
            "Deploy dedicated programmatic neighborhood landing pages for every master-planned community in your primary service zone.\n\n"
            "Each page features local job photos, verified local customer testimonials, and specific municipal water pressure or freeze advisories.\n\n"
            "Dominating 6 high-income subdivisions adds $35,000 to $50,000 in monthly high-margin billable capacity.\n\n"
            "#LocalSEO #SuburbanTargeting #ContractorGrowth #DigitalMarketing",
            "Text Only",
            "Explains hyper-local landing page architecture for affluent subdivisions.",
            "1. Copy text from Column G\n2. Post on Tuesday morning at 8:15 AM EST"
        ],
        # Post 23 (Day 53)
        [
            "POST #23 (Day 53)",
            "Week 8: Thursday 9:00 AM EST",
            "Financial Teardown",
            "The $68,500/Month Leakage Model",
            "SCHEDULED",
            "The Anatomy of a $68,500/Mo Operational Leakage Model.",
            "Here is the exact financial modeling formula we use in an Executive Systems Diagnostic to quantify operational friction:\n\n"
            "1. Mobile TTFB Latency Drop-Off:\n"
            "1,500 monthly mobile visits × 31% excess bounce penalty = 465 lost visits × 2% conversion × $5,800 replacement ticket = $54,000/mo ($648,000/yr).\n\n"
            "2. After-Hours Call Abandonment:\n"
            "10 unassisted emergency calls lost monthly × $1,450 blended emergency ticket = $14,500/mo ($174,000/yr).\n\n"
            "3. Single-Tier Quoting Penalty:\n"
            "20 major equipment replacements monthly forfeiting 22% choice architecture lift ($900/job) = $18,000/mo ($216,000/yr).\n\n"
            "TOTAL ANNUAL GROSS LEAKAGE: $822,000.\n\n"
            "Operational friction isn't qualitative. It has an exact dollar price tag.\n\n"
            "Review the full financial model in the sample audit deliverable pinned in my Featured section.\n\n"
            "#FinancialModeling #OperationsConsulting #UnitEconomics #McKinseyStandard",
            "Text Only with Economic Formulas",
            "Displays the mathematical rigor behind the 4-Pillar Diagnostic model.",
            "1. Copy text from Column G\n2. Post on Thursday morning at 9:00 AM EST"
        ],
        # Post 24 (Day 56)
        [
            "POST #24 (Day 56)",
            "Week 8: Sunday 6:30 PM EST",
            "Strategic Reflection",
            "The 3 Software Handoffs to Automate",
            "SCHEDULED",
            "The 3 software handoffs trade fleets must automate.",
            "If your trade business is between $2M and $10M in revenue, these are the 3 non-negotiable software handoffs that must run on autopilot:\n\n"
            "1. Lead to Triage (Under 60 Seconds):\n"
            "Every web inquiry and missed call must trigger an automated SMS with safety guidance and CRM calendar booking.\n\n"
            "2. Completed Ticket to Review Request (45 Minutes):\n"
            "Job completion in field CRM must trigger an automated review sequence via webhook with zero technician friction.\n\n"
            "3. Completed Single-Trade Invoice to Cross-Sell Agreement (14 Days):\n"
            "Plumbing jobs must automatically feed seasonal HVAC maintenance offers, and vice versa.\n\n"
            "Automate these three handoffs and your business will out-execute competitors twice your size.\n\n"
            "#WorkflowAutomation #FieldServiceManagement #ContractorSystems #Scale",
            "Text Only",
            "Executive summary of core automated workflows; prepares readers for capstone audit offer.",
            "1. Copy text from Column G\n2. Post Sunday evening at 6:30 PM EST"
        ],
        # Post 25 (Day 58 / Capstone)
        [
            "POST #25 (Day 58)",
            "Week 9: Tuesday 8:15 AM EST",
            "Capstone Offer & Audit Invitation",
            "Direct Diagnostic Invitation",
            "SCHEDULED",
            "What we learned auditing $45M in trade revenue.",
            "Over the past 60 days, we've broken down dozens of operational workflows across regional plumbing, HVAC, and mechanical service enterprises.\n\n"
            "The biggest takeaway?\n\n"
            "Every single contractor we audited had world-class craftsmen, dedicated field crews, and active trade licenses.\n\n"
            "Yet almost all of them were leaking between $200,000 and $800,000 annually through invisible digital bottlenecks: 7-second mobile load times, unassisted night voicemails, unauthenticated DNS records, and disconnected software silos.\n\n"
            "Plugging these leaks requires zero new hires and minimal CapEx.\n\n"
            "Ready to inspect your firm's operational bottlenecks?\n\n"
            "I am opening up 5 complimentary 4-Pillar Executive Systems Diagnostics for trade contractors and commercial service operators this month.\n\n"
            "We analyze your sales conversion, intake speed, field quoting mechanics, and internal infrastructure—delivering a comprehensive 4-page executive roadmap and dollarized leakage model.\n\n"
            "📩 Send me a direct message with your domain or schedule a 15-minute operational discovery call via my Featured link above.\n\n"
            "#BusinessAudit #OperationalArchitecture #TradeContractors #GrowthMindset",
            "Direct CTA to DM or Featured Booking Link",
            "High-conversion capstone offer driving inbound executive audit requests.",
            "1. Copy text from Column G\n2. Post on Tuesday morning at 8:15 AM EST\n3. Reply to DMs within 15 minutes with booking link"
        ]
    ]

    all_rows = [headers] + featured_section_rows + [separator_row] + posts
    return all_rows

def main():
    env = load_env()
    client_id = env["GOOGLE_CLIENT_ID"]
    client_secret = env["GOOGLE_CLIENT_SECRET"]
    refresh_token = env["GOOGLE_REFRESH_TOKEN"]
    sheet_id = env["GOOGLE_SHEET_ID"]

    token = get_access_token(client_id, client_secret, refresh_token)
    print("Obtained fresh access token.")

    # 1. Inspect existing sheets to get sheetId
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        meta = json.loads(resp.read().decode("utf-8"))

    existing_sheets = {s["properties"]["title"]: s["properties"]["sheetId"] for s in meta.get("sheets", [])}
    tab_name = "LinkedIn Content Calendar"

    sheet_tab_id = existing_sheets.get(tab_name)
    if not sheet_tab_id:
        print("Tab not found. Please create it first.")
        return

    data_rows = build_data()
    print(f"Prepared {len(data_rows)} total rows (Headers + Featured Rotation + 25 Scheduled Posts).")

    # 2. Write markdown backup file
    md_path = "outputs/linkedin_content/posts_copy/60_day_calendar.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 60-Day LinkedIn Content Calendar & Featured Section Engine\n\n")
        f.write("**Lead Consultant**: Joel Adawah Sani | Principal Business Systems Consultant\n")
        f.write("**Target Audience**: $1M–$10M Trade Contractors, Mechanical Executives, Commercial Service Founders\n")
        f.write("**Cadence**: 3 Posts / Week (Tuesday 8:15 AM, Thursday 9:00 AM, Sunday 6:30 PM EST)\n\n")
        f.write("---\n\n## Part 1: Featured Section Rotation & Scheduling Roadmap\n\n")
        for fr in data_rows[1:6]:
            f.write(f"### {fr[0]} ({fr[1]})\n")
            f.write(f"- **Format**: {fr[2]}\n")
            f.write(f"- **Status**: `{fr[4]}`\n")
            f.write(f"- **Headline / Hook**: {fr[5]}\n")
            f.write(f"- **Local Asset Path**: `{fr[7]}`\n")
            f.write(f"- **Copy-Paste Text**:\n\n```text\n{fr[6]}\n```\n\n")
            f.write(f"- **Instructions**: {fr[9]}\n\n---\n\n")

        f.write("## Part 2: 25 Scheduled Posts (60-Day Date-Mapped Publishing Calendar)\n\n")
        for pr in data_rows[7:]:
            f.write(f"### {pr[0]} — {pr[1]}\n")
            f.write(f"- **Format**: {pr[2]}\n")
            f.write(f"- **Content Pillar**: {pr[3]}\n")
            f.write(f"- **Status**: `{pr[4]}`\n")
            f.write(f"- **Hook**: {pr[5]}\n")
            f.write(f"- **Attached Asset**: `{pr[7]}`\n")
            f.write(f"- **Target CTA**: {pr[8]}\n")
            f.write(f"- **Ready-to-Paste Copy**:\n\n```text\n{pr[6]}\n```\n\n")
            f.write(f"- **Posting Instructions**: {pr[9]}\n\n---\n\n")

    print(f"Markdown calendar backup written to: {md_path}")

    # 3. Update Google Sheet
    target_range = f"'{tab_name}'!A1:J{len(data_rows)}"
    print(f"Writing {len(data_rows)} rows to {target_range}...")
    update_range(sheet_id, target_range, data_rows, token)
    print("Values written successfully.")

    # 4. Format the Google Sheet
    format_requests = [
        # Main Header (Row 1): Dark Navy, Bold White Text, Centered
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_tab_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 10
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {
                            "red": 0.06,
                            "green": 0.12,
                            "blue": 0.24
                        },
                        "textFormat": {
                            "foregroundColor": {
                                "red": 1.0,
                                "green": 1.0,
                                "blue": 1.0
                            },
                            "fontSize": 11,
                            "bold": True
                        },
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE",
                        "wrapStrategy": "WRAP"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)"
            }
        },
        # Freeze Row 1
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_tab_id,
                    "gridProperties": {
                        "frozenRowCount": 1
                    }
                },
                "fields": "gridProperties.frozenRowCount"
            }
        },
        # Row 1 Height = 45px
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_tab_id,
                    "dimension": "ROWS",
                    "startIndex": 0,
                    "endIndex": 1
                },
                "properties": {
                    "pixelSize": 45
                },
                "fields": "pixelSize"
            }
        },
        # Text wrapping and font size for all data cells
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_tab_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(data_rows),
                    "startColumnIndex": 0,
                    "endColumnIndex": 10
                },
                "cell": {
                    "userEnteredFormat": {
                        "wrapStrategy": "WRAP",
                        "verticalAlignment": "TOP",
                        "textFormat": {
                            "fontSize": 10
                        }
                    }
                },
                "fields": "userEnteredFormat(wrapStrategy,verticalAlignment,textFormat.fontSize)"
            }
        },
        # Bold Post # (Col 0)
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_tab_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(data_rows),
                    "startColumnIndex": 0,
                    "endColumnIndex": 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(textFormat.bold)"
            }
        },
        # Center align Schedule (Col 1), Format (Col 2), Status (Col 4)
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_tab_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(data_rows),
                    "startColumnIndex": 1,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment,textFormat.bold)"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_tab_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(data_rows),
                    "startColumnIndex": 4,
                    "endColumnIndex": 5
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment,textFormat.bold)"
            }
        }
    ]

    # Column Widths
    # Col 0 (Post # / Asset): 170px
    # Col 1 (Timing): 160px
    # Col 2 (Format): 180px
    # Col 3 (Pillar / Topic): 190px
    # Col 4 (Status): 130px
    # Col 5 (Hook): 240px
    # Col 6 (Full Copy): 520px
    # Col 7 (Asset Path): 250px
    # Col 8 (CTA): 180px
    # Col 9 (Instructions): 240px
    widths = [170, 160, 180, 190, 130, 240, 520, 250, 180, 240]
    for idx, w in enumerate(widths):
        format_requests.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_tab_id,
                    "dimension": "COLUMNS",
                    "startIndex": idx,
                    "endIndex": idx + 1
                },
                "properties": {
                    "pixelSize": w
                },
                "fields": "pixelSize"
            }
        })

    print("Applying styling and column dimensions...")
    batch_update_spreadsheet(sheet_id, format_requests, token)
    print("Formatting applied successfully.")
    print(f"\nSUCCESS! 60-Day LinkedIn Content & Carousel Engine synchronized to:")
    print(f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid={sheet_tab_id}")

if __name__ == "__main__":
    main()
