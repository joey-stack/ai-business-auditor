#!/usr/bin/env python3
"""
Syncs client audit PDFs, video walkthroughs, and outreach strategy PDFs to Google Drive,
and updates the 'Outreach Pipeline' Google Sheet with direct clickable Google Drive links
and ready-to-send outreach copy.
"""
import os
import sys
import io
import re
import json
from pathlib import Path

# Fix Windows cp1252 unicode print crashes
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import tools.sync_to_google_drive_and_sheets as s

CLIENTS = [
    {
        "row_idx": 2,
        "name": "Austin Plumbing®",
        "folder_name": "Austin Plumbing",
        "slug": "austin-plumbing",
        "audit_file": "audit_2026-09-19.pdf",
    },
    {
        "row_idx": 3,
        "name": "Austin's Greatest Plumbing",
        "folder_name": "Austin's Greatest Plumbing",
        "slug": "austins-greatest-plumbing",
        "audit_file": "audit_2026-09-15.pdf",
    },
    {
        "row_idx": 4,
        "name": "Cold Is On The Right Plumbing & Air",
        "folder_name": "Cold Is On The Right Plumbing & Air",
        "slug": "cold-is-on-the-right-plumbing-air",
        "audit_file": "audit_2026-09-15.pdf",
    },
    {
        "row_idx": 5,
        "name": "Plumbing Outfitters",
        "folder_name": "Plumbing Outfitters",
        "slug": "plumbing-outfitters",
        "audit_file": "audit_2026-09-15.pdf",
    },
    {
        "row_idx": 6,
        "name": "Clarke Kent Plumbing",
        "folder_name": "Clarke Kent Plumbing",
        "slug": "clarke-kent-plumbing",
        "audit_file": "audit_2026-09-15.pdf",
    },
    {
        "row_idx": 7,
        "name": "Wisdom Kwati Smart City Plc",
        "folder_name": "Wisdom Kwati Smart City Plc",
        "slug": "wisdom-kwati-smart-city-plc",
        "audit_file": "audit_2026-09-15.pdf",
    },
    {
        "row_idx": 8,
        "name": "LEE Investment Handlers",
        "folder_name": "LEE Investment Handlers",
        "slug": "lee-investment-handlers",
        "audit_file": "audit_2026-09-15.pdf",
    },
]

def parse_outreach_copy(slug: str):
    """Extracts clean primary and secondary outreach copy without raw markdown syntax or slop."""
    try:
        from tools.clean_outreach_copy import OUTREACH_DATA
        for biz in OUTREACH_DATA:
            if biz["slug"] == slug:
                return biz["primary_copy"], biz["secondary_copy"]
    except Exception:
        pass
    
    md_path = ROOT_DIR / "outputs" / "clients" / slug / "outreach.md"
    if not md_path.exists():
        return "", ""
    content = md_path.read_text(encoding="utf-8")
    
    parts = content.split("--------------------------------------------------------------------------------")
    primary = parts[2].strip() if len(parts) > 2 else ""
    secondary = parts[4].strip() if len(parts) > 4 else ""
    return primary, secondary

