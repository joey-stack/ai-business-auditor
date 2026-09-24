#!/usr/bin/env python3
"""
Sync Instagram & Facebook Content Calendars to Google Sheets.
1. Creates 'Instagram Content Calendar' tab with 4:5 Carousel breakdowns, captions, audio recommendations, and asset links.
2. Creates 'Facebook Content Calendar' tab with long-form authority posts, discussion prompts, and contractor group targeting.
3. Formats with executive Navy headers (#0F172A), bold white text, frozen rows, and custom column dimensions.
"""

import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

# Fix Windows cp1252 unicode print crashes
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import tools.sync_to_google_drive_and_sheets as s

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

# -------------------------------------------------------------
# INSTAGRAM CALENDAR DATA
# -------------------------------------------------------------
IG_HEADERS = [
    "Post #", "Scheduled Date & Time", "Format / Style", "Content Pillar", 
    "Publish Status", "Cover Hook (Slide 1)", "Slide Breakdown (4:5 Ratio)", 
    "Full Instagram Caption", "Recommended Audio / Search Track", "Target Hashtags", "Asset Folder / Link"
]

IG_POSTS = [
    [
        "Post 01",
        "Day 1: Mon 11:30 AM CST",
        "5-Slide 4:5 Carousel",
        "Speed-to-Lead & Emergency Intake",
        "READY TO PUBLISH",
        "The Homeowner Burst Pipe Test ⏱️",
        "Slide 1: Hook ('A pipe bursts at 9 PM on Friday...')\nSlide 2: 78% of calls go to 1st responder\nSlide 3: Harvard 21x drop stat\nSlide 4: Instant 10-second SMS triage\nSlide 5: CTA (Comment 'DISPATCH')",
        (
            "What happens when a homeowner has a burst pipe at 9:00 PM on a Friday?\n\n"
            "They don't submit a web contact form and wait until Monday morning. They go straight to Google Maps and call the first 3 contractors on the list.\n\n"
            "Whoever picks up or triggers an instant automated text message within 60 seconds wins the $1,200 emergency ticket.\n\n"
            "Most trade operators don't lose revenue because of bad marketing. They lose it because their dispatch goes dark the second their office closes.\n\n"
            "👉 Swipe to see the automated 10-second dispatch architecture.\n\n"
            "Want to install this workflow in your trade business?\n"
            "Comment 'DISPATCH' below and I'll send you our complete 10-Second Dispatch Blueprint PDF for free.\n\n"
            "—\n"
            "Joel Adawah Sani | Systems & Automation Consultant"
        ),
        "\"Chill Day\" — LAKEY INSPIRED (or search 'lakey inspired')",
        "#fieldservices #plumbingcontractor #hvaclife #contractorsofinstagram #automation #smallbusinessgrowth #speedtolead",
        "outputs/tiktok_content/post_01_homeowner_has_a_burst_pipe_at_9_00_pm"
    ],
    [
        "Post 02",
        "Day 3: Wed 12:15 PM CST",
        "5-Slide 4:5 Carousel",
        "Speed-to-Lead & Response Latency",
        "READY TO PUBLISH",
        "The 60-Second Rule on Google Maps ⏱️",
        "Slide 1: The 60-Second Rule on Google Maps\nSlide 2: The $14,500/Mo Latency Leak\nSlide 3: HBR 21x Qualification Drop\nSlide 4: The 60-Second Window in Emergency Trades\nSlide 5: Checklist CTA (Comment 'AUDIT')",
        (
            "Whoever responds within 60 seconds captures 78% of emergency service calls on Google Maps. ⏱️\n\n"
            "Look at Slide 2: $14,500 every single month. That’s not marketing spend. That is uncaptured revenue from homeowners who called a local plumbing or HVAC company, got sent to voicemail, and hung up.\n\n"
            "Trade owners aren't ignoring calls because they don't care — they're in the field, under a house, or managing crews.\n\n"
            "Harvard Business Review proved it: waiting just 30 minutes drops qualification rates by 21x. In home services, 60 seconds is the threshold.\n\n"
            "👉 Swipe through for the operational breakdown.\n\n"
            "Want to inspect your own dispatch speed and pipeline friction?\n"
            "Comment 'AUDIT' below and I’ll DM you our free 4-Pillar Systems Diagnostic Checklist.\n\n"
            "—\n"
            "Joel Adawah Sani | Systems & Automation Consultant"
        ),
        "\"Lofi Study\" — FASSounds (or search 'aesthetic' by Tollan Kim)",
        "#businessoperations #fieldservices #plumbinglife #hvaccontractor #hvaclife #contractorsofinstagram #automation #speedtolead #b2bconsulting",
        "outputs/instagram_content/carousel_02_the_60_second_rule"
    ],
    [
        "Post 03",
        "Day 5: Fri 01:00 PM CST",
        "4-Slide 4:5 Carousel",
        "Founder Burnout & Operational Systems",
        "READY TO PUBLISH",
        "How to Protect Your Weekend Dinner 🍷",
        "Slide 1: The 7:30 PM Friday Phone Ring\nSlide 2: The Trade Owner Dilemma (Answer vs Burnout)\nSlide 3: The 3-Node Weekend Triage Protocol\nSlide 4: CTA (Comment 'WEEKEND')",
        (
            "It’s 7:30 PM on a Friday. You’re sitting down to dinner with your family. Your phone rings with an unknown number.\n\n"
            "Every trade contractor knows this dilemma:\n"
            "If you ignore it, you might lose an $8,000 emergency replacement job.\n"
            "If you answer it, you’re back in dispatch mode for the rest of your evening.\n\n"
            "Scaling past $2M doesn't mean working 80-hour weeks. It means building automated triage filters that qualify emergency calls, collect photos, and route jobs to on-call techs without pulling you away from dinner.\n\n"
            "👉 Swipe through for the Weekend Lead Rescue Protocol.\n\n"
            "Comment 'WEEKEND' and I'll send you the exact triage flowchart.\n\n"
            "—\n"
            "Joel Adawah Sani | Systems & Automation Consultant"
        ),
        "\"Better Days\" — LAKEY INSPIRED (or search 'chillhop')",
        "#worklifebalance #founderburnout #contractors #fieldservicemanagement #smallbusinesstips #systemsstrategy",
        "outputs/tiktok_content/post_03_how_to_protect_your_weekend_dinner"
    ],
    [
        "Post 04",
        "Day 8: Mon 11:30 AM CST",
        "5-Slide 4:5 Carousel",
        "Choice Architecture & Field Quoting",
        "READY TO PUBLISH",
        "Stop Sending 1 Flat Quote to Homeowners 📄",
        "Slide 1: Why 1 Flat Quote Kills Close Rates\nSlide 2: The Psychology of Choice vs Ultimatum\nSlide 3: The 3-Tier Architecture (Standard/Preferred/Premium)\nSlide 4: The Decoy Effect in Trade Pricing\nSlide 5: CTA (Comment 'TIER')",
        (
            "When you send a homeowner a single flat price for a $9,000 HVAC or plumbing install, you force them into a binary choice:\n\n"
            "\"Do I buy from this company, or do I call someone cheaper?\"\n\n"
            "Top-performing field service companies use 3-Tier Choice Architecture:\n"
            "1. Economy (Basic repair/code compliance)\n"
            "2. Preferred (Recommended solution + extended warranty)\n"
            "3. Premium (Whole-home protection + maintenance plan)\n\n"
            "Now the customer's mental question shifts from \"Should I hire them?\" to \"Which tier fits my budget?\"\n\n"
            "Average ticket size increases 24% without generating a single extra lead.\n\n"
            "👉 Swipe to see the field quoting breakdown.\n"
            "Comment 'TIER' to get our quoting template.\n\n"
            "—\n"
            "Joel Adawah Sani | Systems & Automation Consultant"
        ),
        "\"Chill Day\" — LAKEY INSPIRED",
        "#pricingstrategy #fieldservice #salestips #contractorgrowth #hvacpricing #tradesman #consulting",
        "outputs/tiktok_content/post_04_stop_sending_1_flat_quote"
    ],
    [
        "Post 05",
        "Day 10: Wed 12:15 PM CST",
        "5-Slide 4:5 Carousel",
        "Dual-Trade Silos & Cross-Selling",
        "READY TO PUBLISH",
        "The $216,000 Dual-Trade Silo 🛠️",
        "Slide 1: Having Plumbing + HVAC Under One Roof\nSlide 2: Why Cross-Selling Fails in the Field\nSlide 3: The 30-Second Water Heater Inspection\nSlide 4: The Automated Membership Pipeline\nSlide 5: CTA (Comment 'CROSS')",
        (
            "If your business offers both plumbing and HVAC, you have a massive advantage over single-trade shops.\n\n"
            "Yet in almost 80% of companies we audit, these trades operate in complete silos.\n\n"
            "HVAC techs service an AC unit, walk right past an 11-year-old rusted water heater, and say nothing because \"that's plumbing's department.\"\n\n"
            "Techs shouldn't have to be high-pressure salesmen. A simple 3-question digital inspection in your dispatch app automatically triggers an automated email + SMS report to the homeowner.\n\n"
            "Unlocks an extra $18k/month in recurring trade memberships.\n\n"
            "👉 Swipe to see the cross-sell workflow.\n"
            "Comment 'CROSS' to get the inspection checklist.\n\n"
            "—\n"
            "Joel Adawah Sani | Systems & Automation Consultant"
        ),
        "\"Breathe\" — Kupla (or search 'aesthetic lofi')",
        "#dualtrade #plumbingandhvac #fieldoperations #tradesystems #recurringrevenue #contractortips",
        "outputs/tiktok_content/post_07_the_216_000_trade_cross_sell_silo"
    ]
]

