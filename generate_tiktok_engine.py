#!/usr/bin/env python3
"""
Generate complete 60-Day TikTok Content & Video Script Engine for Joel Adawah Sani.
Includes:
- 25 date-mapped teleprompter scripts (Mondays, Wednesdays, Fridays)
- Visual cues, on-screen text overlays, and audio hooks
- Master markdown calendar in outputs/tiktok_content/
- Google Sheets tab synchronization script
"""
import os
import json

VIDEOS = [
    {
        "num": 1,
        "date": "2026-09-28",
        "day_time": "Week 1: Monday 6:45 AM EST",
        "format": "Talking Head / POV",
        "pillar": "Speed-to-Lead & Response Latency",
        "status": "READY TO RECORD",
        "text_hook": "Homeowner has a burst pipe at 9:00 PM 🚨",
        "verbal_hook": "If a homeowner has water pouring through their ceiling at 9:00 PM, do you really think they're filling out your 7-field contact form?",
        "script": (
            "[LOOK DIRECTLY AT CAMERA - LEAN IN]\n"
            "If a homeowner has water pouring through their ceiling at 9:00 PM, do you really think they're filling out your 7-field website contact form?\n\n"
            "[SHAKE HEAD]\n"
            "Not a chance. They pull out their phone, search 'emergency plumber near me', and dial the first 3 contractors on Google Maps.\n\n"
            "[COUNT ON FINGERS: 1, 2, 3]\n"
            "Whoever answers first—or triggers an automated SMS within 60 seconds—wins the $3,500 emergency job. Every single time.\n\n"
            "[HOLD UP HAND]\n"
            "In our systems audits of $2M to $5M trade fleets, we found businesses leaking over $14,000 every single month just from unassisted after-hours call abandonment.\n\n"
            "[LEAN IN CLOSE]\n"
            "You don't need a $4,000-a-month call center. You just need a 10-second automated dispatch triage. Link in bio to see the exact workflow."
        ),
        "visual_cue": "Hold smartphone showing incoming call screen, tap red reject button, look into camera with serious expression.",
        "caption": "Why trade contractors forfeit $14,500/month after 8:00 PM. Speed to lead is operational architecture. 🔧💧 #bluecollar #plumbingcontractor #tradesman #hvacbusiness #contractorsoftiktok",
        "cta": "Check the link in my bio to inspect your fleet's after-hours speed-to-lead workflow."
    },
    {
        "num": 2,
        "date": "2026-09-30",
        "day_time": "Week 1: Wednesday 12:15 PM EST",
        "format": "Green Screen Teardown",
        "pillar": "Speed-to-Lead & Response Latency",
        "status": "READY TO RECORD",
        "text_hook": "The 60-Second Rule on Google Maps ⏱️",
        "verbal_hook": "Whoever responds within 60 seconds captures 78% of local emergency service calls.",
        "script": (
            "[GREEN SCREEN BACKGROUND: APEX AUDIT PAGE SHOWING $14,500 LATENCY LEAK]\n"
            "[POINT TO AUDIT NUMBER ABOVE YOUR SHOULDER]\n"
            "Look at this number right here: $14,500 a month. That is not marketing spend. That is uncaptured revenue from customers who called this plumbing company and hung up because nobody answered.\n\n"
            "[STEP ASIDE - HIGHLIGHT THE STAT]\n"
            "Harvard Business Review tested lead response times across thousands of businesses. If you respond within 5 minutes vs 30 minutes, your qualification rate drops by 21 times.\n\n"
            "[TURN TO CAMERA]\n"
            "In emergency trades like plumbing, HVAC, and roofing, the window isn't 5 minutes. It's 60 seconds. If your trucks aren't automated to reply instantly, you're buying leads for your competitors."
        ),
        "visual_cue": "Green screen displaying Apex Home Services audit deliverable page 2 highlighting latency calculations.",
        "caption": "Harvard proved it: 5 minutes vs 30 minutes is a 21x drop in conversion. In home service trades, 60 seconds is the threshold. #fieldservice #contractor #plumbing #hvaclife #businesssystems",
        "cta": "Comment 'AUDIT' and I'll send you our 4-pillar systems diagnostic checklist."
    },
    {
        "num": 3,
        "date": "2026-10-02",
        "day_time": "Week 1: Friday 4:30 PM EST",
        "format": "Whiteboard / Screen Flow",
        "pillar": "Speed-to-Lead & Response Latency",
        "status": "READY TO RECORD",
        "text_hook": "How to protect your weekend dinner 📱🍲",
        "verbal_hook": "Here is the exact 3-step automation that stops weekend emergency calls from ruining your family dinner.",
        "script": (
            "[DRAW ON WHITEBOARD OR TABLET: 1 -> 2 -> 3]\n"
            "Every contractor I audit tells me the same thing: 'Joel, either my phone rings off the hook at Saturday dinner, or I miss out on thousands in revenue.'\n\n"
            "[POINT TO STEP 1]\n"
            "Step 1: Instant SMS Trigger. If a call is missed after hours, an automated SMS fires within 10 seconds: 'We see you called! Are you experiencing an active water leak or safety hazard?'\n\n"
            "[POINT TO STEP 2]\n"
            "Step 2: Interactive Triage. If they text 'Yes', they get safety shutoff steps and an on-call priority dispatch alert. If 'No', they are queued for Monday 8:00 AM.\n\n"
            "[POINT TO STEP 3]\n"
            "Step 3: Zero Headcount. You capture the $2,500 job automatically without paying an outsourced answering service $3,000 a month."
        ),
        "visual_cue": "Drawing 3 connected boxes on an iPad or physical dry-erase whiteboard showing Call -> Triage -> Dispatch.",
        "caption": "Stop letting after-hours phone calls control your life. Automate the triage, protect your weekend, and capture high-margin revenue. #contractorsoftiktok #trades #plumber #electrician #operations",
        "cta": "Link in bio to schedule a 15-minute diagnostic walkthrough."
    },
    {
        "num": 4,
        "date": "2026-10-05",
        "day_time": "Week 2: Monday 6:45 AM EST",
        "format": "Contrarian Talking Head",
        "pillar": "Choice Architecture & Quoting",
        "status": "READY TO RECORD",
        "text_hook": "Stop sending 1 flat quote ❌📄",
        "verbal_hook": "If you send a homeowner one flat price for a new water heater or AC unit, you are forfeiting 22% of your margin.",
        "script": (
            "[LEAN IN - DIRECT EYE CONTACT]\n"
            "If your technicians are quoting homeowners one single price for an equipment replacement, you are literally giving away 22% of your profit margin every single day.\n\n"
            "[HOLD UP 1 FINGER]\n"
            "When you give a customer one number—say $4,200—the only decision in their brain is: 'Yes or No? Do I pay this guy or call someone else?'\n\n"
            "[HOLD UP 3 FINGERS]\n"
            "When you give them THREE choices—Good, Better, Best—their psychology flips from 'Do I hire this company?' to 'Which tier do I want?'\n\n"
            "[SMILE]\n"
            "Over 60% of homeowners choose the middle option, and 15% choose the highest tier with premium warranties. Stop quoting flat numbers."
        ),
        "visual_cue": "Hold up a single crumpled estimate sheet, throw it aside, then display a clean 3-tier iPad estimate screen.",
        "caption": "Why single-tier estimates kill contractor close rates. Choice architecture flips 'Yes vs No' into 'Which option fits best?' #bluecollar #hvacbusiness #contractor #pricingstrategy #systems",
        "cta": "Follow for more trade business systems teardowns."
    },
    {
        "num": 5,
        "date": "2026-10-07",
        "day_time": "Week 2: Wednesday 12:15 PM EST",
        "format": "Green Screen Teardown",
        "pillar": "Choice Architecture & Quoting",
        "status": "READY TO RECORD",
        "text_hook": "The Decoy Effect in Trade Pricing 📊",
        "verbal_hook": "This one pricing psychology trick increases average ticket size by $1,200 on every installation.",
        "script": (
            "[GREEN SCREEN: 3-TIER PRICING MATRIX FROM DELOITTE ROADMAP]\n"
            "[POINT TO TIER 1]\n"
            "Tier 1 is the Base Model: $3,800. Basic unit, standard 1-year labor warranty. It anchors the price floor.\n\n"
            "[POINT TO TIER 2 - TAP THE SCREEN]\n"
            "Tier 2 is the Recommended System: $4,900. High efficiency, surge protector, 5-year parts and labor, plus 1 year of maintenance. It is designed to be the no-brainer choice.\n\n"
            "[POINT TO TIER 3]\n"
            "Tier 3 is the Premium Armor: $6,800. Top-tier inverter, 10-year complete warranty, 24/7 priority dispatch queue.\n\n"
            "[STEP IN]\n"
            "Tier 3 makes Tier 2 feel like an incredible deal. We installed this in a 15-van plumbing fleet and their average ticket jumped 22% in 30 days."
        ),
        "visual_cue": "Green screen pointing at Good/Better/Best table showing ticket lift from Apex Home Services audit.",
        "caption": "Choice architecture isn't manipulative—it gives customers autonomy while protecting your margin. #fieldservice #plumber #hvac #contractorsoftiktok #tradesman",
        "cta": "Download our Good/Better/Best template at the link in bio."
    },
    {
        "num": 6,
        "date": "2026-10-09",
        "day_time": "Week 2: Friday 4:30 PM EST",
        "format": "Scenario / POV",
        "pillar": "Choice Architecture & Quoting",
        "status": "READY TO RECORD",
        "text_hook": "Why customers ghost your $15k bids 👻",
        "verbal_hook": "Ever send a $15,000 commercial quote and the customer completely vanishes? Here's why that happens.",
        "script": (
            "[ACT OUT POV: SITTING AT DESK LOOKING AT INBOX]\n"
            "'Hey Joel, I sent the quote on Tuesday, followed up Thursday, and they completely ghosted me. What happened?'\n\n"
            "[LOOK AT CAMERA]\n"
            "Here's what happened: You sent a single static PDF attachment with zero payment terms, no financing options, and no expiration date.\n\n"
            "[LEAN IN]\n"
            "High-ticket commercial clients don't buy from confusing PDFs. They buy from interactive approval portals where they can click 'Approve with 12-Month Financing' right on their phone.\n\n"
            "[NOD]\n"
            "If your quote requires them to print, sign, scan, and email it back, you're adding 3 days of friction. In trades, friction equals lost jobs."
        ),
        "visual_cue": "Hold printed paper quote, try to sign it with a broken pen, look frustrated, then tap iPhone screen to approve in 1 second.",
        "caption": "Why PDFs get ghosted. The easier you make it for a customer to approve a quote, the higher your close rate. #contractor #commercialplumbing #hvaclife #businessoperations #salestips",
        "cta": "Link in bio to audit your quoting and dispatch workflow."
    },
    {
        "num": 7,
        "date": "2026-10-12",
        "day_time": "Week 3: Monday 6:45 AM EST",
        "format": "Green Screen Teardown",
        "pillar": "Dual-Trade Cross-Sell Silos",
        "status": "READY TO RECORD",
        "text_hook": "The $216,000 Trade Cross-Sell Silo 💰",
        "verbal_hook": "If your company does both HVAC and Plumbing, your technicians are leaving $18,000 in your customers' basements every single month.",
        "script": (
            "[GREEN SCREEN: SUMMIT MECHANICAL AUDIT DELIVERABLE - CROSS-SELL SECTION]\n"
            "[POINT TO THE $216,000 ANNUAL LEAKAGE FIGURE]\n"
            "This is from an institutional diagnostic we just completed for an 18-van mechanical contractor in Texas.\n\n"
            "[LOOK AT CAMERA]\n"
            "They have 10 HVAC trucks and 8 plumbing trucks. But their software systems don't talk to each other. When the HVAC tech is servicing an AC unit in the basement, he literally walks right past a 14-year-old, rusting water heater.\n\n"
            "[SHAKE HEAD]\n"
            "Does he inspect it? No. Does he log it? No. He finishes the AC tune-up and drives away.\n\n"
            "[STEP FORWARD]\n"
            "Two weeks later, that water heater bursts, and the homeowner calls a different plumbing company from Google. That is $216,000 in lost revenue walking out your door."
        ),
        "visual_cue": "Green screen showing Summit Mechanical audit deliverable page 3 (cross-sell analysis).",
        "caption": "Why dual-trade contractors stay stuck at $3M. If your HVAC and plumbing dispatchers aren't cross-triggering inspections, you are leaking cash. #dualtrade #mechanicalcontractor #hvac #plumbing",
        "cta": "Inspect your trade fleet's operational leakage—link in bio."
    },
    {
        "num": 8,
        "date": "2026-10-14",
        "day_time": "Week 3: Wednesday 12:15 PM EST",
        "format": "Talking Head / Tablet",
        "pillar": "Dual-Trade Cross-Sell Silos",
        "status": "READY TO RECORD",
        "text_hook": "The 30-Second Water Heater Check 🔍",
        "verbal_hook": "Teach your AC technicians this 30-second inspection habit and watch your plumbing revenue jump 30%.",
        "script": (
            "[HOLD UP TABLET WITH TECH CHECKLIST]\n"
            "Never ask your field technicians to be aggressive salespeople. They hate it, and customers hate it.\n\n"
            "[SHOW SCREEN]\n"
            "Instead, give them a mandatory 2-photo checklist inside your mobile dispatch app whenever they complete an HVAC maintenance call:\n\n"
            "[COUNT 1]\n"
            "Photo 1: Water heater manufacturer serial plate (logs the age automatically).\n"
            "[COUNT 2]\n"
            "Photo 2: Main shutoff valve condition.\n\n"
            "[LOOK AT CAMERA]\n"
            "If the water heater is over 10 years old, your CRM automatically triggers a preventative replacement offer to the homeowner the next morning from the office.\n\n"
            "Zero pressure on the tech. $45,000 in recaptured plumbing revenue."
        ),
        "visual_cue": "Show phone screen tapping 'Add Inspection Photo' in a field service app, then smiling at camera.",
        "caption": "How to unlock dual-trade cross-selling without forcing your technicians to be sleazy pushy salespeople. #bluecollar #fieldservice #plumber #hvaclife #businessowner",
        "cta": "Comment 'CHECKLIST' to get our technician field inspection SOP."
    },
    {
        "num": 9,
        "date": "2026-10-16",
        "day_time": "Week 3: Friday 4:30 PM EST",
        "format": "Contrarian Insight",
        "pillar": "Dual-Trade Cross-Sell Silos",
        "status": "READY TO RECORD",
        "text_hook": "Why technicians hate selling 🛠️🙅‍♂️",
        "verbal_hook": "If your field technicians are resisting your sales training, good. You hired mechanics, not used car salesmen.",
        "script": (
            "[LEAN FORWARD - SERIOUS TONE]\n"
            "Most contractor business coaches tell owners: 'Send your technicians to high-pressure sales seminars!'\n\n"
            "[SCOFF - SHAKE HEAD]\n"
            "It fails every single time. Why? Because your best technicians pride themselves on technical craftsmanship and honest diagnostic integrity.\n\n"
            "[NOD]\n"
            "When you force them to memorize manipulative closing scripts, your best guys feel dirty and they quit.\n\n"
            "[EXPLAIN SOLUTION]\n"
            "The solution is operational: Build the choices into your estimate software. Let the software present the tiers. Let the technician remain the trusted advisor.\n\n"
            "Protect your culture, protect your technicians, and watch your close rate increase."
        ),
        "visual_cue": "Wear a clean work polo or button-up, speak emphatically with authentic contractor empathy.",
        "caption": "Stop trying to turn honest technicians into high-pressure salesmen. Build the sales psychology into your systems instead. #trades #bluecollarlife #businessculture #hvac #plumbing",
        "cta": "Check the link in my bio to book a 1-on-1 systems walkthrough."
    },
    {
        "num": 10,
        "date": "2026-10-19",
        "day_time": "Week 4: Monday 6:45 AM EST",
        "format": "Screen Walkthrough / Talking Head",
        "pillar": "Digital Infrastructure & Spam Deliverability",
        "status": "READY TO RECORD",
        "text_hook": "Why your quotes land in SPAM 📥🚫",
        "verbal_hook": "If your commercial bids are getting ignored, there is an 80% chance they are sitting in your customer's junk folder.",
        "script": (
            "[SHOW LAPTOP SCREEN WITH EMAIL HEADER TOOL]\n"
            "Contractors spend thousands on marketing, send out a $25,000 commercial quote, and then wonder why the client never opened it.\n\n"
            "[POINT TO EMAIL DOMAIN]\n"
            "Two massive red flags we find during every tech audit:\n\n"
            "[COUNT 1]\n"
            "1. Using a `@gmail.com` or `@yahoo.com` email for commercial dispatch. In 2026, corporate spam filters immediately quarantine personal email addresses.\n\n"
            "[COUNT 2]\n"
            "2. Zero SPF, DKIM, or DMARC authentication on your custom domain. If these 3 DNS records aren't configured, Google and Outlook reject your invoices.\n\n"
            "[LOOK AT CAMERA]\n"
            "This takes 15 minutes to fix and stops tens of thousands in proposals from disappearing into spam."
        ),
        "visual_cue": "Show a laptop screen with a red 'FAILED SPF/DKIM' error, then flip to camera with urgent tone.",
        "caption": "Why trade contractors lose $20k jobs before the client even reads the bid. Fix your DNS records today. #emaildeliverability #contractorsoftiktok #tradesman #operations #businesstips",
        "cta": "Link in bio to audit your company's digital infrastructure."
    },
    {
        "num": 11,
        "date": "2026-10-21",
        "day_time": "Week 4: Wednesday 12:15 PM EST",
        "format": "Green Screen Teardown",
        "pillar": "Digital Infrastructure & Spam Deliverability",
        "status": "READY TO RECORD",
        "text_hook": "The 6.9-Second Website Bounce Penalty 📉",
        "verbal_hook": "If your website takes longer than 3 seconds to load on an iPhone, over half your visitors are leaving before they see your phone number.",
        "script": (
            "[GREEN SCREEN: GOOGLE LIGHTHOUSE PAGESPEED AUDIT SCORE - 28/100 RED]\n"
            "[POINT TO LOAD TIME: 6.9 SECONDS]\n"
            "Google released official data proving that if a mobile page load stretches from 1 second to 5 seconds, the probability of a bounce increases by 90%.\n\n"
            "[STEP ASIDE]\n"
            "Look at this audit: 6.9 seconds on mobile. This plumbing contractor was spending $4,500 a month on Google Ads, sending traffic to a website so bloated with uncompressed truck photos that 52% of visitors bounced.\n\n"
            "[CALCULATE OUT LOUD]\n"
            "That's $2,300 in ad budget literally thrown in the trash every single month. Compress your images, clean your cache, and cut your bounce rate in half."
        ),
        "visual_cue": "Green screen displaying Google PageSpeed Insights mobile report showing red 28 performance score.",
        "caption": "Why high Google Ads spend fails. If your mobile load time is over 3 seconds, 50% of your paid traffic bounces before dialing. #digitalmarketing #googleads #contractor #plumber #hvac",
        "cta": "Want to know your site speed score? Drop your domain in the comments."
    },
    {
        "num": 12,
        "date": "2026-10-23",
        "day_time": "Week 4: Friday 4:30 PM EST",
        "format": "Whiteboard / Screen Flow",
        "pillar": "Digital Infrastructure & Spam Deliverability",
        "status": "READY TO RECORD",
        "text_hook": "The 10-Second Lead Capture Stack ⚡",
        "verbal_hook": "Here is the exact 3-piece software stack that captures 94% of inbound leads automatically.",
        "script": (
            "[WRITE ON WHITEBOARD: CRM + SMS + DISPATCH]\n"
            "You don't need 10 different complicated software tools to run an 8-figure trade company. You only need three that talk to each other:\n\n"
            "[DRAW ARROW 1]\n"
            "1. Central Dispatch CRM (ServiceTitan, Housecall Pro, or Jobber).\n\n"
            "[DRAW ARROW 2]\n"
            "2. Instant SMS Webhook Relay. The second a web form or missed call registers, a personalized text fires in 10 seconds.\n\n"
            "[DRAW ARROW 3]\n"
            "3. Cloud VoIP Tracking Line. Logs all recordings directly into the customer file so your dispatchers never re-ask basic questions.\n\n"
            "Clean architecture beats shiny tools every single day."
        ),
        "visual_cue": "Draw clean workflow diagram on whiteboard connecting Phone -> Webhook -> CRM -> Tech App.",
        "caption": "Stop buying shiny SaaS tools that don't talk to each other. Simplify your field service tech stack. #systems #software #fieldservice #bluecollar #contractorsoftiktok",
        "cta": "Link in bio to see our full 4-pillar systems diagnostic roadmap."
    },
    {
        "num": 13,
        "date": "2026-10-26",
        "day_time": "Week 5: Monday 6:45 AM EST",
        "format": "Green Screen Teardown",
        "pillar": "Google Map Pack & Review Velocity",
        "status": "READY TO RECORD",
        "text_hook": "Why you're ranked #7 on Google Maps 🗺️📍",
        "verbal_hook": "It's not your website keywords. Here is the exact reason your competitor is sitting in the top 3 on Google Maps.",
        "script": (
            "[GREEN SCREEN: GOOGLE MAPS 3-PACK BENCHMARK TABLE]\n"
            "[POINT TO COMPETITOR #1: 480 REVIEWS (4.9 STARS)]\n"
            "Look at the top contractor in this market: 480 reviews, 4.9 stars, and getting 15 new reviews every single week.\n\n"
            "[POINT TO TARGET COMPANY: 42 REVIEWS]\n"
            "Now look down here: 42 reviews. The last review was posted 4 months ago.\n\n"
            "[LOOK AT CAMERA]\n"
            "Google Maps does not care how nice your logo is. Google cares about REVIEW VELOCITY—how consistently fresh reviews are coming in.\n\n"
            "If your competitor gets 20 reviews a month and you get 1, Google pushes you down to page 2. And on page 2, nobody calls."
        ),
        "visual_cue": "Green screen highlighting competitor benchmark table from our audit deliverable.",
        "caption": "Why Google Map Pack rankings drop. Review velocity is the #1 local ranking factor for trade contractors. #localbusiness #googlemaps #seo #contractorsoftiktok #trades",
        "cta": "Comment 'MAPS' to get our local competitor benchmark template."
    },
    {
        "num": 14,
        "date": "2026-10-28",
        "day_time": "Week 5: Wednesday 12:15 PM EST",
        "format": "Talking Head",
        "pillar": "Google Map Pack & Review Velocity",
        "status": "READY TO RECORD",
        "text_hook": "How to get 35 Google reviews a month ⭐⭐⭐⭐⭐",
        "verbal_hook": "Stop begging customers for reviews manually. Here is the automated trigger that generates 35 five-star reviews a month.",
        "script": (
            "[HOLD UP PHONE SHOWING SMS NOTIFICATION]\n"
            "Most contractors tell their technicians: 'Make sure to remind Mrs. Jones to leave us a Google review!'\n\n"
            "[SHAKE HEAD]\n"
            "Does Mrs. Jones do it? No. She has kids to feed and dinner to make.\n\n"
            "[SHOW AUTOMATED FLOW]\n"
            "Here is the automated protocol: The exact second the technician hits 'Job Complete' and collects payment on his tablet, an automated text fires:\n\n"
            "'Hi Mrs. Jones, Mike just completed your repair! Was everything clean and professional? Tap here to confirm: [Direct Google Review Link]'\n\n"
            "When you ask within 3 minutes of completion while the technician is still packing his tools, your review conversion rate jumps from 4% to 38%."
        ),
        "visual_cue": "Demonstrate tapping 'Complete Job' on tablet, instant notification chime on phone, smile at camera.",
        "caption": "Timing is everything in review collection. Ask 3 minutes after the job is finished, not 3 days later by email. #businessautomation #fieldservicemanagement #contractor #plumber #hvac",
        "cta": "Follow for daily operations workflows for trade contractors."
    },
    {
        "num": 15,
        "date": "2026-10-30",
        "day_time": "Week 5: Friday 4:30 PM EST",
        "format": "POV / Scenario",
        "pillar": "Google Map Pack & Review Velocity",
        "status": "READY TO RECORD",
        "text_hook": "The Suburban SEO Secret 🏡🎯",
        "verbal_hook": "Stop wasting your marketing budget trying to rank for your entire metropolitan area.",
        "script": (
            "[HOLD UP MAP OF METRO AREA WITH SUBURB CIRCLED]\n"
            "If you are in Houston, Dallas, or Atlanta, trying to rank for 'Houston Plumber' is like trying to boil the ocean. You're competing against $50M PE-backed rollups with unlimited ad budgets.\n\n"
            "[POINT TO HIGH-INCOME SUBURB]\n"
            "Instead, dominate the top 3 wealthiest suburban clusters within 15 miles of your dispatch yard.\n\n"
            "[NOD]\n"
            "Target location pages, localized Google Maps profiles, and hyper-targeted service radius. You get higher-ticket replacement jobs, shorter drive times, and zero wasted fuel burn.\n\n"
            "Own your backyard before trying to conquer the whole state."
        ),
        "visual_cue": "Draw circle around suburb on physical map, cross out downtown core with red marker.",
        "caption": "Why hyper-local suburban positioning beats broad metro targeting for 10-20 van trade fleets. #contractor #localmarketing #fieldservice #plumbing #hvacbusiness",
        "cta": "Link in bio to audit your company's local search presence."
    },
    {
        "num": 16,
        "date": "2026-11-02",
        "day_time": "Week 6: Monday 6:45 AM EST",
        "format": "Contrarian Rant",
        "pillar": "The Headcount Trap vs Dispatch Automation",
        "status": "READY TO RECORD",
        "text_hook": "Stop hiring more dispatchers! 🛑📞",
        "verbal_hook": "You don't need to hire another $50,000-a-year office dispatcher. You need to fix your broken handoff workflows.",
        "script": (
            "[DIRECT EYE CONTACT - PASSIONATE DELIVERY]\n"
            "Every time a contractor fleet hits $3M or $5M, the owner says: 'Joel, our office is chaotic. Phones are ringing, techs are complaining, I need to hire 2 more office staff!'\n\n"
            "[RAISE HAND TO STOP]\n"
            "Stop right there. Adding headcount to a broken process does not fix the problem—it just creates a more expensive broken process.\n\n"
            "[COUNT ISSUES]\n"
            "Your dispatchers aren't drowning because there are too many calls. They're drowning because they spend 65% of their day manually copying addresses, texting technicians updates, and chasing unsigned estimate PDFs.\n\n"
            "Automate the repetitive administrative handoffs. Free your team to do high-touch customer care."
        ),
        "visual_cue": "Sit in front of stacked messy paperwork, push it aside to reveal a clean tablet dashboard.",
        "caption": "The Headcount Trap in service trade businesses. Don't hire to compensate for broken software workflows. #businessoperations #fieldservice #contractorsoftiktok #bluecollar #productivity",
        "cta": "Link in bio to book a 15-minute operational discovery call."
    },
    {
        "num": 17,
        "date": "2026-11-04",
        "day_time": "Week 6: Wednesday 12:15 PM EST",
        "format": "Screen Walkthrough",
        "pillar": "The Headcount Trap vs Dispatch Automation",
        "status": "READY TO RECORD",
        "text_hook": "Why your trucks are wasting gas 🚐⛽",
        "verbal_hook": "If your service vans are crisscrossing each other on the highway, your dispatch board is burning your net margin.",
        "script": (
            "[SHOW GPS ROUTE SCREEN WITH JAGGED CROSSING LINES]\n"
            "Look at this fleet map: Truck 4 is driving 35 miles south for a routine filter change, while Truck 7 is driving 30 miles north for a drain clean.\n\n"
            "[SHAKE HEAD]\n"
            "They literally passed each other on the highway. That is 2 hours of technician windshield time and $40 in fuel burned for zero billable revenue.\n\n"
            "[EXPLAIN CLUSTER DISPATCH]\n"
            "By implementing geographic cluster dispatch, you group routine service calls into tight 5-mile zones and reserve floating vans exclusively for high-margin emergency calls.\n\n"
            "Fewer miles driven, 1 extra billable ticket per truck per day."
        ),
        "visual_cue": "Show GPS fleet tracking screen with chaotic zigzag routes vs clean cluster zones.",
        "caption": "Windshield time kills contractor profitability. Cluster dispatch recovers 1 extra billable job per van per day. #fleetmanagement #trades #contractor #plumbing #hvac",
        "cta": "Comment 'FLEET' for our dispatch routing optimization guide."
    },
    {
        "num": 18,
        "date": "2026-11-06",
        "day_time": "Week 6: Friday 4:30 PM EST",
        "format": "Whiteboard / Screen Flow",
        "pillar": "The Headcount Trap vs Dispatch Automation",
        "status": "READY TO RECORD",
        "text_hook": "The 12-Minute Morning Dispatch Ritual ☕📋",
        "verbal_hook": "If your morning dispatch meeting takes longer than 12 minutes, your operations are bleeding money.",
        "script": (
            "[SHOW CLOCK SETTING TO 12 MINUTES]\n"
            "At 7:00 AM in most trade yards, it's complete chaos. Techs standing around drinking coffee, dispatchers frantically printing paper tickets, parts missing from warehouse shelves.\n\n"
            "[WRITE 3 RULES ON WHITEBOARD]\n"
            "Here is the 12-minute operational standard of 8-figure fleets:\n\n"
            "1. All truck inventory replenished the night before by the warehouse lead.\n"
            "2. First 2 jobs pre-assigned to mobile tablets at 6:00 PM the previous evening.\n"
            "3. 7-minute standup reviewing yesterday's conversion rate and today's priority emergencies.\n\n"
            "Vans rolling by 7:15 AM. That's how you win the morning."
        ),
        "visual_cue": "Stand at whiteboard with countdown timer set on phone, write the 3 rules with brisk energy.",
        "caption": "Win the morning, win the day. The 12-minute dispatch protocol that gets vans on the road before competitors. #morningroutine #contractorsoftiktok #tradesman #leadership #businessowner",
        "cta": "Follow for weekly trade business operational frameworks."
    },
    {
        "num": 19,
        "date": "2026-11-09",
        "day_time": "Week 7: Monday 6:45 AM EST",
        "format": "Green Screen Teardown",
        "pillar": "Prioritization & Deloitte Effort vs Impact",
        "status": "READY TO RECORD",
        "text_hook": "The Deloitte Effort vs Impact Matrix 📊⚡",
        "verbal_hook": "Stop trying to fix everything at once in your trade business. Here's how to prioritize high-ROI wins.",
        "script": (
            "[GREEN SCREEN: DELOITTE EFFORT VS IMPACT MATRIX FROM AUDIT REPORT]\n"
            "[POINT TO TOP LEFT QUADRANT: LOW EFFORT, HIGH VALUE]\n"
            "Look at this quadrant right here: 'Quick Wins'.\n\n"
            "Most contractors try to tackle massive, painful projects first—like switching their entire CRM or completely redesigning their brand.\n\n"
            "[POINT TO ITEM 1: INSTANT SMS TRIAGE]\n"
            "Look at this: Setting up instant after-hours SMS triage takes 4 hours of setup. Cost? Less than $500. Payback horizon? Under 14 days. Recaptured revenue? Over $14,000 a month.\n\n"
            "[LEAN IN]\n"
            "Execute the low-effort, high-impact operational fixes first. Fund your growth with recaptured cash flow."
        ),
        "visual_cue": "Green screen displaying 4-quadrant Deloitte Prioritization Matrix from Summit Mechanical audit deliverable.",
        "caption": "Why you should never switch CRMs until you've plugged basic lead leakage. Prioritize low-effort high-impact quick wins. #consulting #operations #contractor #plumber #hvaclife",
        "cta": "Link in bio to see how our 4-pillar diagnostic scores your fleet."
    },
    {
        "num": 20,
        "date": "2026-11-11",
        "day_time": "Week 7: Wednesday 12:15 PM EST",
        "format": "Talking Head",
        "pillar": "Prioritization & Deloitte Effort vs Impact",
        "status": "READY TO RECORD",
        "text_hook": "How we unlocked $486,000 without ads 📈💵",
        "verbal_hook": "How an 18-van mechanical contractor recaptured $486,000 in annual profit without buying a single new truck.",
        "script": (
            "[DIRECT TO CAMERA - CALM AUTHORITY]\n"
            "When people think about growing a trade business, they always say: 'Buy 5 more vans! Spend $10,000 more on Google Ads!'\n\n"
            "[SHAKE HEAD]\n"
            "In our recent diagnostic of an 18-van mechanical fleet, we found $486,000 in annualized revenue leakage across 3 internal bottlenecks:\n\n"
            "[COUNT 1, 2, 3]\n"
            "1. $216k in uncaptured dual-trade cross-sells between HVAC and plumbing.\n"
            "2. $174k in after-hours emergency call abandonment.\n"
            "3. $96k in single-tier flat estimates.\n\n"
            "They didn't need more leads. They needed tighter systems."
        ),
        "visual_cue": "Hold printed 4-page audit sample deliverable, show cover page, speak with calm executive authority.",
        "caption": "Revenue vs Capacity. You don't always need more marketing—often you just need to stop leaking the leads you already paid for. #casestudy #businessgrowth #contractor #bluecollar #systems",
        "cta": "Book a 15-minute operational discovery call at the link in bio."
    },
    {
        "num": 21,
        "date": "2026-11-13",
        "day_time": "Week 7: Friday 4:30 PM EST",
        "format": "Contrarian Insight",
        "pillar": "Prioritization & Deloitte Effort vs Impact",
        "status": "READY TO RECORD",
        "text_hook": "The Vanity Metric Trap (Revenue vs Margin) 💸",
        "verbal_hook": "A $5M trade business taking home 4% net margin is actually smaller than a $2M business taking home 18%.",
        "script": (
            "[LEAN IN CLOSE]\n"
            "In the trades, everyone loves to brag about their top-line revenue: 'We did $6 Million this year!'\n\n"
            "[SMIRK]\n"
            "Cool. What did you take home at the end of December? Because if you did $6M at a 3% net profit, you made $180,000 while carrying $2M in truck debt and managing 35 stressed employees.\n\n"
            "[POINT FINGER]\n"
            "Meanwhile, a tight 8-van operator doing $2.2M at 19% net margin takes home $418,000 in clean, stress-free profit.\n\n"
            "Revenue feeds your ego. Margin feeds your family. Build for systems and margin."
        ),
        "visual_cue": "Write $6,000,000 (3% = $180k) vs $2,200,000 (19% = $418k) on notepad, point to the second number.",
        "caption": "Stop chasing top-line vanity numbers. High-margin operational systems beat bloated low-margin volume every time. #profitmargin #businessmindset #contractorsoftiktok #trades #entrepreneur",
        "cta": "Follow for daily operational frameworks for trade entrepreneurs."
    },
    {
        "num": 22,
        "date": "2026-11-16",
        "day_time": "Week 8: Monday 6:45 AM EST",
        "format": "Talking Head / POV",
        "pillar": "Seasonal Weather Volatility & Emergency Spikes",
        "status": "READY TO RECORD",
        "text_hook": "What happens when the first freeze hits? ❄️🥶",
        "verbal_hook": "When the first winter freeze hits and your phone rings 300 times in 2 hours, what happens to the 280 calls you miss?",
        "script": (
            "[SOUND OF PHONE RINGING CONSTANTLY]\n"
            "It's 6:00 AM on the first sub-zero morning of the winter. Every pipe in the city is freezing, furnaces are failing, and your phone board is melting.\n\n"
            "[LOOK AT CAMERA]\n"
            "Your office dispatcher can only answer 1 call at a time. The other 20 callers get a busy signal or voicemail. They hang up and call the next contractor.\n\n"
            "[REVEAL SOLUTION]\n"
            "Contractors with automated surge capacity handle this differently: Inbound overflow calls route to an AI voice triage agent that captures address, confirms leak severity, and slots emergencies into the dispatch board automatically.\n\n"
            "Don't let seasonal weather crashes break your business."
        ),
        "visual_cue": "Act out answering phone, another phone rings, looking overwhelmed, then showing tablet handling calls smoothly.",
        "caption": "How elite plumbing & HVAC fleets prepare for weather surges without burning out their office staff. #weatheremergency #plumbing #hvac #contractor #fieldservice",
        "cta": "Link in bio to audit your fleet's emergency surge capacity."
    },
    {
        "num": 23,
        "date": "2026-11-18",
        "day_time": "Week 8: Wednesday 12:15 PM EST",
        "format": "Whiteboard",
        "pillar": "Seasonal Weather Volatility & Emergency Spikes",
        "status": "READY TO RECORD",
        "text_hook": "Dynamic Emergency Surge Pricing 🌡️📈",
        "verbal_hook": "Why trade contractors should use emergency surge pricing during peak weather disasters.",
        "script": (
            "[DRAW SURGE CURVE ON WHITEBOARD]\n"
            "Airlines do it, Uber does it, hotels do it. Why do trade contractors still charge their standard $120 diagnostic fee during a catastrophic winter freeze?\n\n"
            "[EXPLAIN VALUE]\n"
            "When demand spikes by 500%, your resources are scarce. Tiered emergency diagnostic pricing does two critical things:\n\n"
            "1. It weeds out tire-kickers who just have a squeaky vent from real emergencies with burst water mains.\n"
            "2. It funds hazard pay and overtime bonuses for your technicians working 14-hour cold shifts.\n\n"
            "Price for value, protect your team, and prioritize true emergencies."
        ),
        "visual_cue": "Draw simple demand spike graph on whiteboard showing standard rate vs surge rate.",
        "caption": "Surge pricing in emergency trades isn't price gouging—it's triage economics that protects your technicians and prioritizes life safety. #economics #pricing #tradesman #contractorsoftiktok #hvac",
        "cta": "Comment 'SURGE' to receive our emergency dispatch pricing matrix."
    },
    {
        "num": 24,
        "date": "2026-11-20",
        "day_time": "Week 8: Friday 4:30 PM EST",
        "format": "Scenario / POV",
        "pillar": "Seasonal Weather Volatility & Emergency Spikes",
        "status": "READY TO RECORD",
        "text_hook": "The Post-Freeze Warranty Nightmare 📉🤦‍♂️",
        "verbal_hook": "Why bad documentation during emergency calls creates a 6-week warranty callback disaster.",
        "script": (
            "[HOLD HEAD IN HANDS - FRUSTRATED]\n"
            "'Hey boss, that customer from the freeze 3 weeks ago says we broke their sheetrock and refuses to pay the $4,500 balance.'\n\n"
            "[LOOK AT CAMERA]\n"
            "This happens to hundreds of contractors every winter. In the rush of emergency calls, technicians skip pre-existing condition photos.\n\n"
            "[HOLD UP SMARTPHONE]\n"
            "If your mobile dispatch workflow doesn't mandate 3 timestamped photos of pre-existing water damage BEFORE turning on a wrench, you have zero legal proof.\n\n"
            "Automated mobile documentation protects your cash flow and saves hundreds of hours in customer disputes."
        ),
        "visual_cue": "Demonstrate taking timestamped photo with field app before touching pipes, showing peace of mind.",
        "caption": "How to prevent warranty disputes and customer chargebacks after emergency storm jobs. Mobile photo verification is mandatory. #contractor #riskmanagement #plumbing #hvac #businesslaw",
        "cta": "Follow Joel Adawah Sani for operational systems strategies."
    },
    {
        "num": 25,
        "date": "2026-11-23",
        "day_time": "Week 9: Monday 6:45 AM EST",
        "format": "Direct Talking Head / Screen Showcase",
        "pillar": "Capstone Offer & Operational Diagnostic",
        "status": "READY TO RECORD",
        "text_hook": "How to audit your trade fleet in 15 mins 🔍📋",
        "verbal_hook": "Here is how we run a full 4-pillar operational diagnostic on $2M to $10M service trade companies.",
        "script": (
            "[HOLD PHYSICAL PRINTED AUDIT REPORT - FLIP THROUGH PAGES]\n"
            "Over the last 60 days, we've broken down why trade businesses leak hundreds of thousands in uncaptured revenue.\n\n"
            "[SHOW 4 PILLARS ON SCREEN]\n"
            "When I audit a contractor fleet, we evaluate 4 specific pillars:\n"
            "1. Sales & Marketing (Speed to lead & conversion latency)\n"
            "2. Customer Support (After-hours triage & review velocity)\n"
            "3. Product Delivery (Dispatch clustering & cross-sell handoffs)\n"
            "4. Internal Infrastructure (CRM sync, email DNS, and quote automation)\n\n"
            "[LEAN IN TO CAMERA]\n"
            "If you run a 5 to 25-van service fleet and want to know exactly where your operations are leaking cash, click the link in my bio to book a 1-on-1 15-minute diagnostic walkthrough. Let's inspect your systems."
        ),
        "visual_cue": "Hold physical institutional audit report, walk through the 4-pillar scoring matrix, look into lens with confident executive presence.",
        "caption": "Ready to plug the operational leakage in your service trade enterprise? Schedule a 15-minute diagnostic session with Joel Adawah Sani. #consulting #operations #plumbing #hvac #roofingcontractor",
        "cta": "Tap the link in bio to book your 15-minute Operational Discovery Call."
    }
]

