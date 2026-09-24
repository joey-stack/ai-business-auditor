#!/usr/bin/env python3
"""
Append Top 3 Abuja Real Estate leads to Outreach Pipeline Google Sheet.
Adheres strictly to Rule 22:
- Writes exclusively to Columns A through K.
- Preserves Columns L through R.
- Appends to rows 19 through 21.
"""

import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

import tools.sync_to_google_drive_and_sheets as s

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

env = s.load_env()
token = s.get_access_token(env['GOOGLE_CLIENT_ID'], env['GOOGLE_CLIENT_SECRET'], env['GOOGLE_REFRESH_TOKEN'])
sheet_id = env['GOOGLE_SHEET_ID']

NEW_LEADS = [
    [
        "Cosgrove Investment Limited",
        "Maitama / CBD, Abuja, Nigeria",
        "82",
        "Tier 1 (Luxury Smart Home Developer)",
        "outputs/clients/cosgrove-investment-limited/audit_2026-09-24.md",
        "Pending Walkthrough Recording",
        "outputs/clients/cosgrove-investment-limited/call_script.md",
        "Noticed Cosgrove leads in IoT smart estates, but off-hours diaspora inquiries wait 8–14 hours for response.",
        "Umar Abdullahi",
        "Chief Executive Officer",
        "https://www.linkedin.com/company/cosgrove-investment-limited/"
    ],
    [
        "Brains & Hammers",
        "Gudu / Life Camp, Abuja, Nigeria",
        "86",
        "Tier 1 (Mega-Scale Community Developer)",
        "outputs/clients/brains-and-hammers/audit_2026-09-24.md",
        "Pending Walkthrough Recording",
        "outputs/clients/brains-and-hammers/call_script.md",
        "Delivering 10,000 units is massive, but centralized inboxes delay estate-specific buyer routing by 48–72 hours.",
        "Muktari Hashim",
        "Managing Director",
        "https://www.linkedin.com/company/brains-and-hammers/"
    ],
    [
        "Bilaad Realty",
        "CBD / Maitama II, Abuja, Nigeria",
        "84",
        "Tier 1 (Eco-Luxury Property Developer)",
        "outputs/clients/bilaad-realty/audit_2026-09-24.md",
        "Pending Walkthrough Recording",
        "outputs/clients/bilaad-realty/call_script.md",
        "The Bahamas eco-design is premier, but international buyers face 6–12h lag with zero automated title verification.",
        "Aliyu Aliyu",
        "Chief Executive Officer",
        "https://www.linkedin.com/company/bilaad-realty/"
    ]
]

print("=== APPENDING ABUJA REAL ESTATE LEADS TO GOOGLE SHEET (COLS A:K) ===")

range_name = f"Outreach Pipeline!A19:K21"
s.update_sheet_range(sheet_id, range_name, NEW_LEADS, token)
print(f"✓ Successfully appended 3 real estate leads to rows 19–21 in Outreach Pipeline!")
print(f"Spreadsheet Link: https://docs.google.com/spreadsheets/d/{sheet_id}/edit")
