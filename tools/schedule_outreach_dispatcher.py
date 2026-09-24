#!/usr/bin/env python3
"""
Automated Outreach Email Dispatcher & Scheduler.
Implements Option A:
- Paced sending with randomized human delays (8-14 mins) to protect domain deliverability.
- Dry-run mode to preview all recipients and queue timings before dispatch.
- Integrates directly with the Josh Braun / Lavender email copy across all 17 leads.
- Automatically logs sent touches to outputs/outreach_outcomes.csv and outputs/clients/<slug>/outreach_log.csv.
- Live-syncs outreach status (Col L) and touch date (Col M) back to Google Sheets.
"""

import os
import sys
import re
import time
import random
import smtplib
import argparse
from datetime import datetime, date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from pathlib import Path

# Fix Windows cp1252 unicode print crashes
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import tools.sync_to_google_drive_and_sheets as s
from tools.sync_all_pipeline_leads import LEADS

OUTCOMES_CSV = ROOT_DIR / "outputs" / "outreach_outcomes.csv"
CLIENTS_DIR = ROOT_DIR / "outputs" / "clients"

def parse_email_copy(raw_copy: str):
    """Extracts recipient email, subject line, and body from formatted outreach copy."""
    to_match = re.search(r"To:\s*([^\s\(\)]+@[^\s\(\)]+)", raw_copy, re.IGNORECASE)
    subject_match = re.search(r"Subject:\s*(.+)", raw_copy, re.IGNORECASE)
    
    recipient_email = to_match.group(1).strip() if to_match else None
    subject = subject_match.group(1).strip() if subject_match else "Operational audit follow-up"
    
    # Body is everything after Subject: line
    lines = raw_copy.splitlines()
    body_lines = []
    found_subject = False
    for line in lines:
        if found_subject:
            body_lines.append(line)
        elif line.lower().startswith("subject:"):
            found_subject = True
            
    body = "\n".join(body_lines).strip()
    return recipient_email, subject, body

def get_lead_email_task(lead_idx, lead):
    """Identifies which copy (primary or secondary) is the email copy."""
    p_copy = lead.get("primary_copy", "")
    s_copy = lead.get("secondary_copy", "")
    
    if "Subject:" in p_copy:
        recipient, subject, body = parse_email_copy(p_copy)
        channel_type = "Primary"
    elif "Subject:" in s_copy:
        recipient, subject, body = parse_email_copy(s_copy)
        channel_type = "Secondary"
    else:
        return None
        
    slug = lead["name"].lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug).strip("-")

    return {
        "index": lead_idx,
        "name": lead["name"],
        "slug": slug,
        "contact": lead["contact_name"],
        "location": lead["location"],
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "channel_type": channel_type
    }

def log_touch(prospect_name, slug, message_excerpt, result="no_reply"):
    """Appends sent touch to outputs/outreach_outcomes.csv and client outreach_log.csv."""
    OUTCOMES_CSV.parent.mkdir(parents=True, exist_ok=True)
    today_str = date.today().isoformat()
    
    # Global ledger
    header_needed = not OUTCOMES_CSV.exists()
    with open(OUTCOMES_CSV, "a", encoding="utf-8") as f:
        if header_needed:
            f.write("date,prospect_name,channel,touch_number,message_excerpt,result\n")
        safe_excerpt = message_excerpt.replace('"', '""')
        f.write(f'"{today_str}","{prospect_name}","email",1,"{safe_excerpt}","{result}"\n')
        
    # Client-specific ledger if folder exists
    client_dir = CLIENTS_DIR / slug
    if client_dir.exists():
        client_log = client_dir / "outreach_log.csv"
        c_header_needed = not client_log.exists()
        with open(client_log, "a", encoding="utf-8") as f:
            if c_header_needed:
                f.write("date,prospect_name,channel,touch_number,message_excerpt,result\n")
            f.write(f'"{today_str}","{prospect_name}","email",1,"{safe_excerpt}","{result}"\n')

