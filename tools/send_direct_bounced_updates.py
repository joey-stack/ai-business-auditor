#!/usr/bin/env python3
"""
Dispatch Touch 1 outreach emails to verified direct inboxes:
- Clarke Kent Plumbing -> dispatch@clarkekentplumbing.com
- Plumbing Outfitters -> info@plumbingoutfitters.com
"""

import sys, time
from pathlib import Path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

import tools.sync_to_google_drive_and_sheets as s
from tools.schedule_outreach_dispatcher import send_smtp_email, log_touch, update_google_sheet_status
from tools.sync_all_pipeline_leads import LEADS
from tools.schedule_outreach_dispatcher import get_lead_email_task

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

env = s.load_env()
smtp_cfg = {
    "host": env.get("SMTP_HOST", "smtp.gmail.com"),
    "port": int(env.get("SMTP_PORT", 587)),
    "user": env.get("SMTP_USER"),
    "password": env.get("SMTP_PASSWORD"),
    "sender_email": env.get("SMTP_USER"),
    "sender_name": env.get("SENDER_NAME", "Joel Adawah Sani")
}

sheet_id = env.get("GOOGLE_SHEET_ID")
token = None
if sheet_id:
    try:
        token = s.get_access_token(env['GOOGLE_CLIENT_ID'], env['GOOGLE_CLIENT_SECRET'], env['GOOGLE_REFRESH_TOKEN'])
    except Exception as e:
        print("Sheet token warning:", e)

# Target updates
updates = [
    {
        "lead_idx": 4, # Plumbing Outfitters (Row 5 in Sheet)
        "new_email": "info@plumbingoutfitters.com",
        "name": "Plumbing Outfitters",
        "slug": "plumbing-outfitters",
        "contact": "Warren and Ashley"
    },
    {
        "lead_idx": 5, # Clarke Kent Plumbing (Row 6 in Sheet)
        "new_email": "dispatch@clarkekentplumbing.com",
        "name": "Clarke Kent Plumbing",
        "slug": "clarke-kent-plumbing",
        "contact": "Gary and Cynthia"
    }
]

print("=== DISPATCHING TOUCH 1 TO NEW ACTIVE DIRECT INBOXES ===\n")

for item in updates:
    idx = item["lead_idx"]
    lead = LEADS[idx - 1]
    task = get_lead_email_task(idx, lead)
    
    new_recipient = item["new_email"]
    subject = task["subject"]
    body = task["body"]
    
    print(f"Sending to {item['name']} ({new_recipient})...")
    try:
        send_smtp_email(smtp_cfg, new_recipient, item["contact"], subject, body)
        print(f"  ✓ Dispatched successfully to {new_recipient}")
        
        # Log touch
        log_touch(item["name"], item["slug"], subject, result="no_reply")
        print(f"  ✓ Logged touch to outreach_outcomes.csv")
        
        # Update sheet row
        if sheet_id and token:
            row_idx = idx + 1
            update_google_sheet_status(sheet_id, token, row_idx, status="Touch 1 Sent (Direct Inbox)", next_action="Follow up in 3 days")
            print(f"  ✓ Updated Google Sheet row {row_idx} (Col L='Touch 1 Sent (Direct Inbox)')")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        
    time.sleep(2)

print("\n✓ DISPATCH TO NEW DIRECT INBOXES COMPLETED!")
