#!/usr/bin/env python3
"""
Render TikTok Video #1 with Open Design Executive UI & Fixed Phonetic Voiceover.
- High-aesthetic 1080x1920 (9:16 vertical) UI rendered via Playwright Chromium
- Fonts: Plus Jakarta Sans, Inter, JetBrains Mono
- Phonetic Edge-TTS voiceover (no raw abbreviations or '000' mispronunciations)
- FFmpeg video compilation with AAC audio sync
"""
import os
import asyncio
import subprocess
from playwright.sync_api import sync_playwright
import edge_tts
import imageio_ffmpeg

OUTPUT_DIR = os.path.abspath("outputs/tiktok_content/rendered")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Phonetic Voiceover Script (Zero TTS pronunciation stumbles)
PHONETIC_SCRIPT = (
    "If a homeowner has water pouring through their ceiling at nine PM, "
    "do you really think they are filling out your seven-field website contact form? "
    "Not a chance. "
    "They pull out their phone, search emergency plumber near me, "
    "and dial the first three contractors on Google Maps. "
    "Whoever answers first, or triggers an automated text within sixty seconds, "
    "wins the thirty-five hundred dollar emergency replacement job. Every single time. "
    "In our systems audits of two to five million dollar trade fleets, "
    "we found businesses leaking over fourteen thousand five hundred dollars every single month, "
    "just from unassisted after-hours call abandonment. "
    "You don't need a four-thousand-dollar-a-month call center. "
    "You just need a ten-second automated dispatch triage. "
    "Tap the link in my bio to see the exact workflow."
)

async def generate_voiceover():
    audio_path = os.path.join(OUTPUT_DIR, "video_01_voiceover_clean.mp3")
    print("Generating phonetic neural voiceover...")
    comm = edge_tts.Communicate(PHONETIC_SCRIPT, "en-US-ChristopherNeural", rate="+5%")
    await comm.save(audio_path)
    print("Clean voiceover generated at:", audio_path)
    return audio_path

# 2. Open Design HTML Templates for the 5 Scenes
def get_base_css():
    return """
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap');
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        width: 1080px;
        height: 1920px;
        background: radial-gradient(circle at 80% 10%, rgba(14, 165, 233, 0.18) 0%, transparent 45%),
                    radial-gradient(circle at 10% 85%, rgba(244, 63, 94, 0.15) 0%, transparent 45%),
                    #070B14;
        color: #F8FAFC;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        padding: 90px 75px 120px 75px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }
    .top-glow-bar {
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 8px;
        background: linear-gradient(90deg, #38BDF8, #818CF8, #F43F5E);
    }
    .header-tag {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        background: rgba(14, 165, 233, 0.12);
        border: 1.5px solid rgba(56, 189, 248, 0.35);
        padding: 12px 26px;
        border-radius: 999px;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 2px;
        color: #38BDF8;
        text-transform: uppercase;
        width: fit-content;
    }
    .header-tag::before {
        content: '';
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #38BDF8;
        box-shadow: 0 0 12px #38BDF8;
    }
    .badge-emergency {
        background: rgba(244, 63, 94, 0.15) !important;
        border-color: rgba(244, 63, 94, 0.5) !important;
        color: #FB7185 !important;
    }
    .badge-emergency::before {
        background: #F43F5E !important;
        box-shadow: 0 0 12px #F43F5E !important;
    }
    .badge-emerald {
        background: rgba(16, 185, 129, 0.15) !important;
        border-color: rgba(16, 185, 129, 0.5) !important;
        color: #34D399 !important;
    }
    .badge-emerald::before {
        background: #10B981 !important;
        box-shadow: 0 0 12px #10B981 !important;
    }
    .badge-amber {
        background: rgba(245, 158, 11, 0.15) !important;
        border-color: rgba(245, 158, 11, 0.5) !important;
        color: #FBBF24 !important;
    }
    .badge-amber::before {
        background: #F59E0B !important;
        box-shadow: 0 0 12px #F59E0B !important;
    }
    .hero-title {
        font-size: 68px;
        font-weight: 900;
        line-height: 1.15;
        letter-spacing: -1.5px;
        color: #FFFFFF;
        margin-top: 28px;
    }
    .hero-title span {
        background: linear-gradient(90deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-title span.danger {
        background: linear-gradient(90deg, #FB7185, #F43F5E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-title span.success {
        background: linear-gradient(90deg, #34D399, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .card-glass {
        background: rgba(15, 23, 42, 0.75);
        border: 1.5px solid rgba(255, 255, 255, 0.1);
        border-radius: 32px;
        padding: 44px 48px;
        backdrop-filter: blur(24px);
        box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.6);
    }
    .footer-brand {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-top: 1.5px solid rgba(255, 255, 255, 0.1);
        padding-top: 32px;
    }
    .brand-left {
        display: flex;
        align-items: center;
        gap: 22px;
    }
    .brand-avatar {
        width: 72px;
        height: 72px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0284C7, #4F46E5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        font-weight: 900;
        color: #FFF;
        border: 2.5px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 0 20px rgba(2, 132, 199, 0.4);
    }
    .brand-name {
        font-size: 28px;
        font-weight: 800;
        color: #FFFFFF;
    }
    .brand-role {
        font-size: 19px;
        color: #94A3B8;
        font-weight: 600;
        margin-top: 4px;
    }
    .brand-pill {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 10px 22px;
        border-radius: 12px;
        font-size: 17px;
        font-weight: 700;
        color: #E2E8F0;
        font-family: 'JetBrains Mono', monospace;
    }
    """

