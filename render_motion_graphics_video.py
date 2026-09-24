#!/usr/bin/env python3
"""
Render TikTok Video #1 as a pure dynamic Motion Graphics video.
Combines:
- HTML5 / CSS3 / WebGL smooth animations, drifting ambient orbs, and pulsing glows
- Staggered card slides with cubic-bezier easing
- Animated real-time glowing progress bar
- Dynamic synchronized subtitle pill tracking the voiceover in real-time
- Playwright Chromium 1080x1920 60/30fps capture
- FFmpeg H.264 encode merged with clean phonetic neural audio
"""
import os
import time
import subprocess
from playwright.sync_api import sync_playwright
import imageio_ffmpeg

OUTPUT_DIR = os.path.abspath("outputs/tiktok_content/rendered")
HTML_FILE = os.path.abspath("outputs/tiktok_content/rendered/motion_graphics.html")
RECORD_DIR = os.path.abspath("outputs/tiktok_content/rendered/recording_cache")
FINAL_MP4 = os.path.abspath("outputs/tiktok_content/rendered/video_01_burst_pipe_motion_graphics.mp4")
AUDIO_FILE = os.path.abspath("outputs/tiktok_content/rendered/video_01_voiceover_clean.mp3")

os.makedirs(RECORD_DIR, exist_ok=True)

# Add real-time clock script to HTML
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html_text = f.read()

# Make sure the clock autostarts smoothly
if "const startTime = performance.now();" not in html_text:
    autostart_js = """
    // Autostart real-time motion loop
    const startTime = performance.now();
    function animateLoop() {
      const elapsed = (performance.now() - startTime) / 1000.0;
      window.setPlaybackTime(elapsed);
      if (elapsed < totalDuration + 2) {
        requestAnimationFrame(animateLoop);
      }
    }
    requestAnimationFrame(animateLoop);
  </script>
</body>"""
    html_text = html_text.replace("</script>\n</body>", autostart_js)
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_text)

def record_motion_graphics():
    # Clean previous webm in cache
    for f in os.listdir(RECORD_DIR):
        if f.endswith(".webm"):
            try: os.remove(os.path.join(RECORD_DIR, f))
            except: pass

    print("Launching Chromium with high-FPS viewport recording (1080x1920)...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1080, "height": 1920},
            record_video_dir=RECORD_DIR,
            record_video_size={"width": 1080, "height": 1920}
        )
        page = context.new_page()
        
        file_url = "file:///" + HTML_FILE.replace("\\", "/")
        print(f"Loading motion graphics canvas: {file_url}")
        page.goto(file_url)
        page.wait_for_load_state("networkidle")
        
        print("Recording real-time motion graphics (49.5 seconds)...")
        time.sleep(49.5)
        
        context.close()
        browser.close()

    recorded_files = [os.path.join(RECORD_DIR, f) for f in os.listdir(RECORD_DIR) if f.endswith(".webm")]
    if not recorded_files:
        raise RuntimeError("No recorded video found in cache.")
    
    latest_webm = sorted(recorded_files, key=os.path.getmtime)[-1]
    print(f"Motion graphics recorded successfully: {latest_webm}")
    return latest_webm

def compile_final_mp4(webm_path):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print("Muxing motion graphics video with clean neural audio into final MP4...")
    
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", webm_path,
        "-i", AUDIO_FILE,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        FINAL_MP4
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print("\n==========================================")
        print("MOTION GRAPHICS VIDEO COMPILED SUCCESSFULLY!")
        print(f"Final MP4: {FINAL_MP4}")
        print(f"File Size: {os.path.getsize(FINAL_MP4)} bytes")
        print("==========================================")
        return FINAL_MP4
    else:
        print("FFmpeg Error:", res.stderr[-500:])
        return None

if __name__ == "__main__":
    webm = record_motion_graphics()
    compile_final_mp4(webm)
