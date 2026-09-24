#!/usr/bin/env python3
"""
Batch Walkthrough Video Generator for AI Business Auditor
Iterates through remaining audited clients, generates customized neural voiceover
across all 4 diagnostic pillars, records synchronized browser sessions with dynamic
executive HUD overlays, and muxes high-definition MP4 walkthrough deliverables.
"""

import os
import sys
import asyncio
import shutil
import subprocess
from pathlib import Path
import edge_tts
import imageio_ffmpeg
from playwright.async_api import async_playwright

CLIENT_CONFIGS = [
    {
        "slug": "austins-greatest-plumbing",
        "name": "Austin's Greatest Plumbing",
        "entity_badge": "Lic. #M-41618 | Austin, TX",
        "url": "https://austinsgreatestplumbing.com/",
        "script": [
            (
                "AI EXECUTIVE DIAGNOSTIC: AUSTIN'S GREATEST PLUMBING",
                "Master Plumber Lic. #M-41618 | South Austin, TX",
                "Welcome to the AI Business Diagnostic walkthrough for Austin's Greatest Plumbing, led by Master Plumber Rachel Humphreys. Today we examine the operational findings from your comprehensive audit across four core pillars: Sales and Marketing, Customer Support, Product Delivery, and Internal Operations.",
                0,
                2.0
            ),
            (
                "PILLAR 1: SALES & MARKETING — REPUTATION DEFICIT",
                "4.9★ (68 Reviews) vs. 4,500+ Competitor Average",
                "Looking at your digital presence, your 4.9-star rating demonstrates outstanding workmanship. However, with only 68 Google reviews, there is a massive visibility deficit compared to Austin market leaders like Radiant and Reliant, who command thousands of reviews. Furthermore, your booking subpage lacks clean indexing and mobile load speeds average 4.2 seconds, degrading mobile ad conversion.",
                800,
                2.5
            ),
            (
                "PILLAR 1: MOBILE CONVERSION & VISIBILITY",
                "4.2s Mobile Latency | Missing Geo-Targeted Landing Pages",
                "Analyzing local search geography, your core service areas in South Austin and Onion Creek lack dedicated neighborhood landing pages. Capturing high-intent water heater and repipe searches requires speed optimization below two seconds and localized service page silos.",
                1400,
                2.5
            ),
            (
                "PILLAR 2: CUSTOMER SUPPORT & EMERGENCY TRIAGE",
                "Manual Phone Intake Only — Zero 24/7 AI Triage",
                "Moving to customer support, emergency plumbing requires instant responsiveness. When homeowners encounter burst pipes after hours, calls currently roll to voicemail or an unmonitored web form. Installing a 24/7 conversational AI concierge allows you to qualify emergencies, capture leak photos, and lock in dispatch windows immediately without manual staff on call.",
                2000,
                2.5
            ),
            (
                "PILLAR 3: PRODUCT & SERVICE DELIVERY",
                "Field Quoting Missing Tiered Good / Better / Best Options",
                "In service delivery, your zero-contact capabilities are solid, but estimates are typically delivered as single line items. Introducing digital, multi-option Good, Better, Best proposals on technician tablets routinely increases average ticket size by 20 to 30 percent for water heater replacements and sewer line repairs.",
                2600,
                2.5
            ),
            (
                "PILLAR 4: INTERNAL OPERATIONS & INFRASTRUCTURE",
                "Disconnected Software Silos & Manual Invoicing Drag",
                "In your back-office infrastructure, customer records, website inquiries, and accounting operate in separate disconnected tools. Automating post-job review requests via SMS triggers and unifying your dispatch workflow will eliminate hours of administrative drag each week.",
                3200,
                2.5
            ),
            (
                "SUMMARY & 90-DAY DEPLOYMENT ROADMAP",
                "Opportunity Score: 82 / 100 | Tier C Priority",
                "With an Opportunity Score of 82, implementing automated review acquisition, mobile speed optimization, and an AI emergency triage assistant will position Austin's Greatest Plumbing to capture an estimated 12 to 20 additional premium jobs monthly. All technical recommendations are detailed in your complete PDF report.",
                0,
                3.0
            )
        ]
    },
    {
        "slug": "cold-is-on-the-right-plumbing-air",
        "name": "Cold Is On The Right Plumbing & Air",
        "entity_badge": "Plumbing & HVAC | Lakeway / Lake Travis, TX",
        "url": "https://www.coldisontheright.com/",
        "script": [
            (
                "AI EXECUTIVE DIAGNOSTIC: COLD IS ON THE RIGHT",
                "Dual-Trade Plumbing & Air | Lake Travis & Lakeway, TX",
                "Welcome to the AI Business Diagnostic walkthrough for Cold Is On The Right Plumbing and Air, founded by Master Plumber Brendin Dittman. In this executive walkthrough, we analyze the operational findings across your dual-trade business spanning sales, emergency triage, field delivery, and internal systems.",
                0,
                2.0
            ),
            (
                "PILLAR 1: SALES & MARKETING — DUAL-TRADE ADVANTAGE",
                "4.8★ (292 Reviews) | High-Income Corridor Under-Monetized",
                "Your business possesses a strong 4.8-star reputation across nearly 300 reviews. Operating in the affluent Lake Travis and Lakeway corridors gives you a major market advantage. However, your review volume remains far below Austin enterprise benchmarks, and your website does not fully cross-sell plumbing customers into high-margin HVAC maintenance agreements.",
                800,
                2.5
            ),
            (
                "PILLAR 1: LOCAL SEARCH & DIGITAL SPEED",
                "3.8s Mobile Response | Fragmented SEO Silos",
                "From a search visibility perspective, your HVAC and plumbing services compete under separate navigation menus without automated bundling. Optimizing your mobile page speeds and creating dedicated service packages for whole-home water softening and AC tune-ups will sharply reduce customer acquisition costs.",
                1500,
                2.5
            ),
            (
                "PILLAR 2: CUSTOMER SUPPORT & AFTER-HOURS TRIAGE",
                "24/7 Service Promised — Missing Conversational Emergency AI",
                "Examining emergency support, Lake Travis residents face urgent winter freeze bursts and summer AC outages. Currently, after-hours inquiries rely on manual telephone answering. Deploying an AI voice and web triage assistant ensures emergency callers receive immediate water shut-off instructions and instant priority scheduling, preventing lead loss to competitors.",
                2200,
                2.5
            ),
            (
                "PILLAR 3: PRODUCT & SERVICE DELIVERY",
                "Missing Unified VIP Maintenance Membership Engine",
                "In service delivery, the highest-leverage opportunity is an automated Dual-Trade VIP Membership Club. When plumbing technicians inspect a home, automated digital checklists can evaluate the HVAC system, presenting homeowners with Good, Better, Best service tiers that build predictable recurring monthly revenue.",
                2900,
                2.5
            ),
            (
                "PILLAR 4: INTERNAL OPERATIONS & DISPATCH",
                "Cross-Trade Scheduling Silos & Technician Dispatch",
                "Operationally, coordinating both HVAC technicians and master plumbers requires unified dispatch intelligence. Automating technician en-route SMS updates with live GPS tracking will elevate the customer experience to enterprise standards while reducing inbound status calls.",
                3500,
                2.5
            ),
            (
                "SUMMARY & 90-DAY DEPLOYMENT ROADMAP",
                "Opportunity Score: 80 / 100 | Tier B Priority",
                "With an Opportunity Score of 80, Cold Is On The Right is primed for accelerated growth. Unifying your dual-trade memberships and deploying 24/7 AI emergency intake can generate an estimated 20 to 30 thousand dollars in additional monthly recurring revenue. Full specifics are available in your PDF diagnostic.",
                0,
                3.0
            )
        ]
    },
    {
        "slug": "plumbing-outfitters",
        "name": "Plumbing Outfitters",
        "entity_badge": "Master Plumber Owned | North Austin & Taylor, TX",
        "url": "https://plumbingoutfitters.com/",
        "script": [
            (
                "AI EXECUTIVE DIAGNOSTIC: PLUMBING OUTFITTERS",
                "Commercial & Residential | Austin & Taylor, TX",
                "Welcome to the AI Business Diagnostic walkthrough for Plumbing Outfitters, founded by Warren and Ashley Stroud. Today we review the four operational pillars evaluated in your diagnostic report: Sales and Marketing, Customer Support, Commercial Delivery, and Infrastructure.",
                0,
                2.0
            ),
            (
                "PILLAR 1: SALES & MARKETING — COMMERCIAL OPPORTUNITY",
                "4.7★ (314 Reviews) | Untapped Commercial Multi-Family Funnel",
                "Plumbing Outfitters holds an enviable reputation with 314 verified reviews and dual operations in North Austin and Taylor. However, while your residential reputation is well-established, your commercial and multi-family property management services lack dedicated digital landing pages, case studies, and instant quote calculators.",
                900,
                2.5
            ),
            (
                "PILLAR 1: PERFORMANCE & LOCAL MAP PACK",
                "4.5s Mobile Speed | Dual-Location Regional Visibility",
                "Evaluating your digital footprint across both Austin and Taylor, localized search traffic can be significantly accelerated by adding dedicated geo-targeted hubs and streamlining mobile load times, which currently sit at 4.5 seconds.",
                1600,
                2.5
            ),
            (
                "PILLAR 2: CUSTOMER SUPPORT & LEAD ROUTING",
                "Generic Intake Form — Missing Commercial vs. Residential AI Routing",
                "In customer support, commercial property managers have vastly different urgency than residential homeowners. Your current web intake uses a standard generic form. Deploying an AI intake assistant that immediately identifies commercial account inquiries routes high-value contracts directly to ownership while handling routine calls automatically.",
                2300,
                2.5
            ),
            (
                "PILLAR 3: PRODUCT & SERVICE DELIVERY",
                "Tiered Commercial Maintenance Agreements & Asset Tracking",
                "In service delivery, your craftsmanship and licensing are top tier. The next level of operational maturity is providing commercial property managers with digital asset inspection logs and tiered preventive maintenance agreements, locking in multi-year service contracts.",
                3000,
                2.5
            ),
            (
                "PILLAR 4: INTERNAL OPERATIONS & MULTI-LOCATION DISPATCH",
                "Austin & Taylor Dual-Facility Dispatch Synchronization",
                "Managing crews across both Travis and Williamson counties creates routing complexity. Automating technician dispatch schedules, parts inventory tracking, and post-job review requests will eliminate administrative friction between your Austin and Taylor hubs.",
                3700,
                2.5
            ),
            (
                "SUMMARY & 90-DAY DEPLOYMENT ROADMAP",
                "Opportunity Score: 74 / 100 | Tier A High-Value Target",
                "Plumbing Outfitters is a Tier A market contender with an Opportunity Score of 74. Deploying automated commercial lead routing, dual-hub review capture, and digital maintenance proposals will solidify your dominance in the Central Texas corridor. Review the full roadmap in your PDF audit.",
                0,
                3.0
            )
        ]
    },
    {
        "slug": "clarke-kent-plumbing",
        "name": "Clarke Kent Plumbing",
        "entity_badge": "Established Contractor | South Austin, TX",
        "url": "https://www.clarkekentplumbing.com/",
        "script": [
            (
                "AI EXECUTIVE DIAGNOSTIC: CLARKE KENT PLUMBING",
                "Established 1986 | South Lamar & Ben White, Austin, TX",
                "Welcome to the AI Business Diagnostic walkthrough for Clarke Kent Plumbing, an established South Austin fixture located on West Ben White Boulevard. In this walkthrough, we examine the diagnostic findings across all four pillars of your business operations.",
                0,
                2.0
            ),
            (
                "PILLAR 1: SALES & MARKETING — BRAND EQUITY & SPEED",
                "4.6★ (185 Reviews) | 5.8s Mobile Latency & Legacy Theme",
                "Clarke Kent Plumbing enjoys decades of brand equity and 185 Google reviews. However, your digital presence has fallen behind modern market benchmarks. Your website runs on a dated template with 5.8-second mobile response latency, causing significant visitor drop-off from mobile searchers looking for immediate plumbing assistance.",
                800,
                2.5
            ),
            (
                "PILLAR 1: LOCAL SEARCH DEFICIT",
                "Missing Dedicated Service Area Silos in 78704 & South Austin",
                "While your physical shop on Ben White gives you great geographic proximity to South Lamar, Barton Hills, and Downtown, your web presence lacks localized neighborhood content, conceding top Map Pack positions to aggressive competitors.",
                1500,
                2.5
            ),
            (
                "PILLAR 2: CUSTOMER SUPPORT & CALL RECAPTURE",
                "Telephone-Only Ingestion — High Missed-Call Risk",
                "In customer support, your business relies almost exclusively on traditional phone calls. When technicians are under sinks or driving, incoming calls frequently go to voicemail. Over 80 percent of plumbing callers immediately dial the next contractor if their call isn't answered. An AI voice and SMS assistant can capture and book these calls instantly 24/7.",
                2200,
                2.5
            ),
            (
                "PILLAR 3: PRODUCT & SERVICE DELIVERY",
                "Paperless Transition & Good / Better / Best Digital Estimates",
                "Looking at service delivery, moving from paper-based or manual invoices to interactive digital estimates on technician tablets will elevate customer trust and increase average order values on water heater and sewer line repairs.",
                2800,
                2.5
            ),
            (
                "PILLAR 4: INTERNAL OPERATIONS & DATA SECURITY",
                "Legacy Email Hosting & Customer Records In Local Files",
                "Our infrastructure scan revealed legacy email hosting without modern DMARC authentication, creating deliverability risks for invoices. Unifying customer records into a cloud CRM will streamline scheduling and safeguard your valuable customer list.",
                3400,
                2.5
            ),
            (
                "SUMMARY & 90-DAY DEPLOYMENT ROADMAP",
                "Opportunity Score: 70 / 100 | Tier B Modernization Target",
                "With an Opportunity Score of 70, Clarke Kent Plumbing has tremendous untapped potential. Upgrading your mobile site speed, capturing missed calls with an AI assistant, and modernizing estimates will revitalize inbound job volume. The complete blueprint is inside your PDF report.",
                0,
                3.0
            )
        ]
    },
    {
        "slug": "wisdom-kwati-smart-city-plc",
        "name": "Wisdom Kwati Smart City Plc",
        "entity_badge": "Smart City Real Estate Conglomerate | Abuja, Nigeria",
        "url": "https://www.wisdomkwatismartcityplc.com",
        "script": [
            (
                "AI EXECUTIVE DIAGNOSTIC: WISDOM KWATI SMART CITY PLC",
                "Urban Mega-Developments & Land Banking | Abuja, FCT",
                "Welcome to the AI Executive Diagnostic walkthrough for Wisdom Kwati Smart City Plc, a leading real estate and infrastructure development conglomerate headquartered in Gwarinpa, Abuja. Today we review the four operational pillars analyzed in your diagnostic audit.",
                0,
                2.0
            ),
            (
                "PILLAR 1: SALES & MARKETING — DIASPORA VISIBILITY",
                "Multi-Billion Naira Asset Portfolio | LCP 7.5s Speed Latency",
                "Wisdom Kwati Smart City commands an extraordinary portfolio of smart residential developments and land banking projects across the Federal Capital Territory. However, international and diaspora visibility is heavily bottlenecked by high web latency, with Largest Contentful Paint exceeding 7.5 seconds, hindering prospective buyers in London, New York, and Toronto.",
                800,
                2.5
            ),
            (
                "PILLAR 1: GLOBAL BRAND TRUST & SEARCH VISIBILITY",
                "Low Organic Search Footprint in UK & US Diaspora Hubs",
                "Diaspora buyers represent your highest-margin off-plan property investors. Establishing dedicated diaspora investment portals with localized financing guides will dramatically increase direct institutional search capture.",
                1500,
                2.5
            ),
            (
                "PILLAR 2: CUSTOMER SUPPORT & INVESTOR TRIAGE",
                "Generic WhatsApp Links — Missing 24/7 AI Investor Screening",
                "Examining customer support, international investors reaching your site across time zones currently encounter generic contact forms and WhatsApp numbers. Implementing an AI diaspora investor concierge can qualify buyer budgets, verify purchasing timelines, and provide instant virtual property brochures around the clock.",
                2200,
                2.5
            ),
            (
                "PILLAR 3: PRODUCT & SERVICE DELIVERY",
                "Missing Interactive Virtual Tours & Digital Mortgage Room",
                "In service delivery, the primary friction point is remote investor verification. Introducing interactive 3D virtual site tours, automated milestone construction updates, and a secure digital documentation room will accelerate closing velocity for off-plan luxury homes.",
                2900,
                2.5
            ),
            (
                "PILLAR 4: INTERNAL OPERATIONS & SALES AGENT SYNC",
                "Fragmented Sales Agent Workflows & Lead Attribution",
                "Operationally, managing hundreds of estate agents and diaspora inquiries requires centralized CRM orchestration. Implementing automated lead distribution and instant follow-up triggers ensures no multi-million naira sales lead goes cold.",
                3600,
                2.5
            ),
            (
                "SUMMARY & 90-DAY DEPLOYMENT ROADMAP",
                "Opportunity Score: 68 / 100 | Tier C Capital Advisory Target",
                "With an Opportunity Score of 68, Wisdom Kwati Smart City has an immense opportunity to scale international property sales. Deploying an AI diaspora investor concierge and interactive buyer portal will unlock rapid capital inflows. All details are outlined in your executive PDF audit.",
                0,
                3.0
            )
        ]
    },
    {
        "slug": "lee-investment-handlers",
        "name": "LEE Investment Handlers",
        "entity_badge": "Private Market Asset Advisory | Lagos & Venice",
        "url": "https://www.leeinvestmenthandlers.com",
        "script": [
            (
                "AI EXECUTIVE DIAGNOSTIC: LEE INVESTMENT HANDLERS",
                "₦50B+ Private Market Assets | Lagos & Venice Advisory",
                "Welcome to the AI Executive Diagnostic walkthrough for LEE Investment Handlers, managing over 50 billion naira in private market assets across Nigeria and Europe. Today we examine the four operational pillars evaluated in your Google Search Console verified audit.",
                0,
                2.0
            ),
            (
                "PILLAR 1: SALES & MARKETING — SERP SNIPPET BLINDNESS",
                "Pos 4.5 on Google Page 1 with 0.0% CTR | Canonical HTTP Leaks",
                "Our inspection of your verified Search Console data revealed an urgent unforced error: your core services page ranks at position 4.5 on Google Page 1 with 70 impressions, yet generated exactly zero clicks due to broken SERP title tags. Furthermore, an insecure HTTP variant remains indexed alongside HTTPS.",
                800,
                2.5
            ),
            (
                "PILLAR 1: GOOGLE PLACES & LOCAL KNOWLEDGE GRAPH",
                "Unverified Business Profiles in Both Lagos and Venice Hubs",
                "Neither your Lagos headquarters in Akowonjo nor your Venice advisory office possesses a verified Google Business Profile. Claiming and optimizing these Knowledge Graph entities is critical to establishing institutional authority and capturing high-net-worth local referrals.",
                1500,
                2.5
            ),
            (
                "PILLAR 2: CUSTOMER SUPPORT & HNWI TRIAGE",
                "High-Touch Manual Onboarding Bottleneck — Zero AI Screening",
                "In customer support, institutional asset inquiries currently rely on static capture forms and direct telephone numbers. Deploying an AI conversational qualification agent allows you to pre-screen prospective investors, assess liquidity requirements, and deliver tailored portfolio briefing decks automatically.",
                2200,
                2.5
            ),
            (
                "PILLAR 3: PRODUCT & SERVICE DELIVERY",
                "Missing Secure Digital Investor Reporting Portal",
                "In service delivery, managing ₦50 billion across real estate, industrial foundries, and energy infrastructure requires real-time reporting. Introducing a secure investor dashboard with automated quarterly yields and KYC document ingestion will elevate client satisfaction to global institutional standards.",
                2900,
                2.5
            ),
            (
                "PILLAR 4: INTERNAL OPERATIONS & CROSS-BORDER SYNC",
                "Eliminating Advisory Silos Between Lagos & Venice Hubs",
                "Operationally, your Next.js and Turbopack web architecture is modern, but advisory workflows between Nigeria and Italy remain siloed. Automating macroeconomic briefing generation and unifying CRM intelligence will eliminate substantial advisor administrative drag.",
                3500,
                2.5
            ),
            (
                "SUMMARY & 90-DAY DEPLOYMENT ROADMAP",
                "Opportunity Score: 60 / 100 | Composite Score: 5.25 / 10",
                "With an Opportunity Score of 60, LEE Investment Handlers can achieve rapid ROI by fixing SERP metadata, claiming dual-hub Knowledge Graph entities, and installing an AI investor intake concierge. Full implementation details are documented in your complimentary PDF report.",
                0,
                3.0
            )
        ]
    }
]