def get_footer_html():
    return """
    <div class="footer-brand">
        <div class="brand-left">
            <div class="brand-avatar">JA</div>
            <div>
                <div class="brand-name">Joel Adawah Sani</div>
                <div class="brand-role">Principal Business Systems Consultant</div>
            </div>
        </div>
        <div class="brand-pill">SYSTEMS AUDIT</div>
    </div>
    """

def generate_scene_1_html():
    return f"""<!DOCTYPE html>
    <html>
    <head><style>{get_base_css()}</style></head>
    <body>
        <div class="top-glow-bar"></div>
        <div>
            <div class="header-tag badge-emergency">🚨 Real-World Field Test</div>
            <h1 class="hero-title">Water Is Pouring <br><span class="danger">Through The Ceiling.</span></h1>
            
            <div class="card-glass" style="margin-top: 50px;">
                <div style="font-size: 22px; color: #94A3B8; font-weight: 600;">Homeowner Scenario at 9:00 PM:</div>
                <div style="font-size: 38px; color: #FFFFFF; font-weight: 800; margin-top: 10px; line-height: 1.3;">
                    Do you think they fill out your 7-field website contact form?
                </div>
                
                <div style="margin-top: 40px; background: rgba(244, 63, 94, 0.12); border: 2px solid rgba(244, 63, 94, 0.4); border-radius: 22px; padding: 35px; text-align: center;">
                    <div style="font-size: 48px; font-weight: 900; color: #F43F5E; letter-spacing: 1px;">❌ NOT A CHANCE</div>
                    <div style="font-size: 24px; color: #FDA4AF; margin-top: 12px; font-weight: 600;">12-hour email replies forfeit the $3,500 replacement job.</div>
                </div>
            </div>

            <div class="card-glass" style="margin-top: 36px; background: rgba(14, 165, 233, 0.08); border-color: rgba(56, 189, 248, 0.3);">
                <div style="font-size: 20px; font-weight: 800; color: #38BDF8; letter-spacing: 1.5px; text-transform: uppercase;">What actually happens:</div>
                <div style="font-size: 34px; font-weight: 800; color: #F8FAFC; margin-top: 12px;">
                    They pull out their phone and search Google Maps for the first 3 contractors.
                </div>
            </div>
        </div>
        {get_footer_html()}
    </body>
    </html>"""

