#!/usr/bin/env python3
"""
Generate high-fidelity phonetic voiceover for TikTok Video #2:
"The 60-Second Rule on Google Maps"
"""
import os
import asyncio
import edge_tts

OUTPUT_DIR = os.path.abspath("outputs/tiktok_content/rendered")
REMOTION_PUBLIC = os.path.abspath("remotion-tiktok/public")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REMOTION_PUBLIC, exist_ok=True)

PHONETIC_SCRIPT_V2 = (
    "Whoever responds within sixty seconds captures seventy-eight percent of local emergency service calls. "
    "Look at this number right here: fourteen thousand five hundred dollars every single month. "
    "That is not marketing spend. "
    "That is uncaptured revenue from customers who called this plumbing company and hung up because nobody answered. "
    "Harvard Business Review tested lead response times across thousands of businesses. "
    "If you respond within five minutes versus thirty minutes, your qualification rate drops by twenty-one times. "
    "In emergency trades like plumbing, HVAC, and roofing, the window isn't five minutes. "
    "It is sixty seconds. "
    "If your trucks aren't automated to reply instantly, you're buying leads for your competitors. "
    "Comment AUDIT below, and I'll send you our four-pillar systems diagnostic checklist."
)

async def main():
    out_file1 = os.path.join(OUTPUT_DIR, "video_02_voiceover.mp3")
    out_file2 = os.path.join(REMOTION_PUBLIC, "audio_v2.mp3")
    
    print("Synthesizing voiceover for Video #2...")
    comm = edge_tts.Communicate(PHONETIC_SCRIPT_V2, "en-US-ChristopherNeural", rate="+4%")
    await comm.save(out_file1)
    
    # Also copy to remotion public
    import shutil
    shutil.copyfile(out_file1, out_file2)
    print(f"Generated: {out_file1}")
    print(f"Copied to: {out_file2}")

if __name__ == "__main__":
    asyncio.run(main())
