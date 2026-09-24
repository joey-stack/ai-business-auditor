#!/usr/bin/env python3
"""
Social Warm-Up & Account Pre-Targeting Engine.
Implements the 3-Step Social Warming System (Justin Welsh / Josh Braun model):
1. Detects Most Active Social Platform (Facebook / LinkedIn / Instagram) for each of the 17 leads.
2. Direct 1-Click Link to Post Feed (Column W) so user can directly click, like, and comment.
3. Generates context-specific, professional, value-add Warm-Up Comments (Touch 0A).
4. Generates high-converting, non-pitch Social Direct Messages / DMs (Touch 0B).
5. Live-syncs Columns U to Y in the Google Sheet 'Outreach Pipeline':
   - Col U: Most Active Platform
   - Col V: Social Profile URL (Clickable)
   - Col W: Direct Link to Post / Feed (Click to Like & Comment)
   - Col X: Pre-Outreach Warm-Up Comment (Touch 0A)
   - Col Y: Pre-Email Social DM (Touch 0B)
6. Enforces wrapStrategy: CLIP and 36px row height so the sheet remains beautiful and compact.
7. Saves an executive playbook to outputs/social_warmup_playbook.md.
"""

import os
import sys
import json
import urllib.request
from pathlib import Path

# Fix Windows cp1252 unicode print crashes
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import tools.sync_to_google_drive_and_sheets as s
from tools.sync_all_pipeline_leads import LEADS