def generate_scene_2_html():
    return f"""<!DOCTYPE html>
    <html>
    <head><style>{get_base_css()}</style></head>
    <body>
        <div class="top-glow-bar"></div>
        <div>
            <div class="header-tag">🗺️ Google Maps 3-Pack Race</div>
            <h1 class="hero-title">They Dial The Top <br><span>3 Contractors In Line.</span></h1>
            
            <div style="display: flex; flex-direction: column; gap: 24px; margin-top: 45px;">
                <div class="card-glass" style="padding: 34px 40px; border-left: 8px solid #F43F5E; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-size: 32px; font-weight: 800; color: #FFF;">Contractor #1</div>
                        <div style="font-size: 22px; color: #FB7185; font-weight: 600; margin-top: 6px;">Rings out to voicemail (Unassisted)</div>
                    </div>
                    <div style="font-size: 36px;">❌</div>
                </div>

                <div class="card-glass" style="padding: 34px 40px; border-left: 8px solid #F43F5E; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-size: 32px; font-weight: 800; color: #FFF;">Contractor #2</div>
                        <div style="font-size: 22px; color: #FB7185; font-weight: 600; margin-top: 6px;">Answering machine: "Call back at 8 AM"</div>
                    </div>
                    <div style="font-size: 36px;">❌</div>
                </div>

                <div class="card-glass" style="padding: 38px 40px; border-left: 8px solid #10B981; background: rgba(16, 185, 129, 0.12); border-color: rgba(16, 185, 129, 0.5); display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="display: flex; align-items: center; gap: 14px;">
                            <div style="font-size: 34px; font-weight: 900; color: #FFF;">Contractor #3</div>
                            <span style="background: #10B981; color: #FFF; font-size: 15px; font-weight: 800; padding: 4px 14px; border-radius: 999px;">AUTOMATED FLEET</span>
                        </div>
                        <div style="font-size: 23px; color: #34D399; font-weight: 700; margin-top: 8px;">10-Second Automated SMS Triage Triggered</div>
                    </div>
                    <div style="font-size: 42px;">⚡</div>
                </div>
            </div>

            <div class="card-glass" style="margin-top: 36px; text-align: center; background: rgba(245, 158, 11, 0.1); border-color: rgba(245, 158, 11, 0.4);">
                <div style="font-size: 20px; font-weight: 800; color: #FBBF24; letter-spacing: 1.5px; text-transform: uppercase;">The Operational Law:</div>
                <div style="font-size: 34px; font-weight: 800; color: #FFF; margin-top: 8px;">
                    Speed to lead isn't marketing—it's architecture.
                </div>
            </div>
        </div>
        {get_footer_html()}
    </body>
    </html>"""

def generate_scene_3_html():
    return f"""<!DOCTYPE html>
    <html>
    <head><style>{get_base_css()}</style></head>
    <body>
        <div class="top-glow-bar"></div>
        <div>
            <div class="header-tag badge-emerald">⏱️ Speed-to-Lead Law</div>
            <h1 class="hero-title">Whoever Answers First <br><span class="success">Wins The $3,500 Job.</span></h1>
            
            <div class="card-glass" style="margin-top: 45px; text-align: center; border-color: rgba(16, 185, 129, 0.4);">
                <div style="font-size: 20px; font-weight: 800; color: #94A3B8; letter-spacing: 2px;">AVERAGE EMERGENCY REPLACEMENT TICKET</div>
                <div style="font-size: 110px; font-weight: 900; color: #34D399; font-family: 'JetBrains Mono', monospace; line-height: 1.1; margin: 15px 0;">$3,500+</div>
                <div style="font-size: 24px; color: #CBD5E1; font-weight: 600;">Main line burst, water heater failure, sewer backup</div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 32px;">
                <div class="card-glass" style="padding: 34px; background: rgba(244, 63, 94, 0.08); border-color: rgba(244, 63, 94, 0.3);">
                    <div style="font-size: 22px; font-weight: 800; color: #FB7185;">Manual Contractor</div>
                    <div style="font-size: 19px; color: #FDA4AF; margin-top: 14px; line-height: 1.6;">
                        • Misses night call<br>
                        • Listens at 8:00 AM<br>
                        • "Already hired."<br>
                    </div>
                    <div style="margin-top: 20px; font-size: 26px; font-weight: 900; color: #F43F5E;">$0 REVENUE</div>
                </div>

                <div class="card-glass" style="padding: 34px; background: rgba(16, 185, 129, 0.08); border-color: rgba(16, 185, 129, 0.3);">
                    <div style="font-size: 22px; font-weight: 800; color: #34D399;">Automated Fleet</div>
                    <div style="font-size: 19px; color: #86EFAC; margin-top: 14px; line-height: 1.6;">
                        • 10-Second SMS<br>
                        • Triage shutoff guide<br>
                        • On-call dispatched<br>
                    </div>
                    <div style="margin-top: 20px; font-size: 26px; font-weight: 900; color: #10B981;">+$3,500 WON</div>
                </div>
            </div>

            <div class="card-glass" style="margin-top: 30px; text-align: center; padding: 24px;">
                <div style="font-size: 22px; font-weight: 700; color: #38BDF8;">Harvard Business Review: 78% of customers hire the first responder.</div>
            </div>
        </div>
        {get_footer_html()}
    </body>
    </html>"""

