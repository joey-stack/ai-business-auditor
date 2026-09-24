#!/usr/bin/env python3
"""
Create Gmail Drafts in [Gmail]/Drafts via IMAP.
This places the exact outreach emails for Cosgrove, Brains & Hammers, and Bilaad Realty
directly into the user's Gmail account (visible instantly on mobile & desktop).
The user can either tap 'Schedule Send' inside Gmail for 8:45 AM WAT,
or let the automated cloud scheduler dispatch them.
"""

import sys, imaplib, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

import tools.sync_to_google_drive_and_sheets as s

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

env = s.load_env()
user = env['SMTP_USER']
pwd = env['SMTP_PASSWORD']
sender_name = env.get('SENDER_NAME', 'Joel Adawah Sani')

DRAFTS = [
    {
        "name": "Cosgrove Investment Limited",
        "to": "sales@cosgroveafrica.com",
        "cc": "info@cosgroveafrica.com",
        "subject": "off-hours diaspora speed-to-lead on katampe & maitama",
        "body": """Umar,

Noticed Cosgrove leads West Africa in IoT smart estate engineering across Katampe and Maitama.

However, when high-net-worth diaspora buyers in the US and UK reach out after hours, inquiries wait 8 to 14 hours for an initial response. In luxury property, that latency leaks an estimated $60,000+ a month in unbooked site inspections to competing developers.

Put together a 2-minute diagnostic showing how a 24/7 AI Concierge qualifies international budgets and books virtual inspections in under 60 seconds.

Worth a look?

Joel Adawah Sani
Independent Systems & Automation Consultant
Abuja, Nigeria | +234 707 378 7442

Kubwa, Abuja, FCT, Nigeria
Reply "unsubscribe" to opt out immediately."""
    },
    {
        "name": "Brains & Hammers",
        "to": "sales@brainsandhammers.com",
        "cc": "info@brainsandhammers.com",
        "subject": "life camp lead triage & resident line congestion",
        "body": """Muktari,

Delivering over 10,000 residential units across Nigeria is an incredible achievement for Brains & Hammers.

However, pooling all 8 active developments into one central desk creates a 48-hour routing delay, while resident facility calls tie up phone lines meant for new buyers. Our diagnostic indicates decoupling resident support and automating estate routing recovers over $80,000 a month in accelerated reservation velocity.

Put together a 2-minute overview of the routing architecture.

Open to seeing the breakdown?

Joel Adawah Sani
Independent Systems & Automation Consultant
Abuja, Nigeria | +234 707 378 7442

Kubwa, Abuja, FCT, Nigeria
Reply "unsubscribe" to opt out immediately."""
    },
    {
        "name": "Bilaad Realty",
        "to": "sales@bilaadnigeria.com",
        "cc": "info@bilaadnigeria.com",
        "subject": "international investor speed-to-lead on the bahamas",
        "body": """Aliyu,

Bilaad's sustainable eco-luxury architecture on The Bahamas in Maitama II is one of the most compelling concepts in Abuja.

However, when international diaspora buyers reach out across US and UK time zones, inquiries face a 6 to 12-hour response lag with zero automated title or payment schedule dispatch.

Put together a 2-minute brief showing how automated 24/7 qualification delivers pre-vetted buyers and verified virtual walkthroughs in under 60 seconds.

Worth a brief look?

Joel Adawah Sani
Independent Systems & Automation Consultant
Abuja, Nigeria | +234 707 378 7442

Kubwa, Abuja, FCT, Nigeria
Reply "unsubscribe" to opt out immediately."""
    }
]

print("=== CREATING GMAIL DRAFTS VIA IMAP ===")
mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
mail.login(user, pwd)

for d in DRAFTS:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = d["subject"]
    msg["From"] = formataddr((sender_name, user))
    msg["To"] = d["to"]
    if d.get("cc"):
        msg["Cc"] = d["cc"]
    msg["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    part = MIMEText(d["body"], "plain", "utf-8")
    msg.attach(part)
    
    # Flags: \Draft
    mail.append('"[Gmail]/Drafts"', '(\\Draft)', imaplib.Time2Internaldate(time.time()), msg.as_bytes())
    print(f"✓ Created Draft for {d['name']} -> To: {d['to']} | Subject: {d['subject']}")

print("\n✓ ALL 3 DRAFTS SUCCESSFULLY PLACED IN YOUR GMAIL DRAFTS FOLDER!")
