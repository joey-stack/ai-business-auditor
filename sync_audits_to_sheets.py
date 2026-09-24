#!/usr/bin/env python3
"""
Sync Audited Prospects to Google Sheets
Directly synchronizes all audited clients under outputs/clients/ into the
Outreach Pipeline Google Sheet using Google Sheets REST API v4.
"""
import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

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
    try:
        with urllib.request.urlopen(req) as resp:
            tokens = json.loads(resp.read().decode("utf-8"))
            return tokens.get("access_token"), tokens.get("scope", "")
    except Exception as e:
        print(f"Error obtaining access token: {e}")
        return None, ""

def update_sheet_values(sheet_id, range_a1, values, access_token):
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
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code} updating {range_a1}: {err_body}")
        return None
    except Exception as e:
        print(f"Error updating {range_a1}: {e}")
        return None

def main():
    env = load_env()
    client_id = env.get("GOOGLE_CLIENT_ID")
    client_secret = env.get("GOOGLE_CLIENT_SECRET")
    refresh_token = env.get("GOOGLE_REFRESH_TOKEN")
    sheet_id = env.get("GOOGLE_SHEET_ID")

    if not all([client_id, client_secret, refresh_token, sheet_id]):
        print("Missing credentials or GOOGLE_SHEET_ID in .env")
        sys.exit(1)

    print(f"Target Sheet ID: {sheet_id}")
    access_token, scope = get_access_token(client_id, client_secret, refresh_token)
    if not access_token:
        print("Failed to authenticate.")
        sys.exit(1)

    if "spreadsheets" not in scope:
        print("\n" + "!" * 70)
        print("PERMISSION REQUIRED:")
        print("Your Google OAuth token does not yet have 'spreadsheets' permission.")
        print("Current granted scope:", scope)
        print("\nTo grant Google Sheets permission:")
        print("  1. Run: python get_gsc_refresh_token.py")
        print("  2. Click 'Allow' in the browser window that opens.")
        print("  3. Re-run: python sync_audits_to_sheets.py")
        print("!" * 70 + "\n")
        sys.exit(2)

    headers = [
        "Business Name", "Location", "Opportunity Score", "Tier",
        "Audit PDF Link", "Video Walkthrough Link", "Call Script Link",
        "Suggested Opening Line", "Contact Name", "Contact Title",
        "LinkedIn Profile URL", "Outreach Status", "Touch 1 Date",
        "Touch 2 Date", "Touch 3 Date", "Last Touch Result", "Next Action", "Notes"
    ]

    rows = [
        [
            "Austin Plumbing®", "Austin, TX", 85, "Tier B",
            "outputs/clients/austin-plumbing/audit_2026-09-19.pdf",
            "outputs/clients/austin-plumbing/walkthrough.mp4",
            "outputs/clients/austin-plumbing/call_script.md",
            "4.8★ with only 21 reviews vs 4,500+ competitor avg; 6.9s mobile load latency; deploy SMS review capture & fast mobile landing page",
            "Chesley Shapiro & Cody Herchberger", "Owner / Operators",
            "https://www.linkedin.com/company/austin-plumbing"
        ],
        [
            "Austin's Greatest Plumbing", "Austin, TX", 82, "Tier C",
            "outputs/clients/austins-greatest-plumbing/audit_2026-09-15.pdf", "",
            "outputs/clients/austins-greatest-plumbing/call_script.md",
            "4.9★ with 68 reviews; missing instant online booking engine; unindexed booking subpage",
            "Rachel Humphreys", "Owner & Principal",
            ""
        ],
        [
            "Cold Is On The Right Plumbing & Air", "Austin, TX (Lakeway)", 80, "Tier B",
            "outputs/clients/cold-is-on-the-right-plumbing-air/audit_2026-09-15.pdf", "",
            "outputs/clients/cold-is-on-the-right-plumbing-air/call_script.md",
            "4.8★ across 292 reviews; dual-trade HVAC + plumbing silos without cross-sell membership engine; missing 24/7 emergency triage",
            "Brendin Dittman", "Owner & Master Plumber",
            "https://www.linkedin.com/company/cold-is-on-the-right"
        ],
        [
            "Plumbing Outfitters", "Austin, TX", 74, "Tier A",
            "outputs/clients/plumbing-outfitters/audit_2026-09-15.pdf", "",
            "outputs/clients/plumbing-outfitters/call_script.md",
            "4.7★ across 314 reviews; commercial multi-family maintenance contracts under-promoted; missing commercial quote estimator",
            "Warren & Ashley Stroud", "Co-Founders (Master Plumber & COO)",
            "https://www.linkedin.com/company/plumbing-outfitters"
        ],
        [
            "Clarke Kent Plumbing", "Austin, TX", 86, "Tier C",
            "outputs/clients/clarke-kent-plumbing/audit_2026-09-15.pdf", "",
            "outputs/clients/clarke-kent-plumbing/call_script.md",
            "4.9★ with 38 reviews; weak emergency CTA; missing automated follow-up for estimate requests",
            "Gary Hacker & Cynthia Clarke", "President & Vice President",
            "https://www.linkedin.com/company/clarke-kent-plumbing"
        ],
        [
            "Wisdom Kwati Smart City Plc", "Abuja, Nigeria", 78, "Tier A",
            "outputs/clients/wisdom-kwati-smart-city-plc/audit_2026-09-15.pdf", "",
            "outputs/clients/wisdom-kwati-smart-city-plc/call_script.md",
            "Smart city IoT platform infrastructure; investor portal friction; multi-currency payment integration",
            "Wisdom Kwati", "Chairman & CEO",
            "https://www.linkedin.com/company/wisdomkwatismartcity"
        ],
        [
            "LEE Investment Handlers", "Lagos, Nigeria & Venice, Italy", 76, "Tier B",
            "outputs/clients/lee-investment-handlers/audit_2026-09-15.pdf", "",
            "outputs/clients/lee-investment-handlers/call_script.md",
            "Client onboarding document friction; portfolio report automation; wealth portal security audit",
            "Uyi Loveday E.", "Founder & CEO",
            ""
        ]
    ]

    print("Writing Row 1 Headers (A1:R1)...")
    res1 = update_sheet_values(sheet_id, "A1:R1", [headers], access_token)
    if not res1:
        # Fallback to Sheet1 or first sheet title if named differently
        res1 = update_sheet_values(sheet_id, "Sheet1!A1:R1", [headers], access_token)

    print("Writing Audited Prospects to Columns A2:K8...")
    res2 = update_sheet_values(sheet_id, "A2:K8", rows, access_token)
    if not res2:
        res2 = update_sheet_values(sheet_id, "Sheet1!A2:K8", rows, access_token)

    if res1 and res2:
        print("\nSUCCESS! Synchronized all 7 audited prospects to your Google Sheet.")
        print(f"Spreadsheet URL: https://docs.google.com/spreadsheets/d/{sheet_id}/edit")

if __name__ == "__main__":
    main()
