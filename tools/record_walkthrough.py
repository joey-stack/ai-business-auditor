#!/usr/bin/env python3
"""
Custom Automated Browser Walkthrough Recorder for AI Business Auditor
Uses Playwright with installed system Chrome or Microsoft Edge to capture
a high-definition video walkthrough of a target prospect's website with
an interactive visual audit HUD overlay.
"""

import sys
import os
import argparse
import asyncio
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

async def record_walkthrough(url: str, output_path: str, duration_sec: int = 25):
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    temp_video_dir = out.parent / "_temp_video"
    if temp_video_dir.exists():
        shutil.rmtree(temp_video_dir)
    temp_video_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Initializing browser walkthrough recorder for: {url}")
    print(f"[*] Destination: {output_path}")

    async with async_playwright() as p:
        # Prefer system Chrome, fallback to msedge
        browser = None
        for channel in ["chrome", "msedge"]:
            try:
                browser = await p.chromium.launch(
                    channel=channel,
                    headless=True
                )
                print(f"[+] Successfully launched browser using '{channel}' channel.")
                break
            except Exception as e:
                print(f"[-] Could not launch with channel '{channel}': {e}")

        if not browser:
            # Fallback to default chromium
            browser = await p.chromium.launch(headless=True)
            print("[+] Successfully launched default Chromium.")

        context = await browser.new_context(
            record_video_dir=str(temp_video_dir),
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )

        page = await context.new_page()

        try:
            print(f"[*] Navigating to {url}...")
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(2000)

            # Inject aesthetic audit HUD overlay badge at top
            await page.evaluate("""() => {
                const badge = document.createElement('div');
                badge.id = 'ai-auditor-hud';
                badge.style.position = 'fixed';
                badge.style.top = '16px';
                badge.style.right = '20px';
                badge.style.zIndex = '999999';
                badge.style.background = 'rgba(15, 23, 42, 0.92)';
                badge.style.backdropFilter = 'blur(8px)';
                badge.style.color = '#ffffff';
                badge.style.padding = '10px 18px';
                badge.style.borderRadius = '10px';
                badge.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(56, 189, 248, 0.4)';
                badge.style.fontFamily = '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif';
                badge.style.fontSize = '13px';
                badge.style.fontWeight = '600';
                badge.style.display = 'flex';
                badge.style.alignItems = 'center';
                badge.style.gap = '10px';
                badge.innerHTML = `
                    <span style="width: 10px; height: 10px; background: #22c55e; border-radius: 50%; box-shadow: 0 0 10px #22c55e;"></span>
                    <span>AI Business Diagnostic Walkthrough</span>
                    <span id="ai-hud-status" style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; padding: 2px 8px; border-radius: 6px; font-size: 11px;">INITIALIZING</span>
                `;
                document.body.appendChild(badge);
            }""")

            async def update_hud(status_text: str):
                try:
                    await page.evaluate(f"""(txt) => {{
                        const el = document.getElementById('ai-hud-status');
                        if (el) el.textContent = txt;
                    }}""", status_text)
                except Exception:
                    pass

            await update_hud("HERO INSPECTION")
            await page.wait_for_timeout(2500)

            # Smooth scroll down page
            scroll_steps = [
                ("REPUTATION & RATINGS", 500, 2000),
                ("SERVICES OVERVIEW", 1200, 2500),
                ("PROMOTIONAL CTA & DISPATCH", 1800, 2000),
                ("ONLINE BOOKING INTAKE", 2500, 2500),
                ("FOOTER & SERVICE AREAS", 3400, 2000),
            ]

            for label, scroll_y, wait_ms in scroll_steps:
                await update_hud(label)
                await page.evaluate(f"window.scrollTo({{ top: {scroll_y}, behavior: 'smooth' }});")
                await page.wait_for_timeout(wait_ms)

            # Scroll back to top
            await update_hud("REVIEW COMPLETE")
            await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' });")
            await page.wait_for_timeout(2000)

        except Exception as e:
            print(f"[!] Warning during navigation: {e}")
        finally:
            await context.close()
            await browser.close()

    # Locate recorded video
    recorded_files = list(temp_video_dir.glob("*.webm"))
    if not recorded_files:
        print("[-] Error: No video file was recorded.")
        return None

    src_video = recorded_files[0]
    print(f"[+] Raw video recorded: {src_video} ({src_video.stat().st_size} bytes)")

    # Move to final output path
    # If target extension is .webm or .mp4, move or copy
    final_target = out
    if final_target.suffix.lower() not in [".webm", ".mp4"]:
        final_target = out.with_suffix(".webm")

    # If target is .mp4, check if ffmpeg is available to transcode, else save as webm
    ffmpeg_path = Path(r"C:\Users\user\AppData\Local\ms-playwright\ffmpeg-1011\ffmpeg-win64.exe")
    if final_target.suffix.lower() == ".mp4" and ffmpeg_path.exists():
        print(f"[*] Converting {src_video.name} to MP4 using Playwright FFmpeg...")
        cmd = f'"{ffmpeg_path}" -y -i "{src_video}" -c:v copy "{final_target}"'
        res = os.system(cmd)
        if res == 0 and final_target.exists():
            print(f"[+] MP4 conversion successful: {final_target}")
        else:
            # Fallback to moving webm
            final_target = out.with_suffix(".webm")
            shutil.move(str(src_video), str(final_target))
    else:
        shutil.move(str(src_video), str(final_target))

    # Clean up temp dir
    try:
        shutil.rmtree(temp_video_dir)
    except Exception:
        pass

    print(f"[SUCCESS] Walkthrough video generated at: {final_target} ({final_target.stat().st_size} bytes)")
    return str(final_target)

def main():
    parser = argparse.ArgumentParser(description="Record an automated website walkthrough video.")
    parser.add_argument("--url", required=True, help="Website URL to record")
    parser.add_argument("--output", "-o", required=True, help="Output video file path (.mp4 or .webm)")
    parser.add_argument("--duration", type=int, default=25, help="Approximate recording duration in seconds")
    args = parser.parse_args()

    res = asyncio.run(record_walkthrough(args.url, args.output, args.duration))
    if not res:
        sys.exit(1)

if __name__ == "__main__":
    main()