# -------------------------------------------------------------
# FACEBOOK CALENDAR DATA
# -------------------------------------------------------------
FB_HEADERS = [
    "Post #", "Scheduled Date & Time", "Format / Style", "Content Pillar", 
    "Publish Status", "Opening Hook (First 2 Lines)", "Full Facebook Post Copy (Ready-to-Paste)", 
    "Attached Visual Asset", "Engagement Question / Discussion Prompt", "Target Contractor Groups & Tags"
]

FB_POSTS = [
    [
        "FB Post 01",
        "Day 1: Mon 08:30 AM CST",
        "Long-Form Case Breakdown + Diagram",
        "Speed-to-Lead & Emergency Triage",
        "READY TO PUBLISH",
        "If a homeowner has a burst pipe at 9:00 PM, they don't wait for your office to open Monday.",
        (
            "If a homeowner in your service area has water gushing from under their sink at 9:00 PM on Friday, they aren't filling out a contact form to wait for a Monday morning callback.\n\n"
            "They pull out their phone, search Google Maps, and call the top 3 listings.\n\n"
            "According to industry dispatch data, 78% of emergency jobs go to whoever answers the phone or responds with an automated 2-way text within 60 seconds.\n\n"
            "Here’s the reality for most independent plumbing & HVAC contractors:\n"
            "You’re either missing those calls and forfeiting $1,200 emergency tickets to your larger private-equity backed competitors, or you’re tethered to your phone 24/7 sacrificing your family dinner.\n\n"
            "The solution isn't hiring an expensive 24/7 call center that knows nothing about your pricing.\n\n"
            "A simple 3-step webhook setup connected to your dispatch software (Jobber, ServiceTitan, or Housecall Pro) can instantly send an automated text message: 'Hi, this is [Company]. We saw your call regarding an emergency repair. What is your street address and is water currently shut off?'\n\n"
            "It engages the lead, confirms emergency dispatch eligibility, and holds the customer while alerting your on-call tech.\n\n"
            "How does your dispatch team handle after-hours inquiries right now? Do you route to voicemail, use an answering service, or take the calls yourself?"
        ),
        "outputs/tiktok_content/post_01_homeowner_has_a_burst_pipe_at_9_00_pm/stills/video_01_scene1_pipe.png",
        "How do you handle weekend dispatch right now? Voicemail, answering service, or phone in hand?",
        "#HVACLife #PlumbersOfFacebook #ContractorTalk #FieldServiceManagement #SmallBusinessOperations"
    ],
    [
        "FB Post 02",
        "Day 3: Wed 08:30 AM CST",
        "Diagnostic Teardown + Stat Infographic",
        "Speed-to-Lead & Response Latency",
        "READY TO PUBLISH",
        "Harvard Business Review tested thousands of inbound leads. Here is what they discovered about response time:",
        (
            "Harvard Business Review published a landmark study analyzing inbound lead response latency:\n\n"
            "Contacting an inbound lead within 5 minutes vs. 30 minutes resulted in a 21x drop in qualification rate.\n\n"
            "In commercial and residential field services, that window isn’t 5 minutes — it’s 60 seconds.\n\n"
            "We recently audited 15 trade contractors in the Austin area. The average response time across web intake forms was 3 hours and 48 minutes.\n\n"
            "By the time the contractor called back, 80% of those homeowners had already signed with another competitor.\n\n"
            "If you’re spending $1,500 to $5,000 a month on Google Local Services Ads or Facebook Ads, but your response time is over 15 minutes, you are essentially buying leads for your competitors.\n\n"
            "Before spending another dollar on lead generation, audit your speed-to-lead pipeline.\n\n"
            "I put together a 4-Pillar Systems Diagnostic Checklist specifically for trade contractors doing $1M–$10M. Drop a comment below if you'd like a copy sent over."
        ),
        "outputs/instagram_content/carousel_02_the_60_second_rule/slide_03_the_hbr_21x_qualification_stat.png",
        "What is the average response time for your web quote forms right now?",
        "#ContractorSuccess #TradeBusiness #BusinessSystems #OperationsExcellence #ServiceContractors"
    ],
    [
        "FB Post 03",
        "Day 5: Fri 08:30 AM CST",
        "Contrarian Founder Perspective",
        "Founder Burnout & Operational Moats",
        "READY TO PUBLISH",
        "Why scaling past $2M in revenue makes most trade founders feel more trapped than when they started:",
        (
            "A lot of trade contractors believe that reaching $2M or $3M in annual revenue will give them freedom.\n\n"
            "Then they hit $2M and realize:\n"
            "- They have more trucks, but smaller profit margins.\n"
            "- They are managing 10 technicians who text them 40 times a day for instructions.\n"
            "- Their phone never stops ringing with customer escalations.\n\n"
            "'You do not rise to the level of your goals. You fall to the level of your systems.' — James Clear.\n\n"
            "When you scale headcount before automating repetitive bottlenecks, you don't scale profit — you just scale chaos.\n\n"
            "High-profit service companies build systems that remove the founder from the daily triage:\n"
            "1. Automated dispatch routing based on technician skill level and job location.\n"
            "2. Instant quote follow-up sequences (Day 2, Day 5, Day 10) so estimates don't die in inboxes.\n"
            "3. Standardized SOPs in your field app so techs don't call the owner for approval on routine pricing.\n\n"
            "What was the hardest transition for you when growing your trade fleet?"
        ),
        "outputs/tiktok_content/post_03_how_to_protect_your_weekend_dinner/stills/video_03_scene1_table.png",
        "What is the biggest operational bottleneck taking up your time this week?",
        "#TradeContractors #ContractorMindset #ScaleSmart #OperationsStrategy #HomeServices"
    ],
    [
        "FB Post 04",
        "Day 8: Mon 08:30 AM CST",
        "Tactical Pricing Breakdown",
        "Choice Architecture & Field Quoting",
        "READY TO PUBLISH",
        "Stop giving customers 1 price. Here is how Choice Architecture adds 20% to average ticket size:",
        (
            "Most trade quotes look like this:\n'Replace 50-gallon gas water heater: $2,850.'\n\n"
            "When a homeowner sees one price, they only have one decision to make: 'Do I want to pay this, or should I get a second quote from another plumber?'\n\n"
            "Look at how automotive dealers or enterprise software companies quote. They never give one option. They use Good / Better / Best choice architecture:\n\n"
            "Tier 1 (Standard): Basic replacement, standard 6-year warranty ($2,850)\n"
            "Tier 2 (Preferred): High-efficiency unit, expansion tank, flood-stop shutoff valve, 10-year warranty ($3,650)\n"
            "Tier 3 (Premium): Tankless continuous supply, whole-home filtration, 12-year warranty, priority emergency dispatch membership ($5,400)\n\n"
            "Over 60% of homeowners choose Tier 2 because people naturally gravitate toward the middle 'safe' choice. Another 15% choose Tier 3.\n\n"
            "You just raised your average job size from $2,850 to $3,400 without selling high pressure.\n\n"
            "Do your technicians present multi-option proposals in the field right now?"
        ),
        "outputs/tiktok_content/post_04_stop_sending_1_flat_quote/stills/video_04_scene1_quote.png",
        "Do you use 3-tier quoting in your business? What's your experience with close rates?",
        "#PlumbingPricing #HVACSales #ContractorTips #FieldService #ServiceTitan"
    ],
    [
        "FB Post 05",
        "Day 10: Wed 08:30 AM CST",
        "Operational Case Study",
        "Review Velocity & Local Reputation",
        "READY TO PUBLISH",
        "How a South Austin plumbing contractor holds a flawless 5.0 rating across 300+ reviews:",
        (
            "In home service trades, your Google Business Profile rating is your primary cash register.\n\n"
            "A company with 300 reviews at 4.9 stars will consistently beat a company with 20 reviews even if the second company spends twice as much on local advertising.\n\n"
            "The mistake most operators make: Telling their techs, 'Remember to ask the customer for a review.'\n\n"
            "Technicians are focused on pipe fittings, wiring, and getting to their next call. They will never consistently remember to ask.\n\n"
            "The companies that scale reviews use an automated post-service webhook:\n"
            "- Step 1: 30 minutes after a job is marked 'Completed' in the dispatch software, the customer receives an automated text: 'Hi [Name], thanks for trusting [Company] today! On a scale of 1 to 5, how did our technician do?'\n"
            "- Step 2: If 4 or 5 stars $\rightarrow$ The system sends a direct 1-click link to Google Maps.\n"
            "- Step 3: If 1 to 3 stars $\rightarrow$ The system routes them to an internal feedback form that alerts the owner immediately to resolve the issue before it ever hits Google.\n\n"
            "Protects your brand while putting review generation on complete autopilot."
        ),
        "outputs/tiktok_content/post_02_the_60_second_rule_on_google_maps/stills/video_02_scene2_dossier.png",
        "How does your business collect Google reviews right now?",
        "#ReputationManagement #GoogleMapsSEO #ContractorGrowth #LocalServices #SmallBusiness"
    ]
]

