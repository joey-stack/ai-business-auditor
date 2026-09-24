#!/usr/bin/env python3
"""
Sync TikTok Content Calendar & Video Script Engine to Google Sheets.
Creates or updates a dedicated 'TikTok Content Calendar' tab in the user's Google Spreadsheet.
Includes:
- 25 date-mapped TikTok video rows (Mondays 6:45 AM, Wednesdays 12:15 PM, Fridays 4:30 PM)
- Video format, content pillar, on-screen text hook, verbal hook, full teleprompter script, visual cues, caption, hashtags, and CTAs.
"""
import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path
from generate_tiktok_engine import VIDEOS

def load_env():
    p = Path(".env")
    env = {}
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

def get_access_token(client_id, client_secret, refresh_token):
    token_url = "https://oauth2.googleapis.com/token"
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }).encode("utf-8")
    req = urllib.request.Request(token_url, data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        tokens = json.loads(resp.read().decode("utf-8"))
        return tokens.get("access_token")

def batch_update_spreadsheet(sheet_id, requests, token):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate"
    payload = json.dumps({"requests": requests}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def update_range(sheet_id, range_a1, values, access_token):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{urllib.parse.quote(range_a1)}?valueInputOption=USER_ENTERED"
    payload = json.dumps({"range": range_a1, "values": values}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        method="PUT"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    env = load_env()
    client_id = env["GOOGLE_CLIENT_ID"]
    client_secret = env["GOOGLE_CLIENT_SECRET"]
    refresh_token = env["GOOGLE_REFRESH_TOKEN"]
    sheet_id = env["GOOGLE_SHEET_ID"]

    print("Authenticating with Google OAuth...")
    token = get_access_token(client_id, client_secret, refresh_token)
    print("Authentication successful.")

    # 1. Inspect existing sheets to check if 'TikTok Content Calendar' exists
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        sheet_meta = json.loads(resp.read().decode("utf-8"))

    tab_name = "TikTok Content Calendar"
    existing_sheets = {s["properties"]["title"]: s["properties"]["sheetId"] for s in sheet_meta.get("sheets", [])}

    new_sheet_id = None
    if tab_name in existing_sheets:
        print(f"Tab '{tab_name}' already exists (sheetId: {existing_sheets[tab_name]}). Updating existing sheet.")
        new_sheet_id = existing_sheets[tab_name]
    else:
        print(f"Creating new tab '{tab_name}'...")
        add_sheet_req = {
            "addSheet": {
                "properties": {
                    "title": tab_name,
                    "gridProperties": {
                        "rowCount": 50,
                        "columnCount": 12,
                        "frozenRowCount": 1
                    },
                    "tabColor": {
                        "red": 0.0,
                        "green": 0.7,
                        "blue": 0.8
                    }
                }
            }
        }
        res = batch_update_spreadsheet(sheet_id, [add_sheet_req], token)
        new_sheet_id = res["replies"][0]["addSheet"]["properties"]["sheetId"]
        print(f"Tab '{tab_name}' created successfully with sheetId: {new_sheet_id}")

    # 2. Build rows
    headers = [
        "Video #",
        "Scheduled Date & Time",
        "Video Style / Format",
        "Content Pillar",
        "Publish Status",
        "On-Screen Text Hook (0-3s)",
        "Verbal Hook (First Sentence)",
        "Full Teleprompter Script & Directions",
        "Visual & B-Roll Cues",
        "TikTok Caption & Hashtags",
        "Call to Action (CTA)",
        "Local Script File"
    ]

    all_rows = [headers]

    for v in VIDEOS:
        filename = f"outputs/tiktok_content/scripts/video_{v['num']:02d}_{v['pillar'].lower().replace(' ', '_').replace('&', 'and')}.md"
        row = [
            f"Video #{v['num']}",
            v["day_time"],
            v["format"],
            v["pillar"],
            v["status"],
            v["text_hook"],
            v["verbal_hook"],
            v["script"],
            v["visual_cue"],
            v["caption"],
            v["cta"],
            filename
        ]
        all_rows.append(row)

    # 3. Write data
    target_range = f"'{tab_name}'!A1:L{len(all_rows)}"
    print(f"Writing {len(all_rows)} rows to {target_range}...")
    update_range(sheet_id, target_range, all_rows, token)
    print("Values written successfully.")

    # 4. Apply styling
    # Modern dark slate header (#0F172A), frozen row, column widths, text wrapping
    format_requests = [
        # Format Header Row (Dark Slate, Bold White Text, Centered)
        {
            "repeatCell": {
                "range": {
                    "sheetId": new_sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 12
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {
                            "red": 0.06,
                            "green": 0.09,
                            "blue": 0.16
                        },
                        "textFormat": {
                            "bold": True,
                            "foregroundColor": {
                                "red": 1.0,
                                "green": 1.0,
                                "blue": 1.0
                            },
                            "fontSize": 10
                        },
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE",
                        "wrapStrategy": "WRAP"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)"
            }
        },
        # Freeze Top Header Row
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": new_sheet_id,
                    "gridProperties": {
                        "frozenRowCount": 1
                    }
                },
                "fields": "gridProperties.frozenRowCount"
            }
        },
        # Set Header Row Height to 46px
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": new_sheet_id,
                    "dimension": "ROWS",
                    "startIndex": 0,
                    "endIndex": 1
                },
                "properties": {
                    "pixelSize": 46
                },
                "fields": "pixelSize"
            }
        },
        # Set Text Wrapping for all data cells
        {
            "repeatCell": {
                "range": {
                    "sheetId": new_sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(all_rows),
                    "startColumnIndex": 0,
                    "endColumnIndex": 12
                },
                "cell": {
                    "userEnteredFormat": {
                        "wrapStrategy": "WRAP",
                        "verticalAlignment": "TOP",
                        "textFormat": {
                            "fontSize": 10
                        }
                    }
                },
                "fields": "userEnteredFormat(wrapStrategy,verticalAlignment,textFormat.fontSize)"
            }
        },
        # Center Align Col 0 (Video #) & Col 1 (Date) & Col 4 (Status)
        {
            "repeatCell": {
                "range": {
                    "sheetId": new_sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(all_rows),
                    "startColumnIndex": 0,
                    "endColumnIndex": 2
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment,textFormat.bold)"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": new_sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(all_rows),
                    "startColumnIndex": 4,
                    "endColumnIndex": 5
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment,textFormat.bold)"
            }
        },
        # Bold Col 2 (Format) & Col 5 (Text Hook)
        {
            "repeatCell": {
                "range": {
                    "sheetId": new_sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(all_rows),
                    "startColumnIndex": 2,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(textFormat.bold)"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": new_sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": len(all_rows),
                    "startColumnIndex": 5,
                    "endColumnIndex": 6
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(textFormat.bold)"
            }
        }
    ]

    # Custom column pixel widths
    # Col 0 (Video #): 90px
    # Col 1 (Date & Time): 180px
    # Col 2 (Format): 170px
    # Col 3 (Pillar): 220px
    # Col 4 (Status): 140px
    # Col 5 (Text Hook): 240px
    # Col 6 (Verbal Hook): 280px
    # Col 7 (Full Script): 500px
    # Col 8 (Visual Cues): 280px
    # Col 9 (Caption & Hashtags): 320px
    # Col 10 (CTA): 240px
    # Col 11 (File Path): 220px
    column_widths = [90, 180, 170, 220, 140, 240, 280, 500, 280, 320, 240, 220]
    for col_idx, width in enumerate(column_widths):
        format_requests.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": new_sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": col_idx,
                    "endIndex": col_idx + 1
                },
                "properties": {
                    "pixelSize": width
                },
                "fields": "pixelSize"
            }
        })

    # Execute formatting batch
    print("Applying styling, column widths, text wrapping, and frozen header row...")
    batch_update_spreadsheet(sheet_id, format_requests, token)
    print("Formatting applied successfully.")

    print(f"\nSUCCESS! Tab '{tab_name}' populated and styled at:")
    print(f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid={new_sheet_id}")

if __name__ == "__main__":
    main()