def generate_scene_4_html():
    return f"""<!DOCTYPE html>
    <html>
    <head><style>{get_base_css()}</style></head>
    <body>
        <div class="top-glow-bar"></div>
        <div>
            <div class="header-tag badge-amber">📊 Institutional Audit Model</div>
            <h1 class="hero-title">After-Hours Abandonment <br><span class="danger">Leaks $14,500 / Month.</span></h1>
            
            <div class="card-glass" style="margin-top: 45px; border-color: rgba(239, 68, 68, 0.4);">
                <div style="font-size: 20px; font-weight: 800; color: #94A3B8; letter-spacing: 2px;">MEASURED ANNUAL REVENUE FORFEITED</div>
                <div style="font-size: 96px; font-weight: 900; color: #EF4444; font-family: 'JetBrains Mono', monospace; line-height: 1.1; margin: 15px 0;">-$174,000</div>
                <div style="height: 1.5px; background: rgba(255, 255, 255, 0.1); margin: 24px 0;"></div>
                <div style="font-size: 22px; color: #E2E8F0; font-weight: 700;">Grounded in Empirical Trade Fleet Telemetry:</div>
                <div style="font-size: 20px; color: #94A3B8; margin-top: 12px; line-height: 1.7;">
                    • 15-Van Service Fleet ($3.8M Annual Run Rate)<br>
                    • 14 Unassisted After-Hours Calls Abandoned Monthly<br>
                    • 35% Conversion Loss to Local Google Maps Competitors
                </div>
            </div>

            <div class="card-glass" style="margin-top: 36px; background: rgba(239, 68, 68, 0.08); border-color: rgba(239, 68, 68, 0.3); text-align: center;">
                <div style="font-size: 32px; font-weight: 900; color: #FFFFFF;">You Don't Need More Marketing Leads.</div>
                <div style="font-size: 24px; font-weight: 600; color: #38BDF8; margin-top: 10px;">You need to stop leaking the high-intent calls you already paid for.</div>
            </div>
        </div>
        {get_footer_html()}
    </body>
    </html>"""