def main():
    print("--- Connecting to Google Sheets API ---")
    env = s.load_env()
    client_id = env['GOOGLE_CLIENT_ID']
    client_secret = env['GOOGLE_CLIENT_SECRET']
    refresh_token = env['GOOGLE_REFRESH_TOKEN']
    sheet_id = env['GOOGLE_SHEET_ID']

    token = s.get_access_token(client_id, client_secret, refresh_token)
    print("✓ Obtained fresh OAuth access token.")

    # 1. Fetch existing sheets
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        meta = json.loads(resp.read().decode("utf-8"))
    
    existing_sheets = {sh["properties"]["title"]: sh["properties"]["sheetId"] for sh in meta.get("sheets", [])}
    print(f"Existing tabs: {list(existing_sheets.keys())}")

    # Helper to add sheet if needed
    for tab_name in ["Instagram Content Calendar", "Facebook Content Calendar"]:
        if tab_name not in existing_sheets:
            print(f"Creating tab '{tab_name}'...")
            add_req = {"addSheet": {"properties": {"title": tab_name}}}
            res = batch_update_spreadsheet(sheet_id, [add_req], token)
            new_id = res["replies"][0]["addSheet"]["properties"]["sheetId"]
            existing_sheets[tab_name] = new_id
            print(f"✓ Created tab '{tab_name}' (ID: {new_id})")

    # 2. Populate Instagram Content Calendar
    print("\n--- Syncing Instagram Content Calendar ---")
    ig_data = [IG_HEADERS] + IG_POSTS
    s.update_sheet_range(sheet_id, f"'Instagram Content Calendar'!A1:K{len(ig_data)}", ig_data, token)
    print(f"✓ Wrote {len(ig_data)} rows to 'Instagram Content Calendar'")

    # 3. Populate Facebook Content Calendar
    print("\n--- Syncing Facebook Content Calendar ---")
    fb_data = [FB_HEADERS] + FB_POSTS
    s.update_sheet_range(sheet_id, f"'Facebook Content Calendar'!A1:J{len(fb_data)}", fb_data, token)
    print(f"✓ Wrote {len(fb_data)} rows to 'Facebook Content Calendar'")

    # 4. Apply styling (Executive Navy #0F172A, bold white text, frozen header, auto dimensions)
    print("\n--- Applying Executive Styling & Dimensions ---")
    requests = []
    
    for tab_name, col_count, row_count in [("Instagram Content Calendar", 11, len(ig_data)), ("Facebook Content Calendar", 10, len(fb_data))]:
        sh_id = existing_sheets[tab_name]
        
        # Freeze 1 row
        requests.append({
            "updateSheetProperties": {
                "properties": {"sheetId": sh_id, "gridProperties": {"frozenRowCount": 1}},
                "fields": "gridProperties.frozenRowCount"
            }
        })
        
        # Header formatting (#0F172A navy, white text, bold)
        requests.append({
            "repeatCell": {
                "range": {"sheetId": sh_id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": col_count},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 15/255, "green": 23/255, "blue": 42/255},
                        "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1}, "bold": True, "fontSize": 10},
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
            }
        })

        # Body formatting (clip wrap, vertical middle)
        requests.append({
            "repeatCell": {
                "range": {"sheetId": sh_id, "startRowIndex": 1, "endRowIndex": row_count, "startColumnIndex": 0, "endColumnIndex": col_count},
                "cell": {
                    "userEnteredFormat": {
                        "wrapStrategy": "CLIP",
                        "verticalAlignment": "MIDDLE",
                        "textFormat": {"fontSize": 10}
                    }
                },
                "fields": "userEnteredFormat(wrapStrategy,verticalAlignment,textFormat)"
            }
        })

        # Set row heights: Row 1 = 40px, Data rows = 36px
        requests.append({
            "updateDimensionProperties": {
                "range": {"sheetId": sh_id, "dimension": "ROWS", "startIndex": 0, "endIndex": 1},
                "properties": {"pixelSize": 40},
                "fields": "pixelSize"
            }
        })
        requests.append({
            "updateDimensionProperties": {
                "range": {"sheetId": sh_id, "dimension": "ROWS", "startIndex": 1, "endIndex": row_count},
                "properties": {"pixelSize": 36},
                "fields": "pixelSize"
            }
        })

    batch_update_spreadsheet(sheet_id, requests, token)
    print("✓ Successfully formatted Instagram & Facebook tabs!")
    print(f"\nSpreadsheet Link: https://docs.google.com/spreadsheets/d/{sheet_id}/edit")

if __name__ == "__main__":
    main()