def get_audio_durations(audio_files, ffmpeg_exe):
    durations = []
    for af in audio_files:
        try:
            res = subprocess.run(
                [str(ffmpeg_exe), "-i", str(af)],
                capture_output=True,
                text=True
            )
            dur = 25.0
            for line in res.stderr.splitlines():
                if "Duration:" in line:
                    parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
                    dur = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
                    break
            durations.append(dur)
        except Exception:
            durations.append(25.0)
    return durations

async def generate_voiceover(script, audio_dir: Path):
    audio_dir.mkdir(parents=True, exist_ok=True)
    voice = "en-US-ChristopherNeural"
    audio_files = []
    print(f"[*] Synthesizing voiceover with '{voice}'...")
    for idx, (hud_title, _, text, _, _) in enumerate(script):
        out_file = audio_dir / f"segment_{idx+1:02d}.mp3"
        comm = edge_tts.Communicate(text, voice, rate="+2%")
        await comm.save(str(out_file))
        audio_files.append(out_file)
        print(f"  [+] Segment {idx+1}/{len(script)} generated: {hud_title[:45]}...")
    return audio_files

async def record_single_client(cfg, ffmpeg_exe):
    slug = cfg["slug"]
    name = cfg["name"]
    entity_badge = cfg["entity_badge"]
    url = cfg["url"]
    script = cfg["script"]

    target_dir = Path("outputs/clients") / slug
    target_dir.mkdir(parents=True, exist_ok=True)
    temp_dir = target_dir / "_temp_walkthrough"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*70}\n[STARTING WALKTHROUGH] {name} ({slug})\n{'='*70}")

    # 1. Generate Voiceover
    audio_files = await generate_voiceover(script, temp_dir / "audio")
    durations = get_audio_durations(audio_files, ffmpeg_exe)
    total_audio_time = sum(durations)
    print(f"[*] Total voiceover duration: {total_audio_time:.1f}s across {len(audio_files)} sections.")

    # 2. Concat Voiceover Audio
    concat_list = temp_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for af in audio_files:
            f.write(f"file '{af.resolve().as_posix()}'\n")

    full_audio = temp_dir / "full_voiceover.mp3"
    sub_concat = subprocess.run(
        [str(ffmpeg_exe), "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(full_audio)],
        capture_output=True,
        text=True
    )
    if sub_concat.returncode != 0:
        print(f"[-] Audio concat error: {sub_concat.stderr}")
    else:
        print(f"[+] Full narration compiled: {full_audio}")

    # 3. Playwright Browser Recording
    video_capture_dir = temp_dir / "raw_video"
    video_capture_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Launching browser session for: {url}...")
    async with async_playwright() as p:
        browser = None
        for channel in ["chrome", "msedge"]:
            try:
                browser = await p.chromium.launch(headless=True, channel=channel)
                break
            except Exception:
                continue
        if not browser:
            browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(video_capture_dir),
            record_video_size={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print(f"[*] Navigating to {url}...")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(3000)
        except Exception as e:
            print(f"[-] Warning: Initial load timeout for {url}: {e}. Proceeding...")

        # Inject Executive HUD Overlay
        await page.evaluate("""([companyName, badgeText]) => {
            const container = document.createElement('div');
            container.id = 'ai-auditor-hud';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                left: 24px;
                right: 24px;
                z-index: 999999;
                display: flex;
                justify-content: space-between;
                align-items: center;
                pointer-events: none;
                transition: all 0.4s ease;
            `;

            container.innerHTML = `
                <div style="background: rgba(15, 23, 42, 0.92); backdrop-filter: blur(8px); color: #fff; padding: 12px 20px; border-radius: 10px; box-shadow: 0 8px 30px rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.1); max-width: 720px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #22c55e;"></span>
                        <span style="font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; font-weight: 700;">AI Business Auditor</span>
                        <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; margin-left: 6px;">LIVE WALKTHROUGH</span>
                    </div>
                    <div id="hud-title" style="font-size: 15px; font-weight: 700; color: #f8fafc; letter-spacing: -0.01em;">INITIALIZING DIAGNOSTIC</div>
                    <div id="hud-metric" style="font-size: 12px; color: #38bdf8; font-weight: 600; margin-top: 3px;">Connecting telemetry...</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(8px); color: #94a3b8; padding: 10px 16px; border-radius: 10px; font-family: -apple-system, sans-serif; font-size: 11px; font-weight: 600; box-shadow: 0 6px 20px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08);">
                    <div style="color: #64748b; font-size: 9px; text-transform: uppercase;">Target Entity</div>
                    <div style="color: #f8fafc; font-size: 12px; font-weight: 700;">` + companyName + `</div>
                    <div style="color: #22c55e; font-size: 10px; display: flex; align-items: center; gap: 4px;">● ` + badgeText + `</div>
                </div>
            `;
            document.body.appendChild(container);
        }""", [name, entity_badge])

        async def update_hud(title_text: str, metric_text: str):
            try:
                await page.evaluate("""([t, m]) => {
                    const tEl = document.getElementById('hud-title');
                    const mEl = document.getElementById('hud-metric');
                    if (tEl) tEl.textContent = t;
                    if (mEl) mEl.textContent = m;
                }""", [title_text, metric_text])
            except Exception:
                pass

        # Execute synchronized walkthrough steps
        for idx, (hud_title, hud_metric, _, scroll_target, pause_after) in enumerate(script):
            seg_duration = durations[idx]
            print(f"[*] Executing Section {idx+1}/{len(script)}: '{hud_title}' ({seg_duration:.1f}s)")
            await update_hud(hud_title, hud_metric)
            await page.evaluate(f"window.scrollTo({{ top: {scroll_target}, behavior: 'smooth' }});")
            await page.wait_for_timeout(int(seg_duration * 1000))
            if pause_after > 0:
                await page.wait_for_timeout(int(pause_after * 1000))

        await context.close()
        await browser.close()

    # 4. Locate Raw Video
    raw_videos = list(video_capture_dir.glob("*.webm"))
    if not raw_videos:
        print(f"[-] Error: No raw video captured for {slug}")
        return None
    raw_video = raw_videos[0]

    # 5. Mux Video + Audio
    final_mp4 = target_dir / "walkthrough.mp4"
    print(f"[*] Muxing video and narration into MP4: {final_mp4}...")
    mux_args = [
        str(ffmpeg_exe),
        "-y",
        "-i", str(raw_video),
        "-i", str(full_audio),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        str(final_mp4)
    ]
    sub_mux = subprocess.run(mux_args, capture_output=True, text=True)

    if sub_mux.returncode == 0 and final_mp4.exists():
        print(f"[SUCCESS] Deliverable created: {final_mp4} ({final_mp4.stat().st_size} bytes)")
    else:
        print(f"[-] Direct transcode failed: {sub_mux.stderr}. Copying fallback...")
        fallback = target_dir / "walkthrough.webm"
        shutil.copy(str(raw_video), str(fallback))
        final_mp4 = fallback

    # Clean up temp working files
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass

    return str(final_mp4)

async def main():
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    results = {}
    print(f"Starting batch generation for {len(CLIENT_CONFIGS)} remaining audited businesses...")

    for cfg in CLIENT_CONFIGS:
        try:
            res = await record_single_client(cfg, ffmpeg_exe)
            results[cfg["slug"]] = res
        except Exception as e:
            print(f"[-] Failed recording for {cfg['slug']}: {e}")
            results[cfg["slug"]] = None

    print("\n" + "="*70)
    print("BATCH RECORDING COMPLETED")
    print("="*70)
    for slug, path in results.items():
        print(f"  - {slug}: {path if path else 'FAILED'}")

if __name__ == '__main__':
    asyncio.run(main())
