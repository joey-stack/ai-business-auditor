#!/usr/bin/env python3
"""
Generate high-fidelity phonetic voiceover for TikTok Video #3:
"How to Protect Your Weekend Dinner"
"""
import os
import asyncio
import edge_tts

OUTPUT_DIR = os.path.abspath("outputs/tiktok_content/rendered")
REMOTION_PUBLIC = os.path.abspath("remotion-tiktok/public")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REMOTION_PUBLIC, exist_ok=True)

PHONETIC_SCRIPT_V3 = (
    "Here is the exact three-step automation that stops weekend emergency calls from ruining your family dinner. "
    "Every contractor I audit tells me the exact same thing: "
    "Joel, either my phone rings off the hook at Saturday dinner, or I miss out on thousands in revenue. "
    "Here is how we fix it without hiring a single person. "
    "Step one: Instant SMS Trigger. If an inbound call goes unassisted after hours or on weekends, "
    "an automated two-way text fires in under ten seconds: We see you called. Are you experiencing an active water leak or safety hazard? "
    "Step two: Interactive Triage. If they text yes, they receive immediate emergency shutoff instructions "
    "and your on-call technician receives a high-priority dispatch alert. If no, the job is queued for Monday at eight AM. "
    "Step three: Zero Headcount. You capture the twenty-five hundred dollar emergency job automatically, "
    "without paying an outsourced call center three thousand dollars a month. "
    "Tap the link in my bio to see the exact workflow."
)

async def main():
    out_file1 = os.path.join(OUTPUT_DIR, "video_03_voiceover.mp3")
    out_file2 = os.path.join(REMOTION_PUBLIC, "audio_v3.mp3")
    
    print("Synthesizing voiceover for Video #3...")
    comm = edge_tts.Communicate(PHONETIC_SCRIPT_V3, "en-US-ChristopherNeural", rate="+4%")
    await comm.save(out_file1)
    
    import shutil
    shutil.copyfile(out_file1, out_file2)
    print(f"Generated: {out_file1}")
    print(f"Copied to: {out_file2}")

if __name__ == "__main__":
    asyncio.run(main())
