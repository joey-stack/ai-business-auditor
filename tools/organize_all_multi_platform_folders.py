#!/usr/bin/env python3
"""
Multi-Platform Content Organizer:
Generates dedicated, structured folders for:
1. outputs/instagram_content/ (4:5 Carousels + Captions + Audio Recommendations)
2. outputs/facebook_content/ (Long-form Posts + Discussion Prompts + Visual Assets)
3. outputs/whatsapp_content/ (WhatsApp Status Images + Formatted Broadcast Copy with *bold* syntax)
"""

import os
import sys
import shutil
from pathlib import Path
from PIL import Image

# Fix Windows cp1252 unicode print crashes
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = ROOT_DIR / "outputs"
TIKTOK_DIR = OUTPUTS_DIR / "tiktok_content"
LEAD_MAGNETS_DIR = OUTPUTS_DIR / "lead_magnets"

IG_DIR = OUTPUTS_DIR / "instagram_content"
FB_DIR = OUTPUTS_DIR / "facebook_content"
WA_DIR = OUTPUTS_DIR / "whatsapp_content"

for d in [IG_DIR, FB_DIR, WA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. ORGANIZE INSTAGRAM CONTENT (4:5 CAROUSELS)
# -------------------------------------------------------------
print("\n--- Organizing Instagram Content Folders ---")

IG_POSTS_DATA = [
    {
        "folder": "post_01_the_burst_pipe_test",
        "title": "The Homeowner Burst Pipe Test ⏱️",
        "pillar": "Speed-to-Lead & Emergency Intake",
        "audio": "\"Chill Day\" — LAKEY INSPIRED (or search 'lakey inspired')",
        "hashtags": "#fieldservices #plumbingcontractor #hvaclife #contractorsofinstagram #automation #smallbusinessgrowth #speedtolead",
        "stills_src": TIKTOK_DIR / "post_01_homeowner_has_a_burst_pipe_at_9_00_pm" / "stills",
        "lead_magnet": "10_second_dispatch_workflow_blueprint.pdf",
        "caption": """What happens when a homeowner has a burst pipe at 9:00 PM on a Friday?

They don't submit a web contact form and wait until Monday morning. They go straight to Google Maps and call the first 3 contractors on the list.

Whoever picks up or triggers an instant automated text message within 60 seconds wins the $1,200 emergency ticket.

Most trade operators don't lose revenue because of bad marketing. They lose it because their dispatch goes dark the second their office closes.

👉 Swipe to see the automated 10-second dispatch architecture.

Want to install this workflow in your trade business?
Comment 'DISPATCH' below and I'll send you our complete 10-Second Dispatch Blueprint PDF for free.

—
Joel Adawah Sani | Systems & Automation Consultant"""
    },
    {
        "folder": "post_02_the_60_second_rule",
        "title": "The 60-Second Rule on Google Maps ⏱️",
        "pillar": "Speed-to-Lead & Response Latency",
        "audio": "\"Lofi Study\" — FASSounds (or search 'aesthetic' by Tollan Kim)",
        "hashtags": "#businessoperations #fieldservices #plumbinglife #hvaccontractor #hvaclife #contractorsofinstagram #automation #speedtolead #b2bconsulting",
        "stills_src": TIKTOK_DIR / "post_02_the_60_second_rule_on_google_maps" / "stills",
        "lead_magnet": "4_pillar_systems_diagnostic_checklist.pdf",
        "caption": """Whoever responds within 60 seconds captures 78% of emergency service calls on Google Maps. ⏱️

Look at Slide 2: $14,500 every single month. That’s not marketing spend. That is uncaptured revenue from homeowners who called a local plumbing or HVAC company, got sent to voicemail, and hung up.

Trade owners aren't ignoring calls because they don't care — they're in the field, under a house, or managing crews. 

Harvard Business Review proved it: waiting just 30 minutes drops qualification rates by 21x. In home services, 60 seconds is the threshold.

If your dispatch isn't automated to trigger instant two-way SMS the second a call or quote request drops in, you're literally paying Google to generate leads for your competitors.

👉 Swipe through for the operational breakdown.

Want to inspect your own dispatch speed and pipeline friction?
Comment 'AUDIT' below and I’ll DM you our free 4-Pillar Systems Diagnostic Checklist.

—
Joel Adawah Sani | Systems & Automation Consultant"""
    },
    {
        "folder": "post_03_protect_weekend_dinner",
        "title": "How to Protect Your Weekend Dinner 🍷",
        "pillar": "Founder Burnout & Operational Systems",
        "audio": "\"Better Days\" — LAKEY INSPIRED (or search 'chillhop')",
        "hashtags": "#worklifebalance #founderburnout #contractors #fieldservicemanagement #smallbusinesstips #systemsstrategy",
        "stills_src": TIKTOK_DIR / "post_03_how_to_protect_your_weekend_dinner" / "stills",
        "lead_magnet": "weekend_protection_blueprint.pdf",
        "caption": """It’s 7:30 PM on a Friday. You’re sitting down to dinner with your family. Your phone rings with an unknown number.

Every trade contractor knows this dilemma:
If you ignore it, you might lose an $8,000 emergency replacement job.
If you answer it, you’re back in dispatch mode for the rest of your evening.

Scaling past $2M doesn't mean working 80-hour weeks. It means building automated triage filters that qualify emergency calls, collect photos, and route jobs to on-call techs without pulling you away from dinner.

👉 Swipe through for the Weekend Lead Rescue Protocol.

Comment 'WEEKEND' and I'll send you the exact triage flowchart.

—
Joel Adawah Sani | Systems & Automation Consultant"""
    },
    {
        "folder": "post_04_stop_sending_1_flat_quote",
        "title": "Stop Sending 1 Flat Quote to Homeowners 📄",
        "pillar": "Choice Architecture & Field Quoting",
        "audio": "\"Chill Day\" — LAKEY INSPIRED",
        "hashtags": "#pricingstrategy #fieldservice #salestips #contractorgrowth #hvacpricing #tradesman #consulting",
        "stills_src": TIKTOK_DIR / "post_04_stop_sending_1_flat_quote" / "stills",
        "lead_magnet": "10_second_dispatch_workflow_blueprint.pdf",
        "caption": """When you send a homeowner a single flat price for a $9,000 HVAC or plumbing install, you force them into a binary choice:

\"Do I buy from this company, or do I call someone cheaper?\"

Top-performing field service companies use 3-Tier Choice Architecture:
1. Economy (Basic repair/code compliance)
2. Preferred (Recommended solution + extended warranty)
3. Premium (Whole-home protection + maintenance plan)

Now the customer's mental question shifts from \"Should I hire them?\" to \"Which tier fits my budget?\"

Average ticket size increases 24% without generating a single extra lead.

👉 Swipe to see the field quoting breakdown.
Comment 'TIER' to get our quoting template.

—
Joel Adawah Sani | Systems & Automation Consultant"""
    },
    {
        "folder": "post_05_the_216k_dual_trade_silo",
        "title": "The $216,000 Dual-Trade Silo 🛠️",
        "pillar": "Dual-Trade Silos & Cross-Selling",
        "audio": "\"Breathe\" — Kupla (or search 'aesthetic lofi')",
        "hashtags": "#dualtrade #plumbingandhvac #fieldoperations #tradesystems #recurringrevenue #contractortips",
        "stills_src": TIKTOK_DIR / "post_07_the_216_000_trade_cross_sell_silo" / "stills",
        "lead_magnet": "4_pillar_systems_diagnostic_checklist.pdf",
        "caption": """If your business offers both plumbing and HVAC, you have a massive advantage over single-trade shops.

Yet in almost 80% of companies we audit, these trades operate in complete silos.

HVAC techs service an AC unit, walk right past an 11-year-old rusted water heater, and say nothing because \"that's plumbing's department.\"

Techs shouldn't have to be high-pressure salesmen. A simple 3-question digital inspection in your dispatch app automatically triggers an automated email + SMS report to the homeowner.

Unlocks an extra $18k/month in recurring trade memberships.

👉 Swipe to see the cross-sell workflow.
Comment 'CROSS' to get the inspection checklist.

—
Joel Adawah Sani | Systems & Automation Consultant"""
    }
]

for p in IG_POSTS_DATA:
    folder_path = IG_DIR / p["folder"]
    folder_path.mkdir(parents=True, exist_ok=True)
    slides_folder = folder_path / "slides_4x5"
    slides_folder.mkdir(parents=True, exist_ok=True)

    # Convert and copy stills to 4:5
    if p["stills_src"].exists():
        for still_file in sorted(p["stills_src"].glob("*.png")):
            img = Image.open(still_file)
            w, h = img.size
            if h > 1350:
                crop_top = int((h - 1350) / 2)
                cropped = img.crop((0, crop_top, 1080, crop_top + 1350))
                cropped.save(slides_folder / still_file.name, quality=95)
            else:
                shutil.copyfile(still_file, slides_folder / still_file.name)

    # Copy lead magnet
    lm_path = LEAD_MAGNETS_DIR / p["lead_magnet"]
    if lm_path.exists():
        shutil.copyfile(lm_path, folder_path / p["lead_magnet"])

    # Write post_copy.md
    post_copy_md = f"""# Instagram Carousel: {p['title']}

- **Content Pillar**: {p['pillar']}
- **Format**: 4:5 Portrait Carousel (1080x1350)
- **Slides Folder**: `slides_4x5/`
- **Lead Magnet PDF**: `{p['lead_magnet']}`

---

## 🎵 Recommended Instagram Background Music to Search
Tap **"Add music"** before sharing and search:
👉 **{p['audio']}**

---

## 📝 Full Instagram Caption (Ready to Paste)

```text
{p['caption']}

—
{p['hashtags']}
```
"""
    with open(folder_path / "post_copy.md", "w", encoding="utf-8") as f:
        f.write(post_copy_md)
    print(f"✓ Prepared Instagram folder: {p['folder']}")


# -------------------------------------------------------------
# 2. ORGANIZE FACEBOOK CONTENT (LONG-FORM + GROUPS)
# -------------------------------------------------------------
print("\n--- Organizing Facebook Content Folders ---")

FB_POSTS_DATA = [
    {
        "folder": "post_01_burst_pipe_emergency_triage",
        "title": "If a homeowner has a burst pipe at 9:00 PM...",
        "pillar": "Speed-to-Lead & Emergency Triage",
        "image_src": TIKTOK_DIR / "post_01_homeowner_has_a_burst_pipe_at_9_00_pm" / "stills" / "video_01_scene1_pipe.png",
        "prompt": "How do you handle weekend dispatch right now? Voicemail, answering service, or phone in hand?",
        "lead_magnet": "10_second_dispatch_workflow_blueprint.pdf",
        "copy": """If a homeowner in your service area has water gushing from under their sink at 9:00 PM on Friday, they aren't filling out a contact form to wait for a Monday morning callback.

They pull out their phone, search Google Maps, and call the top 3 listings.

According to industry dispatch data, 78% of emergency jobs go to whoever answers the phone or responds with an automated 2-way text within 60 seconds.

Here’s the reality for most independent plumbing & HVAC contractors:
You’re either missing those calls and forfeiting $1,200 emergency tickets to your larger private-equity backed competitors, or you’re tethered to your phone 24/7 sacrificing your family dinner.

The solution isn't hiring an expensive 24/7 call center that knows nothing about your pricing.

A simple 3-step webhook setup connected to your dispatch software (Jobber, ServiceTitan, or Housecall Pro) can instantly send an automated text message: 
"Hi, this is [Company]. We saw your call regarding an emergency repair. What is your street address and is water currently shut off?"

It engages the lead, confirms emergency dispatch eligibility, and holds the customer while alerting your on-call tech.

How does your dispatch team handle after-hours inquiries right now? Do you route to voicemail, use an answering service, or take the calls yourself?"""
    },
    {
        "folder": "post_02_harvard_response_time_study",
        "title": "Harvard Business Review Response Time Breakdown",
        "pillar": "Speed-to-Lead & Response Latency",
        "image_src": TIKTOK_DIR / "post_02_the_60_second_rule_on_google_maps" / "stills" / "video_02_scene3_hbr21x.png",
        "prompt": "What is the average response time for your web quote forms right now?",
        "lead_magnet": "4_pillar_systems_diagnostic_checklist.pdf",
        "copy": """Harvard Business Review published a landmark study analyzing inbound lead response latency:

Contacting an inbound lead within 5 minutes vs. 30 minutes resulted in a 21x drop in qualification rate.

In commercial and residential field services, that window isn’t 5 minutes — it’s 60 seconds.

We recently audited 15 trade contractors in the Austin area. The average response time across web intake forms was 3 hours and 48 minutes.

By the time the contractor called back, 80% of those homeowners had already signed with another competitor.

If you’re spending $1,500 to $5,000 a month on Google Local Services Ads or Facebook Ads, but your response time is over 15 minutes, you are essentially buying leads for your competitors.

Before spending another dollar on lead generation, audit your speed-to-lead pipeline.

I put together a 4-Pillar Systems Diagnostic Checklist specifically for trade contractors doing $1M–$10M. Drop a comment below if you'd like a copy sent over."""
    },
    {
        "folder": "post_03_founder_headcount_vs_systems",
        "title": "Headcount vs Systems: Why Scaling Beyond $2M Traps Owners",
        "pillar": "Founder Burnout & Operational Moats",
        "image_src": TIKTOK_DIR / "post_03_how_to_protect_your_weekend_dinner" / "stills" / "video_03_scene1_table.png",
        "prompt": "What is the biggest operational bottleneck taking up your time this week?",
        "lead_magnet": "weekend_protection_blueprint.pdf",
        "copy": """A lot of trade contractors believe that reaching $2M or $3M in annual revenue will give them freedom.

Then they hit $2M and realize:
- They have more trucks, but smaller profit margins.
- They are managing 10 technicians who text them 40 times a day for instructions.
- Their phone never stops ringing with customer escalations.

'You do not rise to the level of your goals. You fall to the level of your systems.' — James Clear.

When you scale headcount before automating repetitive bottlenecks, you don't scale profit — you just scale chaos.

High-profit service companies build systems that remove the founder from the daily triage:
1. Automated dispatch routing based on technician skill level and job location.
2. Instant quote follow-up sequences (Day 2, Day 5, Day 10) so estimates don't die in inboxes.
3. Standardized SOPs in your field app so techs don't call the owner for approval on routine pricing.

What was the hardest transition for you when growing your trade fleet?"""
    },
    {
        "folder": "post_04_3_tier_choice_architecture",
        "title": "Stop Giving Homeowners 1 Price (3-Tier Quoting)",
        "pillar": "Choice Architecture & Field Quoting",
        "image_src": TIKTOK_DIR / "post_04_stop_sending_1_flat_quote" / "stills" / "video_04_scene1_quote.png",
        "prompt": "Do you use 3-tier quoting in your business? What's your experience with close rates?",
        "lead_magnet": "10_second_dispatch_workflow_blueprint.pdf",
        "copy": """Most trade quotes look like this:
'Replace 50-gallon gas water heater: $2,850.'

When a homeowner sees one price, they only have one decision to make: 'Do I want to pay this, or should I get a second quote from another plumber?'

Look at how automotive dealers or enterprise software companies quote. They never give one option. They use Good / Better / Best choice architecture:

Tier 1 (Standard): Basic replacement, standard 6-year warranty ($2,850)
Tier 2 (Preferred): High-efficiency unit, expansion tank, flood-stop shutoff valve, 10-year warranty ($3,650)
Tier 3 (Premium): Tankless continuous supply, whole-home filtration, 12-year warranty, priority emergency dispatch membership ($5,400)

Over 60% of homeowners choose Tier 2 because people naturally gravitate toward the middle 'safe' choice. Another 15% choose Tier 3.

You just raised your average job size from $2,850 to $3,400 without selling high pressure.

Do your technicians present multi-option proposals in the field right now?"""
    },
    {
        "folder": "post_05_review_velocity_autopilot",
        "title": "Automated Review Velocity (Protecting 4.9 Stars)",
        "pillar": "Review Velocity & Local Reputation",
        "image_src": TIKTOK_DIR / "post_02_the_60_second_rule_on_google_maps" / "stills" / "video_02_scene2_dossier.png",
        "prompt": "How does your business collect Google reviews right now?",
        "lead_magnet": "4_pillar_systems_diagnostic_checklist.pdf",
        "copy": """In home service trades, your Google Business Profile rating is your primary cash register.

A company with 300 reviews at 4.9 stars will consistently beat a company with 20 reviews even if the second company spends twice as much on local advertising.

The mistake most operators make: Telling their techs, 'Remember to ask the customer for a review.'

Technicians are focused on pipe fittings, wiring, and getting to their next call. They will never consistently remember to ask.

The companies that scale reviews use an automated post-service webhook:
- Step 1: 30 minutes after a job is marked 'Completed' in the dispatch software, the customer receives an automated text: 'Hi [Name], thanks for trusting [Company] today! On a scale of 1 to 5, how did our technician do?'
- Step 2: If 4 or 5 stars -> The system sends a direct 1-click link to Google Maps.
- Step 3: If 1 to 3 stars -> The system routes them to an internal feedback form that alerts the owner immediately to resolve the issue before it ever hits Google.

Protects your brand while putting review generation on complete autopilot."""
    }
]

for p in FB_POSTS_DATA:
    folder_path = FB_DIR / p["folder"]
    folder_path.mkdir(parents=True, exist_ok=True)

    # Copy image
    if p["image_src"].exists():
        shutil.copyfile(p["image_src"], folder_path / "attached_graphic.png")

    # Copy lead magnet
    lm_path = LEAD_MAGNETS_DIR / p["lead_magnet"]
    if lm_path.exists():
        shutil.copyfile(lm_path, folder_path / p["lead_magnet"])

    # Write post_copy.md
    post_copy_md = f"""# Facebook Post: {p['title']}

- **Content Pillar**: {p['pillar']}
- **Attached Image**: `attached_graphic.png`
- **Discussion Prompt**: {p['prompt']}
- **Lead Magnet PDF**: `{p['lead_magnet']}`

---

## 📝 Full Facebook Post Copy (Ready to Paste)

```text
{p['copy']}
```

---

## 👥 Best Contractor Facebook Groups to Share In:
1. **HVAC Contractors Group**
2. **Plumbing & Mechanical Professionals**
3. **Field Service & Trades Network**
4. **ServiceTitan / Jobber Mastermind Groups**
"""
    with open(folder_path / "post_copy.md", "w", encoding="utf-8") as f:
        f.write(post_copy_md)
    print(f"✓ Prepared Facebook folder: {p['folder']}")


# -------------------------------------------------------------
# 3. ORGANIZE WHATSAPP CONTENT (STATUS CARDS + BROADCAST COPY)
# -------------------------------------------------------------
print("\n--- Organizing WhatsApp Content Folders ---")

WA_POSTS_DATA = [
    {
        "folder": "status_01_the_burst_pipe_test",
        "title": "The Burst Pipe Reality Check ⏱️",
        "status_image_src": TIKTOK_DIR / "post_01_homeowner_has_a_burst_pipe_at_9_00_pm" / "stills" / "video_01_scene1_pipe.png",
        "lead_magnet": "10_second_dispatch_workflow_blueprint.pdf",
        "status_caption": "What happens when a homeowner has a burst pipe at 9 PM on Friday? ⏱️ 78% of emergency calls go to the first contractor who responds within 60 seconds. Reply *DISPATCH* to see the automated workflow.",
        "broadcast_message": """*The 9:00 PM Burst Pipe Test ⏱️*

If a homeowner has water gushing across their floor on Friday night, they aren't filling out a contact form to wait for Monday morning.

They call the top 3 contractors on Google Maps.

*78% of emergency tickets go to whoever responds within 60 seconds.*

If your dispatch goes dark after 5 PM, you're forfeiting $1,200 emergency calls to competitors.

I documented the exact 3-step automated instant triage architecture used by top service contractors.

Reply *DISPATCH* and I’ll send you the free PDF blueprint right here on WhatsApp! 📲"""
    },
    {
        "folder": "status_02_the_60_second_rule",
        "title": "The 60-Second Rule on Google Maps ⏱️",
        "status_image_src": TIKTOK_DIR / "post_02_the_60_second_rule_on_google_maps" / "stills" / "video_02_scene3_hbr21x.png",
        "lead_magnet": "4_pillar_systems_diagnostic_checklist.pdf",
        "status_caption": "Harvard tested thousands of leads: Waiting 30 mins drops qualification by 21x. In home services, 60 seconds is the threshold. Reply *AUDIT* for the checklist.",
        "broadcast_message": """*The 60-Second Rule on Google Maps ⏱️*

Harvard Business Review proved it:
Waiting 30 minutes to contact an inbound lead drops your qualification rate by *21 times* compared to responding in 5 minutes.

In emergency trades (plumbing, AC repair, roofing), the window isn't 5 minutes. *It's 60 seconds.*

If you spend money on ads or Google Maps but don't have automated 2-way text triage, you're literally buying leads for your competitors.

Want to inspect your own dispatch speed and pipeline friction?

Reply *AUDIT* and I’ll send you our 4-Pillar Systems Diagnostic Checklist PDF! 📊"""
    },
    {
        "folder": "status_03_protect_weekend_dinner",
        "title": "How to Protect Your Weekend Dinner 🍷",
        "status_image_src": TIKTOK_DIR / "post_03_how_to_protect_your_weekend_dinner" / "stills" / "video_03_scene1_table.png",
        "lead_magnet": "weekend_protection_blueprint.pdf",
        "status_caption": "7:30 PM Friday phone ring. Answer and ruin dinner, or ignore and lose $5k? Build automated triage. Reply *WEEKEND* for the protocol.",
        "broadcast_message": """*Protecting Your Weekend Dinner Without Losing Revenue 🍷*

It’s 7:30 PM on Friday. You’re with family. Your phone rings.

Every trade founder knows this battle:
- Ignore it = Risk losing an $8,000 emergency replacement job.
- Answer it = You’re back in dispatch mode all night.

Scaling your business shouldn't mean sacrificing your life. You can install an automated after-hours triage filter that qualifies emergencies and routes jobs to on-call techs automatically.

Reply *WEEKEND* and I'll send you the Weekend Lead Rescue Protocol flowchart! 🚀"""
    },
    {
        "folder": "status_04_stop_sending_1_flat_quote",
        "title": "Stop Sending 1 Flat Quote 📄",
        "status_image_src": TIKTOK_DIR / "post_04_stop_sending_1_flat_quote" / "stills" / "video_04_scene1_quote.png",
        "lead_magnet": "10_second_dispatch_workflow_blueprint.pdf",
        "status_caption": "Sending 1 flat price forces customers into 'Buy vs Call Someone Cheaper'. 3-Tier quoting raises ticket size by 24%. Reply *TIER* for the template.",
        "broadcast_message": """*The 3-Tier Quoting Secret 📄*

When you send a homeowner a single flat price for a big repair or install, they ask:
_\"Should I hire them, or should I call someone cheaper?\"_

When you give 3 Tiers (Standard, Preferred, Premium), their question shifts to:
_*\"Which option fits my budget best?\"*_

Over 60% of homeowners choose the middle option, boosting average ticket size by 24% with zero pressure.

Reply *TIER* and I'll send you our 3-Tier choice architecture template! 📈"""
    },
    {
        "folder": "status_05_the_dual_trade_silo",
        "title": "The $216k Dual-Trade Silo 🛠️",
        "status_image_src": TIKTOK_DIR / "post_07_the_216_000_trade_cross_sell_silo" / "stills" / "video_07_scene1_trucks.png",
        "lead_magnet": "4_pillar_systems_diagnostic_checklist.pdf",
        "status_caption": "Running both plumbing and HVAC? Don't let techs ignore cross-sells. Automated 30-sec checks add $18k/mo. Reply *CROSS* for the checklist.",
        "broadcast_message": """*The $216,000 Dual-Trade Silo 🛠️*

If your company offers both Plumbing and HVAC, your trades shouldn't operate in isolated silos.

Techs shouldn't be aggressive salespeople. A simple 3-question digital inspection in your dispatch app automatically triggers an automated health report to the homeowner.

Recovers an estimated $18k/month in maintenance memberships.

Reply *CROSS* and I'll send you our digital inspection checklist! 🔧"""
    }
]

for p in WA_POSTS_DATA:
    folder_path = WA_DIR / p["folder"]
    folder_path.mkdir(parents=True, exist_ok=True)

    # Copy 9:16 vertical image for WhatsApp Status
    if p["status_image_src"].exists():
        shutil.copyfile(p["status_image_src"], folder_path / "whatsapp_status_image.png")

    # Copy lead magnet
    lm_path = LEAD_MAGNETS_DIR / p["lead_magnet"]
    if lm_path.exists():
        shutil.copyfile(lm_path, folder_path / p["lead_magnet"])

    # Write post_copy.md
    post_copy_md = f"""# WhatsApp Content: {p['title']}

- **Status Image (9:16 Vertical)**: `whatsapp_status_image.png`
- **Lead Magnet PDF**: `{p['lead_magnet']}`

---

## 📱 WhatsApp Status (Stories)

### Status Image:
Upload `whatsapp_status_image.png` directly to your WhatsApp Status.

### Status Caption (Text Overlay):
```text
{p['status_caption']}
```

---

## 📢 WhatsApp Broadcast / Direct Message Copy

Formatted with WhatsApp bold (`*bold*`) and italic (`_italic_`) markdown for instant copy-pasting:

```text
{p['broadcast_message']}
```
"""
    with open(folder_path / "post_copy.md", "w", encoding="utf-8") as f:
        f.write(post_copy_md)
    print(f"✓ Prepared WhatsApp folder: {p['folder']}")

print("\n==================================================================")
print("SUCCESS: ALL MULTI-PLATFORM FOLDERS ORGANIZED!")
print("1. outputs/instagram_content/")
print("2. outputs/facebook_content/")
print("3. outputs/whatsapp_content/")
print("==================================================================")
