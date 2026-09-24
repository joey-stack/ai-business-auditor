#!/usr/bin/env python3
"""
Detailed Narrated Browser Walkthrough Recorder for AI Business Auditor.
Synchronizes professional neural voiceover (edge-tts) with automated browser
interactions, visual audit HUD overlays, and metric callouts, rendering a
complete, high-definition MP4 walkthrough video.
"""

import os
import sys
import asyncio
import json
import shutil
from pathlib import Path
import subprocess
import edge_tts
import imageio_ffmpeg
from playwright.async_api import async_playwright

# Script segments: (hud_title, hud_metric, narration_text, scroll_target, pause_after_sec)
AUSTIN_PLUMBING_SCRIPT = [
    (
        "AI EXECUTIVE DIAGNOSTIC: AUSTIN PLUMBING®",
        "Master Plumber Lic. #M-44706 | Austin, TX",
        "Welcome to the AI Business Diagnostic walkthrough for Austin Plumbing, operating under Texas Master Plumber License M-44706. In this comprehensive walkthrough, we examine the four core operational pillars from your diagnostic audit: Sales and Marketing, Customer Support, Product Delivery, and Internal Infrastructure, identifying high-impact leverage points to accelerate inbound high-margin service calls.",
        0,
        2.0
    ),
    (
        "PILLAR 1: SALES & MARKETING — REPUTATION DEFICIT",
        "21 Verified Reviews vs. 4,500+ Competitor Average",
        "Starting here on the homepage, Austin Plumbing maintains an outstanding 4.8-star service rating. However, our technical benchmark reveals a critical market bottleneck: your business currently holds only 21 verified Google reviews. In the Greater Austin market, dominant competitors like Radiant with over 17,000 reviews and Reliant with 4,500 reviews monopolize the high-intent Google Map Pack for emergency keywords, forcing your team to rely heavily on expensive paid ads.",
        450,
        2.5
    ),
    (
        "PILLAR 1: SALES & MARKETING — MOBILE SPEED LATENCY",
        "6.9s Mobile Page Load vs. 2.0s Industry Target",
        "Scrolling through your services, live server telemetry recorded an initial page download and response latency of 6.9 seconds on WordPress and Divi. For emergency plumbing services where over 80 percent of distressed homeowners search on mobile devices during active water leaks, 7-second load times trigger catastrophic bounce rates exceeding 50 percent, forfeiting valuable emergency tickets before customers even see your phone number.",
        1100,
        2.5
    ),
    (
        "PILLAR 2: CUSTOMER SUPPORT & EMERGENCY TRIAGE",
        "Manual Phone Only — Zero 24/7 Conversational AI",
        "Moving down to emergency service intake, Austin Plumbing prominently advertises 24-hour emergency support. Yet, visitors are limited strictly to raw telephone links and a standard Jobber work request form. After business hours, there is no conversational AI or automated call triage to assist homeowners facing pipe bursts. Deploying an AI voice and chat concierge allows you to qualify emergencies, capture leak photos, and lock in arrival windows 24/7.",
        1850,
        2.5
    ),
    (
        "PILLAR 3: PRODUCT & SERVICE DELIVERY",
        "Jobber CRM Installed — Missing Tiered Quoting & Live GPS",
        "Looking at your field operations, your integration with Jobber provides clean web scheduling and zero-contact service. However, two significant revenue levers remain untapped: first, automated technician-en-route SMS notifications with live GPS tracking; and second, interactive Good, Better, Best digital quoting on technician tablets for major water heater and repipe installations, which typically lifts average ticket values by 20 to 30 percent.",
        2500,
        2.5
    ),
    (
        "PILLAR 4: INTERNAL OPERATIONS & EMAIL SECURITY",
        "Critical SPF Misalignment Under p=quarantine",
        "Finally, our infrastructure audit uncovered an urgent transactional email vulnerability. Your domain SPF record currently authorizes legacy GoDaddy servers, but omits Microsoft 365 Exchange and Jobber dispatch servers under a strict quarantine policy. As a result, automated customer quotes and dispatch confirmations risk being flagged as spam by modern mailbox providers.",
        3300,
        2.5
    ),
    (
        "SUMMARY & 90-DAY DEPLOYMENT ROADMAP",
        "Overall Score: 5.00 / 10 | High Opportunity Prospect",
        "By resolving your DNS authentication, deploying automated post-service SMS review capture via Jobber webhooks, and optimizing mobile speeds under 2 seconds, Austin Plumbing can systematically overtake larger competitors and capture an estimated 15 to 25 additional high-margin jobs each month. The complete findings and step-by-step roadmap are detailed in your complimentary PDF report. Thank you for your craftsmanship, and we look forward to connecting.",
        0,
        3.0
    )
]

