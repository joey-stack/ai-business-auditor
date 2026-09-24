#!/usr/bin/env python3
"""
Sync LinkedIn Content Calendar & Featured Section Showcase to Google Sheets.
Creates a dedicated 'LinkedIn Content Calendar' tab in the user's Google Spreadsheet.
Includes:
- Section 1: 4 Drop-in Ready Featured Section Media Assets (Apex Home Services & Summit Mechanical)
- Section 2: 8 High-Impact Scheduled LinkedIn Posts (Day, Time, Hook, Full Copy, CTA, Hashtags)
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

def main():
    env = load_env()
    client_id = env["GOOGLE_CLIENT_ID"]
    client_secret = env["GOOGLE_CLIENT_SECRET"]
    refresh_token = env["GOOGLE_REFRESH_TOKEN"]
    sheet_id = env["GOOGLE_SHEET_ID"]

    token = get_access_token(client_id, client_secret, refresh_token)
    print("Obtained fresh access token.")

    # 1. Inspect existing sheets to check if 'LinkedIn Content Calendar' exists
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        meta = json.loads(resp.read().decode("utf-8"))

    existing_sheets = {s["properties"]["title"]: s["properties"]["sheetId"] for s in meta.get("sheets", [])}
    tab_name = "LinkedIn Content Calendar"

    new_sheet_id = None

    if tab_name in existing_sheets:
        print(f"Tab '{tab_name}' already exists (sheetId: {existing_sheets[tab_name]}). Updating existing sheet.")
        new_sheet_id = existing_sheets[tab_name]
    else:
        print(f"Creating new tab '{tab_name}'...")
        add_sheet_req = {
            "addSheet": {
                "properties": {
                    "title": tab_name,
                    "gridProperties": {
                        "rowCount": 35,
                        "columnCount": 10,
                        "frozenRowCount": 1
                    },
                    "tabColor": {
                        "red": 0.12,
                        "green": 0.53,
                        "blue": 0.90
                    }
                }
            }
        }
        res = batch_update_spreadsheet(sheet_id, [add_sheet_req], token)
        new_sheet_id = res["replies"][0]["addSheet"]["properties"]["sheetId"]
        print(f"Tab '{tab_name}' created successfully with sheetId: {new_sheet_id}")

    # 2. Define Headers
    headers = [
        "Category / Asset",
        "Scheduled Timing",
        "Content Pillar / Focus",
        "Publish Status",
        "Hook Line / Headline",
        "Full Ready-to-Paste Copy (Text / Description)",
        "Asset to Attach / Local Path",
        "Target Goal / CTA",
        "LinkedIn Step-by-Step Instructions"
    ]

    # Section 1: Featured Section Assets (4 Items)
    featured_rows = [
        # Featured 1: Apex Home Services (Plumbing Diagnostic)
        [
            "FEATURED ASSET #1 (Showcase Audit)",
            "Always Pinned (Slot #1)",
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
            "Establishes institutional Big-4 credibility; showcases $822k leakage model without risking client confidentiality or NDA breaches.",
            "1. In LinkedIn profile, scroll to 'Featured' -> click '+' -> 'Add media'\n"
            "2. Upload 'outputs/clients/apex-home-services/audit_sample.pdf'\n"
            "3. Paste Title & Description from Column F\n"
            "4. Click 'Save' — renders as an interactive document carousel!"
        ],
        # Featured 2: Summit Mechanical (Dual-Trade Plumbing & HVAC)
        [
            "FEATURED ASSET #2 (Showcase Audit)",
            "Always Pinned (Slot #2)",
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
            "Demonstrates multi-trade expertise across HVAC and Plumbing; shows how dual-trade cross-sell stops $486k leakage.",
            "1. In Featured section, click '+' -> 'Add media'\n"
            "2. Upload 'outputs/clients/summit-mechanical-services/audit_sample.pdf'\n"
            "3. Paste Title & Description from Column F\n"
            "4. Click 'Save' — provides a 2nd swipeable audit carousel!"
        ],
        # Featured 3: 15-Minute Discovery Call Link
        [
            "FEATURED ASSET #3 (Conversion Link)",
            "Always Pinned (Slot #3)",
            "Direct Calendar Booking",
            "SETUP LINK",
            "Schedule a 15-Minute Operational Discovery Call",
            "TITLE (Paste into Title field):\n"
            "Schedule a 15-Minute Operational Discovery Call\n\n"
            "DESCRIPTION (Paste into Description field — 201 / 500 chars):\n"
            "Book a 1-on-1 walkthrough with Joel Adawah Sani to review your firm's operational bottlenecks, inspect lead leakage, and receive a customized 4-Pillar Executive Diagnostic for your service enterprise.",
            "Link Card: Paste your Calendly / Cal.com / HubSpot URL\n"
            "(e.g. calendly.com/your-name/discovery-call)",
            "Converts profile visitors and audit readers into scheduled discovery calls without friction.",
            "1. In Featured section, click '+' -> 'Add a link'\n"
            "2. Paste your booking URL\n"
            "3. Paste Title & Description from Column F\n"
            "4. Click 'Save'"
        ],
        # Featured 4: Pinned Thought Leadership Post
        [
            "FEATURED ASSET #4 (Pinned Post)",
            "Always Pinned (Slot #4)",
            "Operational Case Study & Teardown",
            "READY TO POST",
            "Case Study: Stopping After-Hours Lead Leakage in Service Trades",
            "TITLE:\n"
            "Case Study: Stopping After-Hours Lead Leakage in Service Trades ($15k–$30k/mo)\n\n"
            "DESCRIPTION:\n"
            "Detailed operational breakdown analyzing why 9:00 PM emergency calls are abandoned and how automated triage and 10-second SMS response recaptures 10–15 high-margin jobs monthly without increasing administrative headcount.\n\n"
            "(See Post #1 below for the full post copy!)",
            "Published LinkedIn Post",
            "Drives social proof and authority directly from the feed into the Featured section.",
            "1. Publish Scheduled Post #1 to your feed\n"
            "2. Click the '...' (three dots) on the top right of the live post\n"
            "3. Click 'Feature on top of profile' (Star icon)"
        ]
    ]

    # Section 2: Scheduled LinkedIn Posts (8 Posts across 4 Weeks)
    post_rows = [
        # Post 1
        [
            "SCHEDULED POST #1",
            "Week 1: Tuesday 8:15 AM EST",
            "Speed-to-Lead & Response Latency",
            "READY TO POST",
            "If a homeowner has a burst pipe at 9:00 PM, they don't fill out a 7-field contact form and wait 12 hours for an email reply.",
            "If a homeowner has a burst pipe at 9:00 PM, they don't fill out a 7-field contact form and wait 12 hours for an email reply.\n\n"
            "They call the first 3 plumbing contractors on Google Maps. The first company that answers or replies by SMS within 60 seconds captures the $3,500 emergency replacement job.\n\n"
            "In our recent diagnostic audits of $2M–$5M trade fleets, we found businesses leaking $14,500 every single month from unassisted after-hours call abandonment.\n\n"
            "Here is the 3-step automated triage stack we install to capture those jobs automatically without burning out dispatchers:\n"
            "1. Instant SMS acknowledgment with water shutoff valve safety instructions.\n"
            "2. Urgency triage to classify genuine emergencies vs next-day routine requests.\n"
            "3. Priority dispatch alerting on-call technicians directly in the CRM calendar.\n\n"
            "Speed to lead isn't marketing—it's operational architecture.\n\n"
            "What's your current after-hours response time?\n\n"
            "#FieldService #TradeContractors #OperationalEfficiency #WorkflowAutomation",
            "Text Post (or attach page 1 screenshot of audit_sample.pdf)",
            "Inspires contractors to inspect after-hours response latency; drives profile views.",
            "1. Copy text from Column F\n2. Open LinkedIn -> 'Start a post'\n3. Paste text, verify spacing, and click 'Post' at 8:15 AM\n4. Pin to Featured (Slot #4)!"
        ],
        # Post 2
        [
            "SCHEDULED POST #2",
            "Week 1: Thursday 9:00 AM EST",
            "Choice Architecture & Pricing",
            "READY TO POST",
            "Why single-price estimates leave 20% to 25% of margin on the table for mechanical contractors.",
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
            "Text Post with reference to Featured section document",
            "Drives direct profile visits to view the pinned Showcase Audit PDF in Featured section.",
            "1. Copy text from Column F\n2. Post on LinkedIn on Thursday morning (8:45–9:15 AM EST)\n3. Respond to early comments within 30 minutes"
        ],
        # Post 3
        [
            "SCHEDULED POST #3",
            "Week 2: Tuesday 8:15 AM EST",
            "Dual-Trade Cross-Sell Silos",
            "SCHEDULED",
            "The biggest unmined goldmine for home service contractors: the dual-trade cross-sell silo.",
            "The biggest unmined goldmine for home service contractors: the dual-trade cross-sell silo.\n\n"
            "If your company holds both plumbing and HVAC licenses, why are 88% of your plumbing customers calling someone else when their AC unit dies?\n\n"
            "In a recent audit of an 18-van dual-trade contractor, we identified $18,000/month ($216,000/year) in leaked revenue simply because the two departments operated as isolated software islands.\n\n"
            "Plumbing technicians were not prompted to inspect HVAC filters. HVAC maintenance plans were never offered to water heater replacement customers.\n\n"
            "The operational fix requires zero added headcount:\n"
            "1. CRM webhook automation that detects single-trade accounts upon invoice sign-off.\n"
            "2. Automated seasonal cross-sell sequences offering complimentary multi-point inspections.\n"
            "3. Unified recurring membership agreements that lock in year-round customer retention.\n\n"
            "Cross-selling isn't about pushing products—it's about connecting disconnected software workflows.\n\n"
            "#DualTrade #PlumbingAndHVAC #FieldServiceManagement #RecurringRevenue",
            "Text Post (or attach Summit Mechanical Page 1 KPI snapshot)",
            "Highlights dual-trade HVAC/Plumbing consulting specialization.",
            "1. Copy text from Column F\n2. Schedule or post on Tuesday Week 2 at 8:15 AM EST\n3. Engage with trade business owners in comments"
        ],
        # Post 4
        [
            "SCHEDULED POST #4",
            "Week 2: Thursday 9:00 AM EST",
            "DNS Infrastructure & Deliverability",
            "SCHEDULED",
            "Why your $12,000 commercial equipment quotes are ending up in your client's spam folder (and how to fix it in 2 hours).",
            "Why your $12,000 commercial equipment quotes are ending up in your client's spam folder (and how to fix it in 2 hours).\n\n"
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
            "Text Post",
            "Positions you as an end-to-end technical systems consultant (not just a marketer).",
            "1. Copy text from Column F\n2. Post on Thursday Week 2 at 9:00 AM EST\n3. Offer quick DNS inspection to contractors in comments"
        ],
        # Post 5
        [
            "SCHEDULED POST #5",
            "Week 3: Tuesday 8:15 AM EST",
            "Google Map Pack & Review Deficit",
            "SCHEDULED",
            "Having a 4.8-star rating means nothing on Google Maps if you only have 28 reviews.",
            "Having a 4.8-star rating means nothing on Google Maps if you only have 28 reviews.\n\n"
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
            "Text Post with bullet points",
            "Educates contractors on review velocity automation.",
            "1. Copy text from Column F\n2. Post on Tuesday Week 3 at 8:15 AM EST"
        ],
        # Post 6
        [
            "SCHEDULED POST #6",
            "Week 3: Thursday 9:00 AM EST",
            "Inside a 4-Pillar Executive Audit",
            "SCHEDULED",
            "What actually happens during an institutional 4-Pillar Operational Diagnostic?",
            "What actually happens during an institutional 4-Pillar Operational Diagnostic?\n\n"
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
            "Directs to Featured Section PDF Carousel",
            "Direct funnel to profile Featured Section document carousel; validates diagnostic rigor.",
            "1. Copy text from Column F\n2. Post on Thursday Week 3 at 9:00 AM EST\n3. Remind commenters to check Featured section"
        ],
        # Post 7
        [
            "SCHEDULED POST #7",
            "Week 4: Tuesday 8:15 AM EST",
            "Weather Spikes & Dispatch Volatility",
            "SCHEDULED",
            "How winter freeze warnings and 100°F summer heatwaves expose contractor dispatch bottlenecks.",
            "How winter freeze warnings and 100°F summer heatwaves expose contractor dispatch bottlenecks.\n\n"
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
            "Text Post",
            "Generates urgency around seasonal weather events and triage automation.",
            "1. Copy text from Column F\n2. Post on Tuesday Week 4 at 8:15 AM EST"
        ],
        # Post 8
        [
            "SCHEDULED POST #8",
            "Week 4: Thursday 9:00 AM EST",
            "Operational Architecture vs Lead Gen",
            "SCHEDULED",
            "You don't have a lead generation problem. You have a lead leakage problem.",
            "You don't have a lead generation problem. You have a lead leakage problem.\n\n"
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
            "Direct CTA to DM or 15-Min Discovery Link",
            "Direct conversion post driving inbound DMs and discovery call bookings.",
            "1. Copy text from Column F\n2. Post on Thursday Week 4 at 9:00 AM EST\n3. Reply to DMs immediately with 15-minute booking link"
        ]
    ]

    all_rows = [headers] + featured_rows + [["---", "---", "---", "---", "---", "---", "---", "---", "---"]] + post_rows

    # 3. Write data to the sheet
    target_range = f"'{tab_name}'!A1:I{len(all_rows)}"
    print(f"Writing {len(all_rows)} rows to {target_range}...")
    update_range(sheet_id, target_range, all_rows, token)
    print("Values written successfully.")

    # 4. Apply Sheet Formatting (Header styling, column widths, text wrapping, borders, freeze row)
    format_requests = [
        # Row 1 (Main Header): Dark Navy Background, Bold White Text, Center alignment
        {
            "repeatCell": {
                "range": {
                    "sheetId": new_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": len(headers)
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {
                            "red": 0.08,
                            "green": 0.15,
                            "blue": 0.28
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
                    "sheetId": new_sheet_id,
                    "gridProperties": {
                        "frozenRowCount": 1
                    }
                },
                "fields": "gridProperties.frozenRowCount"
            }
        },
        # Row Height for Header
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": new_sheet_id,
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
        # Wrap text and set font size for all data cells
        {
            "repeatCell": {
                "range": {
                    "sheetId": new_sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(all_rows),
                    "startColumnIndex": 0,
                    "endColumnIndex": len(headers)
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
        # Center align Schedule (Col 1) and Status (Col 3)
        {
            "repeatCell": {
                "range": {
                    "sheetId": new_sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(all_rows),
                    "startColumnIndex": 1,
                    "endColumnIndex": 2
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
                    "sheetId": new_sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(all_rows),
                    "startColumnIndex": 3,
                    "endColumnIndex": 4
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
        # Bold text for Category (Col 0)
        {
            "repeatCell": {
                "range": {
                    "sheetId": new_sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(all_rows),
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
        }
    ]

    # Column Widths
    # Col 0 (Category): 190px
    # Col 1 (Schedule): 160px
    # Col 2 (Focus): 210px
    # Col 3 (Status): 120px
    # Col 4 (Headline / Hook): 240px
    # Col 5 (Copy): 520px
    # Col 6 (Asset / Path): 250px
    # Col 7 (Goal / CTA): 190px
    # Col 8 (Instructions): 250px
    column_widths = [190, 160, 210, 120, 240, 520, 250, 190, 250]
    for col_idx, width in enumerate(column_widths):
        format_requests.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": new_sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": col_idx,
                    "endIndex": col_idx + 1
                },
                "properties": {
                    "pixelSize": width
                },
                "fields": "pixelSize"
            }
        })

    # Execute formatting
    print("Applying styling, column widths, text wrapping, and frozen row...")
    batch_update_spreadsheet(sheet_id, format_requests, token)
    print("Formatting applied successfully.")

    print(f"\nSUCCESS! Tab '{tab_name}' populated and styled at:")
    print(f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid={new_sheet_id}")

if __name__ == "__main__":
    main()