def generate_scene_5_html():
    return f"""<!DOCTYPE html>
    <html>
    <head><style>{get_base_css()}</style></head>
    <body>
        <div class="top-glow-bar"></div>
        <div>
            <div class="header-tag">⚡ The 10-Second Fix</div>
            <h1 class="hero-title">You Don't Need A <br><span>$4,000/Mo Call Center.</span></h1>
            
            <div style="display: flex; flex-direction: column; gap: 20px; margin-top: 40px;">
                <div class="card-glass" style="padding: 28px 36px; display: flex; align-items: center; gap: 24px; border-left: 6px solid #38BDF8;">
                    <div style="background: #0284C7; color: #FFF; font-size: 22px; font-weight: 800; padding: 10px 18px; border-radius: 12px;">STEP 1</div>
                    <div style="font-size: 25px; font-weight: 700; color: #FFF;">Instant SMS acknowledgment in under 10 seconds</div>
                </div>

                <div class="card-glass" style="padding: 28px 36px; display: flex; align-items: center; gap: 24px; border-left: 6px solid #818CF8;">
                    <div style="background: #4F46E5; color: #FFF; font-size: 22px; font-weight: 800; padding: 10px 18px; border-radius: 12px;">STEP 2</div>
                    <div style="font-size: 25px; font-weight: 700; color: #FFF;">Emergency triage & water shutoff video sent to caller</div>
                </div>

                <div class="card-glass" style="padding: 28px 36px; display: flex; align-items: center; gap: 24px; border-left: 6px solid #10B981;">
                    <div style="background: #166534; color: #FFF; font-size: 22px; font-weight: 800; padding: 10px 18px; border-radius: 12px;">STEP 3</div>
                    <div style="font-size: 25px; font-weight: 700; color: #FFF;">On-call technician priority dispatch alert in CRM</div>
                </div>
            </div>

            <div class="card-glass" style="margin-top: 36px; background: linear-gradient(135deg, rgba(2, 132, 199, 0.4), rgba(79, 70, 229, 0.4)); border: 2px solid #38BDF8; text-align: center; padding: 45px;">
                <div style="font-size: 22px; font-weight: 800; color: #BAE6FD; letter-spacing: 2px; text-transform: uppercase;">Ready To Inspect Your Fleet?</div>
                <div style="font-size: 38px; font-weight: 900; color: #FFFFFF; margin-top: 10px;">Book a 15-Minute Diagnostic Walkthrough</div>
                <div style="margin-top: 25px; background: #FFFFFF; color: #0284C7; font-size: 24px; font-weight: 800; padding: 18px 36px; border-radius: 16px; display: inline-block;">
                    👉 Tap The Link In My Bio
                </div>
            </div>
        </div>
        {get_footer_html()}
    </body>
    </html>"""

def render_scenes_with_playwright():
    print("Launching Chromium to render Open Design 1080x1920 frames...")
    scenes = [
        ("scene_1.png", generate_scene_1_html()),
        ("scene_2.png", generate_scene_2_html()),
        ("scene_3.png", generate_scene_3_html()),
        ("scene_4.png", generate_scene_4_html()),
        ("scene_5.png", generate_scene_5_html()),
    ]
    
    rendered_paths = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        
        for name, html in scenes:
            page.set_content(html)
            page.wait_for_load_state("networkidle")
            out_img = os.path.join(OUTPUT_DIR, f"od_{name}")
            page.screenshot(path=out_img)
            rendered_paths.append(out_img)
            print(f"Rendered: {out_img}")
            
        browser.close()
        
    return rendered_paths

def compile_final_video(images, audio_path):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    output_mp4 = os.path.join(OUTPUT_DIR, "video_01_burst_pipe_v2_opendesign.mp4")
    
    # Precise scene durations matching clean voiceover:
    # Scene 1: 0.0 - 7.5s (7.5s)
    # Scene 2: 7.5 - 15.5s (8.0s)
    # Scene 3: 15.5 - 24.5s (9.0s)
    # Scene 4: 24.5 - 35.5s (11.0s)
    # Scene 5: 35.5 - 45.0s (9.5s)
    durations = [7.5, 8.0, 9.0, 11.0, 9.5]
    
    concat_file = os.path.join(OUTPUT_DIR, "concat_v2.txt")
    with open(concat_file, "w", encoding="utf-8") as f:
        for img_path, dur in zip(images, durations):
            f.write(f"file '{img_path.replace(chr(92), '/')}'\n")
            f.write(f"duration {dur}\n")
        f.write(f"file '{images[-1].replace(chr(92), '/')}'\n")
        
    print("Compiling Open Design vertical MP4 via FFmpeg...")
    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-i", audio_path,
        "-vf", "format=yuv420p",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print("\nOPEN DESIGN VIDEO V2 COMPILED SUCCESSFULLY!")
        print("Output file:", output_mp4)
        print("File size:", os.path.getsize(output_mp4), "bytes")
        return output_mp4
    else:
        print("FFmpeg error:", res.stderr[-500:])
        return None

def main():
    # 1. Generate clean voiceover
    audio_path = asyncio.run(generate_voiceover())
    
    # 2. Render Open Design UI scenes
    images = render_scenes_with_playwright()
    
    # 3. Compile to MP4
    final_video = compile_final_video(images, audio_path)
    print("Done!")

if __name__ == "__main__":
    main()