def sync_outreach_pipeline():
    env = s.load_env()
    client_id = env["GOOGLE_CLIENT_ID"]
    client_secret = env["GOOGLE_CLIENT_SECRET"]
    refresh_token = env["GOOGLE_REFRESH_TOKEN"]
    sheet_id = env.get("GOOGLE_SHEET_ID")

    print("==================================================================", flush=True)
    print("OUTREACH PIPELINE — GOOGLE DRIVE ASSET SYNC & SPREADSHEET ENRICHER", flush=True)
    print("==================================================================", flush=True)

    print("\n[1/4] Authenticating with Google APIs...", flush=True)
    token = s.get_access_token(client_id, client_secret, refresh_token)
    print("✓ Access token generated.", flush=True)

    print("\n[2/4] Verifying Master & Client Folders in Google Drive...", flush=True)
    root_id, root_link = s.find_or_create_folder("AI Business Auditor - Social Content / Joel Adawah Sani", None, token)
    s.set_shareable_permission(root_id, token)

    clients_master_folder_id, clients_master_link = s.find_or_create_folder("Audited Clients & Outreach Dossiers", root_id, token)
    s.set_shareable_permission(clients_master_folder_id, token)
    print(f"✓ Audited Clients Drive Folder: {clients_master_link}", flush=True)

    print("\n[3/4] Uploading Audit PDFs, Walkthrough Videos & Outreach PDFs...", flush=True)
    updated_rows_efg = [] # [audit_link, video_link, outreach_link]
    updated_rows_st = []  # [primary_copy, secondary_copy]

    for biz in CLIENTS:
        slug = biz["slug"]
        print(f"\n--> Processing {biz['name']} ({slug})...", flush=True)
        
        # 1. Create client folder
        cf_id, cf_link = s.find_or_create_folder(biz["folder_name"], clients_master_folder_id, token)
        s.set_shareable_permission(cf_id, token)

        base_dir = ROOT_DIR / "outputs" / "clients" / slug
        audit_pdf = base_dir / biz["audit_file"]
        video_mp4 = base_dir / "walkthrough.mp4"
        outreach_pdf = base_dir / "outreach.pdf"
        outreach_md = base_dir / "outreach.md"

        audit_url = ""
        video_url = ""
        outreach_url = ""

        # Upload Audit PDF
        if audit_pdf.exists():
            up_audit = s.upload_file_smart(audit_pdf, cf_id, token)
            audit_url = up_audit.get("webViewLink", "")
            print(f"    ✓ Audit PDF: {audit_url}", flush=True)
        else:
            print(f"    ⚠ Audit PDF not found: {audit_pdf}", flush=True)

        # Upload Video Walkthrough
        if video_mp4.exists():
            up_vid = s.upload_file_smart(video_mp4, cf_id, token)
            video_url = up_vid.get("webViewLink", "")
            print(f"    ✓ Video Walkthrough: {video_url}", flush=True)
        else:
            print(f"    ⚠ Video not found: {video_mp4}", flush=True)

        # Upload Outreach PDF
        if outreach_pdf.exists():
            up_outreach = s.upload_file_smart(outreach_pdf, cf_id, token)
            outreach_url = up_outreach.get("webViewLink", "")
            print(f"    ✓ Outreach Strategy & Script PDF: {outreach_url}", flush=True)
        elif outreach_md.exists():
            up_md = s.upload_file_smart(outreach_md, cf_id, token)
            outreach_url = up_md.get("webViewLink", "")
            print(f"    ✓ Outreach Markdown: {outreach_url}", flush=True)

        # Also upload outreach.md to client folder for convenience
        if outreach_md.exists():
            s.upload_file_smart(outreach_md, cf_id, token)

        # Build Sheet Formulas
        cell_e = f'=HYPERLINK("{audit_url}", "📄 View Audit PDF")' if audit_url else ""
        cell_f = f'=HYPERLINK("{video_url}", "▶ View Walkthrough Video")' if video_url else ""
        cell_g = f'=HYPERLINK("{outreach_url}", "📄 View Outreach Strategy & Script PDF")' if outreach_url else ""
        updated_rows_efg.append([cell_e, cell_f, cell_g])

        # Parse copy for Columns S & T
        primary_copy, secondary_copy = parse_outreach_copy(slug)
        updated_rows_st.append([primary_copy, secondary_copy])

    # 4. Update Google Sheet
    if sheet_id:
        print("\n==================================================================", flush=True)
        print("[4/4] UPDATING GOOGLE SPREADSHEET 'Outreach Pipeline' TAB...", flush=True)
        print("==================================================================", flush=True)

        s.ensure_sheet_columns(sheet_id, token, 20)

        # Update Columns E, F, G (Rows 2 to 8)
        range_efg = "Outreach Pipeline!E2:G8"
        s.update_sheet_range(sheet_id, range_efg, updated_rows_efg, token)
        print(f"✓ Updated {range_efg} with direct clickable Google Drive links!", flush=True)

        # Update Columns S & T Headers (Row 1)
        range_st_header = "Outreach Pipeline!S1:T1"
        st_headers = [["Ready-to-Send Outreach Copy (Primary Channel)", "Ready-to-Send Outreach Copy (Secondary Channel)"]]
        s.update_sheet_range(sheet_id, range_st_header, st_headers, token)

        # Update Columns S & T Data (Rows 2 to 8)
        range_st_data = "Outreach Pipeline!S2:T8"
        s.update_sheet_range(sheet_id, range_st_data, updated_rows_st, token)
        print(f"✓ Updated {range_st_data} with ready-to-send outreach copy (Columns S & T)!", flush=True)

    print("\n==================================================================", flush=True)
    print("SUCCESS: ALL 7 CLIENTS FULLY SYNCED TO GOOGLE DRIVE & OUTREACH PIPELINE!", flush=True)
    print(f"Drive Folder: {clients_master_link}", flush=True)
    print("==================================================================", flush=True)

if __name__ == "__main__":
    sync_outreach_pipeline()