async def generate_voiceover(script, audio_dir: Path):
    audio_dir.mkdir(parents=True, exist_ok=True)
    voice = "en-US-ChristopherNeural"  # Professional, confident male consultant voice
    audio_files = []
    
    print(f"[*] Generating neural voiceover using '{voice}'...")
    for idx, (title, metric, text, _, _) in enumerate(script):
        segment_path = audio_dir / f"segment_{idx:02d}.mp3"
        comm = edge_tts.Communicate(text, voice, rate="+2%")
        await comm.save(str(segment_path))
        audio_files.append(segment_path)
        print(f"  [+] Segment {idx+1}/{len(script)} generated: {title}")

    return audio_files

def get_audio_durations(audio_files):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    import subprocess
    durations = []
    for af in audio_files:
        cmd = [ffmpeg_exe, "-i", str(af)]
        proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, errors="replace")
        # Find duration in stderr
        import re
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", proc.stderr)
        if m:
            hours, mins, secs = m.groups()
            dur = int(hours)*3600 + int(mins)*60 + float(secs)
            durations.append(dur)
        else:
            durations.append(15.0)
    return durations

async def run_detailed_walkthrough(url: str, output_path: str):
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = out.parent / "_temp_walkthrough"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate Voiceover
    audio_files = await generate_voiceover(AUSTIN_PLUMBING_SCRIPT, temp_dir / "audio")
    durations = get_audio_durations(audio_files)
    total_audio_time = sum(durations)
    print(f"[*] Total voiceover duration: {total_audio_time:.1f} seconds across {len(audio_files)} sections.")

    # 2. Concat all audio files
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    concat_list = temp_dir / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for af in audio_files:
            # write normalized path
            f.write(f"file '{af.resolve().as_posix()}'\n")

    full_audio_path = temp_dir / "full_voiceover.mp3"
    concat_args = [
        str(ffmpeg_exe),
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(full_audio_path)
    ]
    sub_res = subprocess.run(concat_args, capture_output=True, text=True)
    if sub_res.returncode != 0:
        print(f"[-] Concat error: {sub_res.stderr}")
    else:
        print(f"[+] Full narration compiled: {full_audio_path}")

    # 3. Record Browser Session with Synced Navigation
    video_capture_dir = temp_dir / "raw_video"
    video_capture_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Launching browser walkthrough recording for: {url}...")
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
        await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(3000)

        # Inject Executive HUD Overlay
        await page.evaluate("""() => {
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
                <div style="background: rgba(15, 23, 42, 0.92); backdrop-filter: blur(8px); color: #fff; padding: 12px 20px; border-radius: 10px; box-shadow: 0 8px 30px rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.1); max-width: 700px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
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
                    <div style="color: #f8fafc; font-size: 12px; font-weight: 700;">Austin Plumbing®</div>
                    <div style="color: #22c55e; font-size: 10px; display: flex; align-items: center; gap: 4px;">● Verified Company Profile</div>
                </div>
            `;
            document.body.appendChild(container);
        }""")

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
        for idx, (hud_title, hud_metric, _, scroll_target, pause_after) in enumerate(AUSTIN_PLUMBING_SCRIPT):
            seg_duration = durations[idx]
            print(f"[*] Executing Section {idx+1}/{len(AUSTIN_PLUMBING_SCRIPT)}: '{hud_title}' ({seg_duration:.1f}s)")
            
            await update_hud(hud_title, hud_metric)
            
            # Smooth scroll to target position
            await page.evaluate(f"window.scrollTo({{ top: {scroll_target}, behavior: 'smooth' }});")
            
            # Wait for the exact spoken narration length
            await page.wait_for_timeout(int(seg_duration * 1000))
            if pause_after > 0:
                await page.wait_for_timeout(int(pause_after * 1000))

        await context.close()
        await browser.close()

    # 4. Locate Raw Video
    raw_videos = list(video_capture_dir.glob("*.webm"))
    if not raw_videos:
        print("[-] Error: No raw video was captured.")
        return None
    raw_video = raw_videos[0]
    print(f"[+] Raw video captured: {raw_video} ({raw_video.stat().st_size} bytes)")

    # 5. Mux Video + Audio using imageio-ffmpeg into pristine MP4
    final_mp4 = out.with_suffix(".mp4")
    print(f"[*] Muxing video and narration into final MP4: {final_mp4}...")
    
    # Use imageio_ffmpeg with AAC audio and H.264 video
    mux_args = [
        str(ffmpeg_exe),
        "-y",
        "-i", str(raw_video),
        "-i", str(full_audio_path),
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
        print(f"[SUCCESS] Detailed narrated walkthrough video created: {final_mp4} ({final_mp4.stat().st_size} bytes)")
    else:
        print(f"[-] Warning: Direct MP4 transcode failed: {sub_mux.stderr}, attempting copy...")
        # Fallback copy
        shutil.copy(str(raw_video), str(out.with_suffix(".webm")))
        final_mp4 = out.with_suffix(".webm")

    # Clean up temp working files
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass

    return str(final_mp4)

if __name__ == '__main__':
    url = "https://austinplumbing.com/"
    target = "outputs/clients/austin-plumbing/walkthrough.mp4"
    res = asyncio.run(run_detailed_walkthrough(url, target))
    if not res:
        sys.exit(1)