def main():
    # 1. Write individual markdown script files
    scripts_dir = os.path.abspath('outputs/tiktok_content/scripts')
    os.makedirs(scripts_dir, exist_ok=True)
    
    print(f"Writing 25 teleprompter scripts to {scripts_dir}...")
    for v in VIDEOS:
        filename = f"video_{v['num']:02d}_{v['pillar'].lower().replace(' ', '_').replace('&', 'and')}.md"
        filepath = os.path.join(scripts_dir, filename)
        
        content = f"""# TikTok Video #{v['num']}: {v['text_hook']}

- **Scheduled Date & Time**: {v['day_time']} ({v['date']})
- **Video Format / Style**: {v['format']}
- **Content Pillar**: {v['pillar']}
- **Publish Status**: `{v['status']}`
- **Target Audience**: Trade contractors, plumbing/HVAC/electrical fleet owners ($1M–$10M)

---

## 1. Fast Visual Hook (0–3 Seconds)
* **On-Screen Text Overlay**: `{v['text_hook']}`
* **Visual Action / Movement**: {v['visual_cue']}
* **Spoken First Sentence**: "{v['verbal_hook']}"

---

## 2. Full Teleprompter Script (Word-for-Word)

{v['script']}

---

## 3. Video Metadata & Publishing Assets
* **TikTok Caption**:
  > {v['caption']}
* **Call to Action (CTA)**:
  > {v['cta']}
* **Recommended Audio**: Low-volume corporate lo-fi, synth ambient, or trending conversational beat.

---
*Created for Joel Adawah Sani | Principal Business Systems Consultant*
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    print("Individual scripts written successfully.")

    # 2. Write Master Calendar Markdown
    master_path = os.path.abspath('outputs/tiktok_content/master_calendar.md')
    print(f"Writing master calendar to {master_path}...")
    
    master_content = """# 60-Day TikTok Content & Video Script Engine Master Calendar