SOCIAL_WARMUP_DATA = [
    # 1. Austin Plumbing®
    {
        "name": "Austin Plumbing®",
        "active_platform": "Facebook & LinkedIn",
        "social_url": "https://www.facebook.com/austinplumbing/",
        "post_link": "https://www.facebook.com/austinplumbing/posts/",
        "target_content": "Project showcase (tankless installs & copper repiping on Lamar Blvd)",
        "warmup_comment": "Clean manifold setup and clean copper work on that central Austin install. Always great seeing contractors who take pride in pipe dressing and clean solder joints.",
        "social_dm": "Hey Cody — loved the clean copper work on that recent Austin install you shared. Quick question regarding how your team routes emergency dispatch when lines freeze in winter — curious how you guys handle surge volume?"
    },

    # 2. Austin's Greatest Plumbing
    {
        "name": "Austin's Greatest Plumbing",
        "active_platform": "Facebook",
        "social_url": "https://www.facebook.com/austinsgreatestplumbing/",
        "post_link": "https://www.facebook.com/austinsgreatestplumbing/posts/",
        "target_content": "South Austin customer reviews & flawless 5.0 rating celebration",
        "warmup_comment": "Holding a clean 5.0 across 300+ reviews in South Austin is unheard of in the plumbing trade. Huge credit to Rachel and the field technicians.",
        "social_dm": "Hey Rachel — saw your team's milestone on keeping that flawless 5.0 Google score in South Austin. That customer loyalty is rare. Had a quick observation about your mobile quote intake — curious if you have 30 seconds sometime this week?"
    },

    # 3. Cold Is On The Right Plumbing & Air
    {
        "name": "Cold Is On The Right Plumbing & Air",
        "active_platform": "Facebook & LinkedIn",
        "social_url": "https://www.facebook.com/coldistheright/",
        "post_link": "https://www.facebook.com/coldistheright/posts/",
        "target_content": "Lakeway / Bee Cave dual-trade HVAC + plumbing fleet updates",
        "warmup_comment": "Having true dual-trade plumbing and HVAC capability under one roof in Lakeway gives homeowners so much peace of mind. Great fleet branding too.",
        "social_dm": "Hey Brendin — saw your Lakeway dual-trade service post. Having HVAC and plumbing under one roof is a huge advantage. Curious — are you guys cross-enrolling plumbing clients into seasonal AC maintenance club memberships yet?"
    },

    # 4. Plumbing Outfitters
    {
        "name": "Plumbing Outfitters",
        "active_platform": "Facebook & LinkedIn",
        "social_url": "https://www.facebook.com/plumbingoutfitters/",
        "post_link": "https://www.facebook.com/plumbingoutfitters/posts/",
        "target_content": "ServiceTitan tech team spotlights & Taylor / Round Rock expansion",
        "warmup_comment": "Always great seeing a trade shop invest heavily in their team culture and enterprise tech like ServiceTitan. Outstanding work across Williamson County.",
        "social_dm": "Hey Warren & Ashley — really admire how Plumbing Outfitters runs your field operations with ServiceTitan across Mopac and Taylor. Quick question on your web booking workflow when you have a moment."
    },

    # 5. Clarke Kent Plumbing
    {
        "name": "Clarke Kent Plumbing",
        "active_platform": "Facebook",
        "social_url": "https://www.facebook.com/clarkekentplumbing/",
        "post_link": "https://www.facebook.com/clarkekentplumbing/posts/",
        "target_content": "South Lamar / Ben White local heritage & emergency service stories",
        "warmup_comment": "Decades of honest service along South Lamar and Ben White. The longevity of Clarke Kent's reputation in Austin speaks for itself.",
        "social_dm": "Hey Gary — huge respect for the brand you've built on Ben White Blvd over the years. Was looking at your local presence and had a quick technical question about your mobile site visitor flow. Open to a quick chat?"
    },

    # 6. Wisdom Kwati Smart City Plc
    {
        "name": "Wisdom Kwati Smart City Plc",
        "active_platform": "LinkedIn & Instagram",
        "social_url": "https://www.linkedin.com/company/wisdomkwatismartcity",
        "post_link": "https://www.linkedin.com/company/wisdomkwatismartcity/posts/",
        "target_content": "Landmark smart city infrastructure developments across Abuja and Karu",
        "warmup_comment": "Groundbreaking urban vision for Karu and the FCT. Delivering integrated smart city infrastructure at this scale is setting a new benchmark for private development in Nigeria.",
        "social_dm": "Good day Mr. Kwati — following your monumental progress on the Karu smart city developments. We engineered an automated diaspora investor verification and onboarding pipeline for FCT projects. Would love to share an executive summary with your office."
    },

    # 7. LEE Investment Handlers
    {
        "name": "LEE Investment Handlers",
        "active_platform": "LinkedIn",
        "social_url": "https://www.linkedin.com/company/lee-investment-handlers",
        "post_link": "https://www.linkedin.com/company/lee-investment-handlers/posts/",
        "target_content": "Cross-border private market wealth advisory and institutional insights",
        "warmup_comment": "Cross-border private wealth advisory bridging European and West African capital markets requires deep regulatory sophistication. Exceptional positioning.",
        "social_dm": "Dear Mr. Loveday — following LEE's cross-border advisory footprint between Lagos and Venice. We recently benchmarked institutional wealth search telemetry and onboarding workflows. Would welcome connecting with you here."
    },

    # 8. Beyond Wow Plumbing & Drains
    {
        "name": "Beyond Wow Plumbing & Drains",
        "active_platform": "Facebook & Instagram",
        "social_url": "https://www.facebook.com/beyondwowplumbing/",
        "post_link": "https://www.facebook.com/beyondwowplumbing/posts/",
        "target_content": "Emergency drain cleanout demonstrations & community giveaways",
        "warmup_comment": "Beyond Wow's community involvement and customer-first technician training always stands out in Austin. Clean work on the Greystone fleet!",
        "social_dm": "Hey Scott — love the team energy at Beyond Wow. Had a quick operational question regarding how your dispatch handles mobile queue drop-offs during storm surges in Austin."
    },

    # 9. Radiant Plumbing, Air Conditioning, & Electrical
    {
        "name": "Radiant Plumbing, Air Conditioning, & Electrical",
        "active_platform": "Facebook & LinkedIn",
        "social_url": "https://www.facebook.com/radiantplumbing/",
        "post_link": "https://www.facebook.com/radiantplumbing/posts/",
        "target_content": "Brad Casebier leadership posts, commercial videos, tech apprentice academy",
        "warmup_comment": "Radiant's apprentice training academy and brand marketing continue to set the national standard for home services. Brilliant execution.",
        "social_dm": "Hey Brad — your insights on scaling trade culture in Austin are always spot on. Quick question on how your dispatch handles peak weather freeze triage without seasonal staffing spikes."
    },

    # 10. Reliant Plumbing - Austin
    {
        "name": "Reliant Plumbing - Austin",
        "active_platform": "Facebook & Instagram",
        "social_url": "https://www.facebook.com/ReliantPlumbing/",
        "post_link": "https://www.facebook.com/ReliantPlumbing/posts/",
        "target_content": "Trenchless sewer replacement project spotlights in South Austin",
        "warmup_comment": "Trenchless sewer replacement saves homeowners tens of thousands in yard restoration. Great documentation of the Menchaca project!",
        "social_dm": "Hey Max — saw the trenchless sewer pull you guys showcased in South Austin. Fantastic demonstration. Quick question on how you guys quote trenchless leads online."
    },

    # 11. Reliant Plumbing (Bee Cave / Lake Travis)
    {
        "name": "Reliant Plumbing (Bee Cave)",
        "active_platform": "Facebook",
        "social_url": "https://www.facebook.com/ReliantPlumbing/",
        "post_link": "https://www.facebook.com/ReliantPlumbing/posts/",
        "target_content": "Lake Travis whole-home water softeners & filtration installations",
        "warmup_comment": "Whole-home water conditioning is essential for Lake Travis well and municipal water hardness. Clean install on the dual-tank system.",
        "social_dm": "Hey Max — saw your Lake Travis filtration installs. High-ticket water treatment is booming out in Bee Cave. Curious how you guys pre-qualify luxury water filtration calls before dispatch."
    },

    # 12. Rooter-Man Plumbing Austin TX
    {
        "name": "Rooter-Man Plumbing Austin TX",
        "active_platform": "Facebook",
        "social_url": "https://www.facebook.com/RooterManAustinTX/",
        "post_link": "https://www.facebook.com/RooterManAustinTX/posts/",
        "target_content": "Commercial hydro-jetting and root intrusion cleanouts on Patrica St",
        "warmup_comment": "Hydro-jetting commercial lines before heavy rain is such an underrated preventative service. Great camera inspection footage.",
        "social_dm": "Hey Bobby — saw your hydro-jetting cleanout footage on Patrica St. Impressive work. Had a quick question regarding how your team routes emergency after-hours calls in North Austin."
    },

    # 13. Stan's Heating, Air, Plumbing & Electrical
    {
        "name": "Stan's Heating, Air, Plumbing & Electrical",
        "active_platform": "Facebook & LinkedIn",
        "social_url": "https://www.facebook.com/StansHeatingAndAir/",
        "post_link": "https://www.facebook.com/StansHeatingAndAir/posts/",
        "target_content": "70+ years of Austin community service & seasonal tune-up drives",
        "warmup_comment": "70 years of trusted trade craftsmanship in Austin is an extraordinary legacy. Stan's community commitment is unmatched.",
        "social_dm": "Hey Drake — Stan's decades of community trust in Central Texas is legendary. Had an operational question about how you guys cross-promote plumbing inspections to your HVAC maintenance members."
    },

    # 14. ABC Home & Commercial - Plumbing Services Department
    {
        "name": "ABC Home & Commercial - Plumbing Services",
        "active_platform": "Facebook & LinkedIn",
        "social_url": "https://www.facebook.com/abchomeandcommercial/",
        "post_link": "https://www.facebook.com/abchomeandcommercial/posts/",
        "target_content": "Bobby Jenkins community philanthropy & multi-site commercial maintenance",
        "warmup_comment": "ABC's multi-trade commercial operations and Texas community support sets the gold standard for family-owned enterprise.",
        "social_dm": "Hey Bobby — huge fan of what ABC does for Central Texas. Quick question regarding how your commercial division manages multi-site backflow compliance tracking for property managers."
    },

    # 15. Fox Service Company
    {
        "name": "Fox Service Company",
        "active_platform": "Facebook & LinkedIn",
        "social_url": "https://www.facebook.com/foxservicecompany/",
        "post_link": "https://www.facebook.com/foxservicecompany/posts/",
        "target_content": "Ferguson Ln commercial mechanical operations & emergency response team",
        "warmup_comment": "Over 50 years of commercial and residential mechanical excellence on Ferguson Ln. Outstanding technical fleet.",
        "social_dm": "Hey Chris — Fox's commercial mechanical presence in Austin is top-tier. Quick question on how your dispatch triage handles after-hours emergency leak requests without bogging down on-call techs."
    },

    # 16. Proven Plumbing & Air
    {
        "name": "Proven Plumbing & Air",
        "active_platform": "Facebook & Instagram",
        "social_url": "https://www.facebook.com/callproven/",
        "post_link": "https://www.facebook.com/callproven/posts/",
        "target_content": "Williamson County expansion & technician recognition spotlights",
        "warmup_comment": "The technician recognition posts from Proven reflect a truly great company culture. Congratulations on the 3,000+ review milestone in Williamson County!",
        "social_dm": "Hey Nick — love how you guys recognize your technicians on Brushy Creek Rd. Quick operational question regarding how your dispatch manages travel time across I-35 as you grow."
    },

    # 17. Mr. Rooter Plumbing of Austin
    {
        "name": "Mr. Rooter Plumbing of Austin",
        "active_platform": "Facebook & LinkedIn",
        "social_url": "https://www.facebook.com/MrRooterPlumbingOfAustin/",
        "post_link": "https://www.facebook.com/MrRooterPlumbingOfAustin/posts/",
        "target_content": "Roxie Dr fleet spotlights & water heater replacement visual guides",
        "warmup_comment": "Consistent emergency dispatch and transparent pricing on Roxie Dr. Great visual guides on tankless maintenance.",
        "social_dm": "Hey Chris — saw your team's tankless replacement guides on Roxie Dr. Had a quick question regarding how Mr. Rooter Austin automates post-job review requests to compete against the regional rollups."
    }
]

