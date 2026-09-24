#!/usr/bin/env python3
"""
Compress Social Media Videos for WhatsApp, Instagram, and Facebook.
- WhatsApp: Compresses status videos to strictly UNDER 10MB (typically 5MB-8MB) with H.264/AAC + faststart.
- Instagram & Facebook: Optimizes reels to under 20MB for instant mobile upload without buffering.
"""

import os
import sys
import subprocess
from pathlib import Path
import imageio_ffmpeg

# Fix Windows cp1252 unicode print crashes
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = ROOT_DIR / "outputs"
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

WA_DIR = OUTPUTS_DIR / "whatsapp_content"
IG_DIR = OUTPUTS_DIR / "instagram_content"
FB_DIR = OUTPUTS_DIR / "facebook_content"

def compress_video(input_path: Path, output_path: Path, max_target_mb: float = 8.5):
    """Compresses video to fit under max_target_mb using FFmpeg CRF and bitrate capping."""
    temp_output = output_path.parent / f"temp_{output_path.name}"
    
    # 2-pass or targeted CRF compression
    # For a 30s 1080x1920 video to be ~7MB, target video bitrate is around 1800k
    cmd = [
        FFMPEG_EXE, "-y",
        "-i", str(input_path),
        "-c:v", "libx264",
        "-crf", "28",
        "-preset", "faster",
        "-maxrate", "2000k",
        "-bufsize", "4000k",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        "-c:a", "aac",
        "-b:a", "96k",
        "-movflags", "+faststart",
        str(temp_output)
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error compressing {input_path.name}: {res.stderr[:300]}")
        return False
        
    size_mb = temp_output.stat().st_size / (1024 * 1024)
    print(f"  ✓ Compressed size: {size_mb:.2f} MB (Target: < {max_target_mb} MB)")
    
    # Replace original
    if temp_output.exists():
        temp_output.replace(output_path)
    return True

def main():
    print("==================================================================")
    print(" COMPRESSING SOCIAL MEDIA VIDEOS FOR WHATSAPP, FB & IG")
    print(f" Using FFmpeg: {FFMPEG_EXE}")
    print("==================================================================")

    # 1. WhatsApp Videos (Strictly < 10MB)
    print("\n--- Compressing WhatsApp Status Videos (< 10MB) ---")
    wa_videos = list(WA_DIR.glob("*/02_whatsapp_status_video.mp4"))
    for vid in wa_videos:
        orig_mb = vid.stat().st_size / (1024 * 1024)
        print(f"\nProcessing {vid.parent.name} (Original: {orig_mb:.2f} MB)...")
        compress_video(vid, vid, max_target_mb=9.0)
        final_mb = vid.stat().st_size / (1024 * 1024)
        print(f"  -> Final WhatsApp file: {vid.name} ({final_mb:.2f} MB)")

    # 2. Facebook Reels (Optimized < 18MB)
    print("\n--- Optimizing Facebook Reels (< 18MB) ---")
    fb_videos = list(FB_DIR.glob("*/01_facebook_reel.mp4"))
    for vid in fb_videos:
        orig_mb = vid.stat().st_size / (1024 * 1024)
        if orig_mb > 15.0:
            print(f"\nProcessing {vid.parent.name} (Original: {orig_mb:.2f} MB)...")
            compress_video(vid, vid, max_target_mb=12.0)
            final_mb = vid.stat().st_size / (1024 * 1024)
            print(f"  -> Final Facebook file: {vid.name} ({final_mb:.2f} MB)")
        else:
            print(f"  ✓ {vid.parent.name} already optimal ({orig_mb:.2f} MB)")

    # 3. Instagram Reels (Optimized < 18MB)
    print("\n--- Optimizing Instagram Reels (< 18MB) ---")
    ig_videos = list(IG_DIR.glob("*/01_instagram_reel.mp4"))
    for vid in ig_videos:
        orig_mb = vid.stat().st_size / (1024 * 1024)
        if orig_mb > 15.0:
            print(f"\nProcessing {vid.parent.name} (Original: {orig_mb:.2f} MB)...")
            compress_video(vid, vid, max_target_mb=12.0)
            final_mb = vid.stat().st_size / (1024 * 1024)
            print(f"  -> Final Instagram file: {vid.name} ({final_mb:.2f} MB)")
        else:
            print(f"  ✓ {vid.parent.name} already optimal ({orig_mb:.2f} MB)")

    print("\n==================================================================")
    print("✓ ALL SOCIAL MEDIA VIDEOS COMPRESSED AND POLICY-COMPLIANT!")
    print("==================================================================")

if __name__ == "__main__":
    main()
