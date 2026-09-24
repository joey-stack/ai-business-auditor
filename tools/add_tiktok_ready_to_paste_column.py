#!/usr/bin/env python3
"""
Adds a dedicated 'Ready-to-Paste TikTok Caption with PDF Link (Copy & Paste)' column
(Column O) to the 'TikTok Content Calendar' tab in the Google Spreadsheet.
Allows Joel to simply copy the entire cell and paste directly into TikTok description box!
"""
import os
import sys
import json
import requests
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from generate_tiktok_engine import VIDEOS
import tools.sync_to_google_drive_and_sheets as s

LM_DISPATCH = "https://drive.google.com/file/d/1ujh_pfAvoVjOJncwPIYKOUK7UyEacmZg/view?usp=drivesdk"
LM_CHECKLIST = "https://drive.google.com/file/d/1SRbPfub84C7CIrH3YiSuOsd_2x30auWR/view?usp=drivesdk"
LM_WEEKEND = "https://drive.google.com/file/d/1efkkFytDU_o_gjsXN0qwO8PpsFRmamWL/view?usp=drivesdk"

def build_ready_to_paste_caption(video: dict) -> str:
    num = video["num"]
    text_hook = video["text_hook"]
    verbal_hook = video["verbal_hook"]
    pillar = video["pillar"]
    caption = video["caption"]
    cta = video["cta"]

    # Separate hashtags from existing caption
    parts = caption.split("#")
    main_caption_body = parts[0].strip()
    hashtags = ["#" + p.strip() for p in parts[1:] if p.strip()]

    # Ensure strong contractor / operations hashtags
    core_tags = [
        "#fieldservice",
        "#tradecontractors",
        "#plumbingcontractor",
        "#hvaclife",
        "#contractorsoftiktok",
        "#tradesman",
        "#operationsconsulting",
        "#joeladawahsani"
    ]
    for tag in core_tags:
        if tag.lower() not in [t.lower() for t in hashtags]:
            hashtags.append(tag)
    
    hashtag_str = " ".join(hashtags[:12])

    txt = (text_hook + " " + pillar + " " + caption).lower()

    if "weekend" in txt or "dinner" in txt:
        lm_title = "The Weekend Protection Blueprint (Free PDF)"
        lm_url = LM_WEEKEND
        action_cta = "👉 Tap the link above or link in bio to reclaim your weekends without missing high-margin calls!"
    elif "dispatch" in txt or "latency" in txt or "speed" in txt or "call" in txt or "lead" in txt or "pipe" in txt or "emergency" in txt or "bounce" in txt:
        lm_title = "The 10-Second Dispatch Workflow Blueprint (Free PDF)"
        lm_url = LM_DISPATCH
        action_cta = "👉 Tap the link above or check the link in bio to inspect your fleet's after-hours speed to lead!"
    else:
        lm_title = "The 4-Pillar Systems Diagnostic Checklist (Free PDF)"
        lm_url = LM_CHECKLIST
        action_cta = "👉 Tap the link above or link in bio to audit your trade fleet's operational efficiency!"

    # Clean, high-converting TikTok post copy with paragraphs
    full_copy = (
        f"{text_hook}\n\n"
        f"{verbal_hook}\n\n"
        f"{main_caption_body}\n\n"
        f"📥 FREE PDF RESOURCE:\n"
        f"{lm_title}:\n"
        f"{lm_url}\n\n"
        f"{action_cta}\n\n"
        f"{hashtag_str}"
    )

    return full_copy

def sync_column_o():
    env = s.load_env()
    client_id = env["GOOGLE_CLIENT_ID"]
    client_secret = env["GOOGLE_CLIENT_SECRET"]
    refresh_token = env["GOOGLE_REFRESH_TOKEN"]
    sheet_id = env.get("GOOGLE_SHEET_ID")

    print("[1/3] Authenticating with Google APIs...")
    token = s.get_access_token(client_id, client_secret, refresh_token)

    # 1. Expand columns to at least 18
    print("[2/3] Ensuring sheet grid width has space for Column O...")
    s.ensure_sheet_columns(sheet_id, token, min_columns=18)

    # 2. Build rows for Column O
    col_o_values = [["Ready-to-Paste TikTok Post Caption (Copy & Paste with PDF Link)"]]
    for v in VIDEOS:
        copy_text = build_ready_to_paste_caption(v)
        col_o_values.append([copy_text])

    print("[3/3] Writing Ready-to-Paste captions with direct PDF links to TikTok Content Calendar!O1:O26...")
    s.update_sheet_range(sheet_id, "TikTok Content Calendar!O1:O26", col_o_values, token)

    # 3. Format Column O (Width 450px, Wrap text)
    # Find sheetId for TikTok Content Calendar
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    sheet_id_num = None
    for sh in resp.json().get("sheets", []):
        if sh["properties"]["title"] == "TikTok Content Calendar":
            sheet_id_num = sh["properties"]["sheetId"]
            break

    if sheet_id_num is not None:
        formatting_req = {
            "requests": [
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": sheet_id_num,
                            "dimension": "COLUMNS",
                            "startIndex": 14, # Column O (0-indexed 14)
                            "endIndex": 15
                        },
                        "properties": {
                            "pixelSize": 460
                        },
                        "fields": "pixelSize"
                    }
                },
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id_num,
                            "startRowIndex": 0,
                            "endRowIndex": 26,
                            "startColumnIndex": 14,
                            "endColumnIndex": 15
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "wrapStrategy": "WRAP",
                                "verticalAlignment": "TOP"
                            }
                        },
                        "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"
                    }
                },
                # Style Header O1
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id_num,
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 14,
                            "endColumnIndex": 15
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {"red": 0.058, "green": 0.09, "blue": 0.164}, # #0F172A dark navy
                                "textFormat": {
                                    "foregroundColor": {"red": 1.0, "green": 0.84, "blue": 0.0}, # Gold/Yellow accent
                                    "bold": True,
                                    "fontSize": 10
                                }
                            }
                        },
                        "fields": "userEnteredFormat(backgroundColor,textFormat)"
                    }
                }
            ]
        }
        batch_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate"
        requests.post(batch_url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, json=formatting_req)

    print("\n[SUCCESS] COLUMN O ADDED TO GOOGLE SHEET WITH DIRECT PDF LINKS & READY-TO-PASTE COPY!")

if __name__ == "__main__":
    sync_column_o()