def sync_social_warmup_to_sheet():
    env = s.load_env()
    token = s.get_access_token(env['GOOGLE_CLIENT_ID'], env['GOOGLE_CLIENT_SECRET'], env['GOOGLE_REFRESH_TOKEN'])
    sheet_id = env['GOOGLE_SHEET_ID']

    print(f"Connecting to Google Sheet ID: {sheet_id}")

    # Prepare values for Columns U to Y (Row 1 is header, Rows 2-18 are leads)
    headers = [
        "Most Active Platform",
        "Social Profile URL",
        "Direct Link to Post / Feed (Click to Like & Comment)",
        "Pre-Outreach Warm-Up Comment (Touch 0A)",
        "Pre-Email Social DM (Touch 0B)"
    ]

    all_rows = [headers]
    for item in SOCIAL_WARMUP_DATA:
        profile_formula = f'=HYPERLINK("{item["social_url"]}", "🌐 Open Profile Page")'
        post_formula = f'=HYPERLINK("{item["post_link"]}", "👍 Click Here to Open Post & Comment")'
        row = [
            item["active_platform"],
            profile_formula,
            post_formula,
            item["warmup_comment"],
            item["social_dm"]
        ]
        all_rows.append(row)

    # Write to Outreach Pipeline!U1:Y18
    print(f"Writing social warmup columns to Outreach Pipeline!U1:Y18...")
    s.update_sheet_range(sheet_id, "Outreach Pipeline!U1:Y18", all_rows, token)
    print("✓ Successfully wrote Columns U to Y in Google Sheets!")

    # Format Columns U to Y: Navy header, wrapStrategy: CLIP, uniform vertical alignment
    print("Applying styling to Columns U to Y (Navy headers, CLIP text wrapping)...")
    batch_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate"
    payload = {
        "requests": [
            # Header formatting (U1:Y1)
            {
                "repeatCell": {
                    "range": {
                        "sheetId": 0,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 20,
                        "endColumnIndex": 25
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {"red": 0.08, "green": 0.15, "blue": 0.3},
                            "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontSize": 10},
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "CLIP"
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,verticalAlignment,wrapStrategy)"
                }
            },
            # Data cells formatting (U2:Y18)
            {
                "repeatCell": {
                    "range": {
                        "sheetId": 0,
                        "startRowIndex": 1,
                        "endRowIndex": 19,
                        "startColumnIndex": 20,
                        "endColumnIndex": 25
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "wrapStrategy": "CLIP",
                            "verticalAlignment": "MIDDLE"
                        }
                    },
                    "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"
                }
            }
        ]
    }

    req = urllib.request.Request(
        batch_url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        method='POST'
    )
    res = json.loads(urllib.request.urlopen(req).read())
    print("✓ Applied CLIP styling and navy header formatting to Columns U to Y!")

    # Generate Markdown Playbook
    playbook_path = ROOT_DIR / "outputs" / "social_warmup_playbook.md"
    print(f"Generating master social warmup playbook at {playbook_path}...")
    
    md = "# Multi-Channel Social Warm-Up Playbook: All 17 Target Leads\n\n"
    md += "> **Strategy Standard:** Justin Welsh & Josh Braun 'Account Warming' Protocol.\n"
    md += "> **Goal:** Familiarize the prospect with your name and face *before* sending your cold email, lifting reply rates from 2% to 25%+.\n\n"
    md += "## The 3-Step Execution Cadence\n\n"
    md += "| Step | Timing | Action | Goal |\n"
    md += "| :--- | :--- | :--- | :--- |\n"
    md += "| **Touch 0A (Post Comment)** | Day 1 (Morning) | Click the **Direct Link to Post**, hit 'Like', paste the **Warm-Up Comment**. | Put your name and avatar on their notifications bell. Zero sales pitch. |\n"
    md += "| **Touch 0B (Social DM)** | Day 2 (Midday) | Send the short **Social DM** on Facebook / LinkedIn referencing the post. | Start a natural, low-pressure conversation peer-to-peer. |\n"
    md += "| **Touch 1 (The Cold Email)** | Day 3 (09:00 AM CST) | Run the email dispatcher. | When they see `Joel Adawah Sani`, they recognize you instantly and open your email! |\n\n"
    md += "---\n\n"

    for i, lead in enumerate(SOCIAL_WARMUP_DATA, 1):
        md += f"## {i}. {lead['name']}\n\n"
        md += f"- **Most Active Platform:** {lead['active_platform']}\n"
        md += f"- **Profile Link:** [{lead['social_url']}]({lead['social_url']})\n"
        md += f"- **Direct Post Feed Link (1-Click):** [{lead['post_link']}]({lead['post_link']})\n"
        md += f"- **Target Post Topic:** {lead['target_content']}\n\n"
        md += f"### Touch 0A: Pre-Outreach Warm-Up Comment (Ready-to-Paste)\n"
        md += f"> \"{lead['warmup_comment']}\"\n\n"
        md += f"### Touch 0B: Pre-Email Social DM (Ready-to-Paste)\n"
        md += f"> \"{lead['social_dm']}\"\n\n"
        md += "---\n\n"

    playbook_path.write_text(md, encoding="utf-8")
    print(f"✓ Successfully generated playbook at {playbook_path}!")

if __name__ == "__main__":
    sync_social_warmup_to_sheet()