**Author**: Joel Adawah Sani | Principal Business Systems Consultant  
**Publishing Cadence**: 3 Videos / Week (Mondays 6:45 AM EST, Wednesdays 12:15 PM EST, Fridays 4:30 PM EST)  
**Total Deliverables**: 25 High-Converting Short-Form Vertical Video Scripts (35–60 Seconds)

---

## The Alternating Multi-Channel System (Zero Same-Day Clashing)

| Day of the Week | Active Platform | Publishing Window | Target Audience Mood / State |
| :--- | :--- | :--- | :--- |
| **Monday** | **TikTok** 📱 | 6:45 AM EST | Morning coffee scroll before crew dispatch |
| **Tuesday** | **LinkedIn** 💼 | 8:15 AM EST | Desk mode; deep-dive institutional PDF Carousel |
| **Wednesday** | **TikTok** 📱 | 12:15 PM EST | Midday truck lunch break; quick teardown / green screen |
| **Thursday** | **LinkedIn** 💼 | 9:00 AM EST | Choice architecture, pricing models & frameworks |
| **Friday** | **TikTok** 📱 | 4:30 PM EST | End-of-shift review & weekend emergency prep |
| **Saturday** | *OFF* ☕ | — | Rest; zero posting |
| **Sunday** | **LinkedIn** 💼 | 6:30 PM EST | Executive systems philosophy & founder mindset |

---

## 60-Day Publishing Ledger

| Video # | Scheduled Date & Time | Video Format / Style | Content Pillar | Hook Line / On-Screen Overlay | Teleprompter Script Link | Status |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
"""
    for v in VIDEOS:
        filename = f"video_{v['num']:02d}_{v['pillar'].lower().replace(' ', '_').replace('&', 'and')}.md"
        master_content += f"| **#{v['num']}** | {v['day_time']} | {v['format']} | {v['pillar']} | {v['text_hook']} | [Script](scripts/{filename}) | `{v['status']}` |\n"

    with open(master_path, "w", encoding="utf-8") as f:
        f.write(master_content)
    
    print("Master calendar written successfully.")

if __name__ == "__main__":
    main()