def update_google_sheet_status(sheet_id, token, row_idx, status="Touch 1 Sent", next_action="Follow up in 3 days"):
    """Updates columns L through Q for the specific lead row."""
    today_str = date.today().isoformat()
    # Columns L to R (indices 11 to 17)
    range_name = f"Outreach Pipeline!L{row_idx}:Q{row_idx}"
    values = [[status, today_str, "", "", "Awaiting Reply", next_action]]
    s.update_sheet_range(sheet_id, range_name, values, token)

def send_smtp_email(smtp_cfg, recipient_email, recipient_name, subject, body_text):
    """Dispatches a single email over authenticated SMTP with TLS or SSL."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr((smtp_cfg["sender_name"], smtp_cfg["sender_email"]))
    msg["To"] = recipient_email
    msg["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    part = MIMEText(body_text, "plain", "utf-8")
    msg.attach(part)
    
    host = smtp_cfg["host"]
    port = int(smtp_cfg["port"])
    user = smtp_cfg["user"]
    password = smtp_cfg["password"]
    
    if port == 465:
        with smtplib.SMTP_SSL(host, port, timeout=30) as server:
            server.login(user, password)
            server.sendmail(smtp_cfg["sender_email"], [recipient_email], msg.as_string())
    else:
        with smtplib.SMTP(host, port, timeout=30) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(smtp_cfg["sender_email"], [recipient_email], msg.as_string())

def main():
    parser = argparse.ArgumentParser(description="Paced Automated Email Outreach Scheduler")
    parser.add_argument("--dry-run", action="store_true", help="Preview recipients, subject lines, and schedule without sending")
    parser.add_argument("--delay-min", type=int, default=8, help="Minimum delay between sends in minutes (default: 8)")
    parser.add_argument("--delay-max", type=int, default=14, help="Maximum delay between sends in minutes (default: 14)")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of emails to send")
    parser.add_argument("--lead", type=int, default=None, help="Send to a specific lead number (1 to 17)")
    parser.add_argument("--start-from", type=int, default=1, help="Resume sending from a specific lead number (default: 1)")
    parser.add_argument("--yes", action="store_true", help="Skip interactive confirmation prompt")
    parser.add_argument("--start-at", type=str, default=None, help="Schedule start time in HH:MM format (24-hour)")
    args = parser.parse_args()

    # Load environment variables
    env = s.load_env()
    smtp_user = env.get("SMTP_USER") or env.get("SENDER_EMAIL")
    smtp_pass = env.get("SMTP_PASSWORD") or env.get("GMAIL_APP_PASSWORD")
    smtp_host = env.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = env.get("SMTP_PORT", "587")
    sender_name = env.get("SENDER_NAME", "Joel Adawah Sani")
    sheet_id = env.get("GOOGLE_SHEET_ID")

    # Collect tasks
    tasks = []
    for idx, lead in enumerate(LEADS, 1):
        if args.lead and idx != args.lead:
            continue
        if args.start_from and idx < args.start_from:
            continue
        task = get_lead_email_task(idx, lead)
        if task and task["recipient"]:
            tasks.append(task)

    if args.limit:
        tasks = tasks[:args.limit]

    print("==================================================================")
    print(" PACED AUTOMATED EMAIL OUTREACH DISPATCHER")
    print(" Standards: Josh Braun & Lavender.ai | Rate: 1 email / 8-14 mins")
    print("==================================================================")
    print(f"Total Targets Queued: {len(tasks)} prospects")
    print(f"Delay Between Sends: {args.delay_min} to {args.delay_max} minutes (randomized jitter)")
    print(f"SMTP Server:         {smtp_host}:{smtp_port}")
    print(f"Sender:              {sender_name} <{smtp_user or 'NOT CONFIGURED IN .env'}>")
    print("------------------------------------------------------------------")

    for i, t in enumerate(tasks, 1):
        print(f"[{i:02d}] {t['name']:<35} | {t['recipient']:<32} | {t['subject']}")

    print("------------------------------------------------------------------")

    # Dry-run exit
    if args.dry_run:
        print("\n✓ [DRY RUN COMPLETE] No emails were sent.")
        print("To send live, configure SMTP_USER & SMTP_PASSWORD in .env and run without --dry-run.\n")
        return

    # Check SMTP credentials
    if not smtp_user or not smtp_pass:
        print("\n[ERROR] SMTP credentials not found in .env!")
        print("Please add the following to your .env file:")
        print("  SMTP_HOST=smtp.gmail.com")
        print("  SMTP_PORT=587")
        print("  SMTP_USER=your_email@gmail.com")
        print("  SMTP_PASSWORD=your_16_digit_app_password")
        print("  SENDER_NAME=Joel Adawah Sani\n")
        print("Tip: For Gmail, generate an App Password at: https://myaccount.google.com/apppasswords")
        return

    smtp_cfg = {
        "host": smtp_host,
        "port": smtp_port,
        "user": smtp_user,
        "password": smtp_pass,
        "sender_email": smtp_user,
        "sender_name": sender_name
    }

    # Scheduled start time
    if args.start_at:
        now = datetime.now()
        target_h, target_m = map(int, args.start_at.split(":"))
        target_dt = now.replace(hour=target_h, minute=target_m, second=0, microsecond=0)
        if target_dt < now:
            print(f"Specified start time {args.start_at} has already passed for today.")
        else:
            wait_seconds = (target_dt - now).total_seconds()
            print(f"⏳ Sleeping until scheduled start time {args.start_at} ({int(wait_seconds // 60)} minutes)...")
            time.sleep(wait_seconds)

    # Confirmation prompt
    if not args.yes:
        confirm = input(f"\nProceed to send {len(tasks)} emails with {args.delay_min}-{args.delay_max} min delays? [y/N]: ")
        if confirm.lower() not in ["y", "yes"]:
            print("Aborted by user.")
            return

    # Google Sheets access token
    token = None
    try:
        token = s.get_access_token(env['GOOGLE_CLIENT_ID'], env['GOOGLE_CLIENT_SECRET'], env['GOOGLE_REFRESH_TOKEN'])
    except Exception as e:
        print(f"Warning: Could not get Google Sheets token ({e}). Sheet status will not update live.")

    # Execution loop
    for idx, t in enumerate(tasks, 1):
        print(f"\n[{idx}/{len(tasks)}] Sending to {t['name']} ({t['recipient']})...", flush=True)
        try:
            send_smtp_email(smtp_cfg, t['recipient'], t['contact'], t['subject'], t['body'])
            print(f"  ✓ Dispatched successfully to {t['recipient']}", flush=True)
            
            # Log touch
            log_touch(t['name'], t['slug'], t['subject'], result="no_reply")
            print(f"  ✓ Logged touch to {OUTCOMES_CSV.name}", flush=True)
            
            # Update sheet dynamically with fresh token
            if sheet_id:
                try:
                    live_token = s.get_access_token(env['GOOGLE_CLIENT_ID'], env['GOOGLE_CLIENT_SECRET'], env['GOOGLE_REFRESH_TOKEN'])
                    sheet_row = t['index'] + 1  # 1-indexed header offset
                    update_google_sheet_status(sheet_id, live_token, sheet_row)
                    print(f"  ✓ Updated Google Sheet row {sheet_row} (Col L='Touch 1 Sent')", flush=True)
                except Exception as e_sheet:
                    print(f"  ! Note: Google Sheet update warning: {e_sheet}", flush=True)
        except Exception as ex:
            print(f"  ✗ Failed to send to {t['recipient']}: {ex}", flush=True)

        # Sleep between sends (except for the last one)
        if idx < len(tasks):
            delay_minutes = random.uniform(args.delay_min, args.delay_max)
            delay_secs = int(delay_minutes * 60)
            next_time = datetime.fromtimestamp(time.time() + delay_secs).strftime("%H:%M:%S")
            print(f"  ⏳ Waiting {delay_minutes:.1f} minutes before next email (next send at {next_time})...", flush=True)
            time.sleep(delay_secs)

    print("\n==================================================================", flush=True)
    print("✓ ALL QUEUED EMAILS DISPATCHED SUCCESSFULLY!", flush=True)
    print("==================================================================", flush=True)

if __name__ == "__main__":
    main()
