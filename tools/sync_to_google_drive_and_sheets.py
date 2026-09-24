#!/usr/bin/env python3
"""
Sync all social media content folders, videos, carousels, scripts, and lead magnets
to Google Drive, and update Google Sheet tabs with direct Google Drive links.
"""
import os
import sys
import io
import json
import mimetypes
import requests
from pathlib import Path

# Fix Windows cp1252 unicode print crashes
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

OUTPUT_DIR = ROOT_DIR / "outputs"
TIKTOK_DIR = OUTPUT_DIR / "tiktok_content"
LINKEDIN_DIR = OUTPUT_DIR / "linkedin_content"
LEAD_MAGNETS_DIR = OUTPUT_DIR / "lead_magnets"
CLIENTS_DIR = OUTPUT_DIR / "clients"

def load_env():
    p = ROOT_DIR / ".env"
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
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    resp = requests.post(token_url, data=data, timeout=30)
    resp.raise_for_status()
    return resp.json().get("access_token")

# ----------------------------------------------------------------------
# Google Drive API Helpers
# ----------------------------------------------------------------------

def find_or_create_folder(folder_name: str, parent_id: str, access_token: str):
    """Finds existing folder by name and parent or creates a new one."""
    headers = {"Authorization": f"Bearer {access_token}"}
    q = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    if parent_id:
        q += f" and '{parent_id}' in parents"

    url = "https://www.googleapis.com/drive/v3/files"
    params = {"q": q, "fields": "files(id,name,webViewLink)"}
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    if resp.status_code == 200:
        files = resp.json().get("files", [])
        if files:
            link = files[0].get("webViewLink") or f"https://drive.google.com/drive/folders/{files[0]['id']}"
            return files[0]["id"], link

    # Create folder
    create_url = "https://www.googleapis.com/drive/v3/files?fields=id,name,webViewLink"
    metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    if parent_id:
        metadata["parents"] = [parent_id]

    resp = requests.post(create_url, headers=headers, json=metadata, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    folder_id = data["id"]
    link = data.get("webViewLink") or f"https://drive.google.com/drive/folders/{folder_id}"
    return folder_id, link

def set_shareable_permission(file_id: str, access_token: str):
    """Sets file or folder permission so anyone with the link can view."""
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}/permissions"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {"role": "reader", "type": "anyone"}
    try:
        requests.post(url, headers=headers, json=payload, timeout=15)
    except Exception:
        pass

def upload_file_smart(local_file_path: Path, parent_id: str, access_token: str) -> dict:
    """
    Uploads a file to Google Drive.
    - If already present in folder, reuses existing file and returns metadata.
    - If small (< 4 MB), uploads via multipart in 1 request.
    - If large (>= 4 MB), uploads via resumable chunked upload with progress display.
    """
    filename = local_file_path.name
    file_size = local_file_path.stat().st_size
    mime_type, _ = mimetypes.guess_type(str(local_file_path))
    if not mime_type:
        mime_type = "application/octet-stream"

    headers = {"Authorization": f"Bearer {access_token}"}

    # 1. Check if file already exists in parent
    q = f"name = '{filename}' and '{parent_id}' in parents and trashed = false"
    url = "https://www.googleapis.com/drive/v3/files"
    params = {"q": q, "fields": "files(id,name,webViewLink,size)"}
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    if resp.status_code == 200:
        files = resp.json().get("files", [])
        if files:
            f = files[0]
            link = f.get("webViewLink") or f"https://drive.google.com/file/d/{f['id']}/view?usp=drivesdk"
            f["webViewLink"] = link
            return f

    # 2. Upload
    if file_size < 4 * 1024 * 1024:
        # Multipart / single request upload
        upload_url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,webViewLink"
        metadata = {
            "name": filename,
            "parents": [parent_id]
        }
        with open(local_file_path, "rb") as f_data:
            files_payload = {
                "data": ("metadata", json.dumps(metadata), "application/json; charset=UTF-8"),
                "file": (filename, f_data, mime_type)
            }
            resp = requests.post(
                upload_url,
                headers={"Authorization": f"Bearer {access_token}"},
                files=files_payload,
                timeout=60
            )
            resp.raise_for_status()
            data = resp.json()
            if not data.get("webViewLink"):
                data["webViewLink"] = f"https://drive.google.com/file/d/{data['id']}/view?usp=drivesdk"
            set_shareable_permission(data["id"], access_token)
            return data
    else:
        # Chunked Resumable Upload
        init_url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&fields=id,name,webViewLink"
        init_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": mime_type,
            "X-Upload-Content-Length": str(file_size)
        }
        metadata = {"name": filename, "parents": [parent_id]}
        init_resp = requests.post(init_url, headers=init_headers, json=metadata, timeout=30)
        init_resp.raise_for_status()
        upload_location = init_resp.headers["Location"]

        chunk_size = 8 * 1024 * 1024
        print(f"    -> Uploading {filename} ({file_size / 1024 / 1024:.1f} MB) in chunks...", flush=True)
        with open(local_file_path, "rb") as f_data:
            byte_start = 0
            while byte_start < file_size:
                chunk = f_data.read(chunk_size)
                byte_end = byte_start + len(chunk) - 1
                chunk_headers = {
                    "Content-Length": str(len(chunk)),
                    "Content-Range": f"bytes {byte_start}-{byte_end}/{file_size}"
                }
                put_resp = requests.put(upload_location, headers=chunk_headers, data=chunk, timeout=90)
                pct = (byte_end + 1) / file_size * 100
                print(f"       [{filename}] Progress: {pct:.1f}%", flush=True)
                byte_start = byte_end + 1

        data = put_resp.json()
        if not data.get("webViewLink"):
            data["webViewLink"] = f"https://drive.google.com/file/d/{data['id']}/view?usp=drivesdk"
        set_shareable_permission(data["id"], access_token)
        return data

# ----------------------------------------------------------------------
# Google Sheets API Helpers
# ----------------------------------------------------------------------

def ensure_sheet_columns(sheet_id: str, access_token: str, min_columns: int = 16):
    """Ensures all sheets in the spreadsheet have at least min_columns."""
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
    if resp.status_code != 200:
        return
    data = resp.json()
    reqs = []
    for sh in data.get("sheets", []):
        p = sh["properties"]
        cols = p.get("gridProperties", {}).get("columnCount", 0)
        if cols < min_columns:
            reqs.append({
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": p["sheetId"],
                        "gridProperties": {"columnCount": min_columns}
                    },
                    "fields": "gridProperties.columnCount"
                }
            })
    if reqs:
        batch_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate"
        requests.post(batch_url, headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}, json={"requests": reqs}, timeout=30)

def update_sheet_range(sheet_id: str, range_a1: str, values: list, access_token: str):
    import urllib.parse
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{urllib.parse.quote(range_a1)}?valueInputOption=USER_ENTERED"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {"range": range_a1, "values": values}
    resp = requests.put(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()

# ----------------------------------------------------------------------
# Main Execution Pipeline
# ----------------------------------------------------------------------

def sync_all():
    env = load_env()
    client_id = env["GOOGLE_CLIENT_ID"]
    client_secret = env["GOOGLE_CLIENT_SECRET"]
    refresh_token = env["GOOGLE_REFRESH_TOKEN"]
    sheet_id = env.get("GOOGLE_SHEET_ID")

    print("==================================================================", flush=True)
    print("AI BUSINESS AUDITOR — CLOUD ASSET & SPREADSHEET SYNC ENGINE", flush=True)
    print("==================================================================", flush=True)

    print("\n[1/6] Authenticating with Google APIs...", flush=True)
    token = get_access_token(client_id, client_secret, refresh_token)
    print("Access token successfully generated.", flush=True)

    # 1. Master Root Folder in Drive
    root_folder_name = "AI Business Auditor - Social Content / Joel Adawah Sani"
    print(f"\n[2/6] Verifying Master Google Drive Folder: '{root_folder_name}'...", flush=True)
    root_id, root_link = find_or_create_folder(root_folder_name, None, token)
    set_shareable_permission(root_id, token)
    print(f"Master Folder Link: {root_link}", flush=True)

    # Subfolders
    lead_magnets_folder_id, lm_link = find_or_create_folder("Lead Magnets", root_id, token)
    set_shareable_permission(lead_magnets_folder_id, token)

    showcase_folder_id, sc_link = find_or_create_folder("Featured Section Showcase Audits", root_id, token)
    set_shareable_permission(showcase_folder_id, token)

    tiktok_master_folder_id, tt_link = find_or_create_folder("TikTok Content", root_id, token)
    set_shareable_permission(tiktok_master_folder_id, token)

    linkedin_master_folder_id, li_link = find_or_create_folder("LinkedIn Content", root_id, token)
    set_shareable_permission(linkedin_master_folder_id, token)

    # 2. Upload Flagship Lead Magnets
    print("\n[3/6] Syncing Flagship Lead Magnets...", flush=True)
    lead_magnet_links = {}
    for pdf_file in LEAD_MAGNETS_DIR.glob("*.pdf"):
        up = upload_file_smart(pdf_file, lead_magnets_folder_id, token)
        lead_magnet_links[pdf_file.name] = up["webViewLink"]
        print(f"  ✓ {pdf_file.name} -> {up['webViewLink']}", flush=True)

    # 3. Upload Featured Section Sample Audits (Apex & Summit)
    print("\n[4/6] Syncing Featured Section Showcase Sample Audits...", flush=True)
    featured_links = {}
    apex_pdf = CLIENTS_DIR / "apex-home-services" / "audit_sample.pdf"
    if apex_pdf.exists():
        up = upload_file_smart(apex_pdf, showcase_folder_id, token)
        featured_links["apex"] = up["webViewLink"]
        print(f"  ✓ Apex Home Services Sample Audit PDF -> {up['webViewLink']}", flush=True)

    summit_pdf = CLIENTS_DIR / "summit-mechanical-services" / "audit_sample.pdf"
    if summit_pdf.exists():
        up = upload_file_smart(summit_pdf, showcase_folder_id, token)
        featured_links["summit"] = up["webViewLink"]
        print(f"  ✓ Summit Mechanical Services Sample Audit PDF -> {up['webViewLink']}", flush=True)

    # 4. Upload TikTok Posts
    print("\n[5/6] Syncing 25 TikTok Post Folders & Rendered Videos...", flush=True)
    tiktok_links = {} # post_num -> {"folder_link", "video_link", "script_link"}
    post_folders = sorted([p for p in TIKTOK_DIR.iterdir() if p.is_dir() and p.name.startswith("post_")])
    for pf in post_folders:
        post_num = int(pf.name.split("_")[1])
        folder_id, folder_link = find_or_create_folder(pf.name, tiktok_master_folder_id, token)
        set_shareable_permission(folder_id, token)

        main_video_link = None
        script_link = None

        for file_path in sorted(pf.iterdir()):
            if file_path.is_file():
                up = upload_file_smart(file_path, folder_id, token)
                if file_path.name == "video.mp4":
                    main_video_link = up.get("webViewLink")
                elif file_path.name == "script.md":
                    script_link = up.get("webViewLink")

        tiktok_links[post_num] = {
            "folder_link": folder_link,
            "video_link": main_video_link,
            "script_link": script_link
        }
        tag = f"MP4 Ready: {main_video_link}" if main_video_link else f"Folder: {folder_link}"
        print(f"  ✓ TikTok #{post_num:02d} Synced -> {tag}", flush=True)

    # 5. Upload LinkedIn Posts
    print("\n[6/6] Syncing 25 LinkedIn Post Folders & Document Carousels...", flush=True)
    linkedin_links = {} # post_num -> {"folder_link", "asset_link", "post_copy_link"}
    li_folders = sorted([p for p in LINKEDIN_DIR.iterdir() if p.is_dir() and p.name.startswith("post_")])
    for pf in li_folders:
        post_num = int(pf.name.split("_")[1])
        folder_id, folder_link = find_or_create_folder(pf.name, linkedin_master_folder_id, token)
        set_shareable_permission(folder_id, token)

        main_asset_link = None
        post_copy_link = None

        for file_path in sorted(pf.iterdir()):
            if file_path.is_file():
                up = upload_file_smart(file_path, folder_id, token)
                if file_path.name.endswith(".pdf"):
                    # Carousel takes priority, then blueprint/checklist
                    if "carousel" in file_path.name:
                        main_asset_link = up.get("webViewLink")
                    elif not main_asset_link:
                        main_asset_link = up.get("webViewLink")
                elif file_path.name == "post_copy.md":
                    post_copy_link = up.get("webViewLink")

        linkedin_links[post_num] = {
            "folder_link": folder_link,
            "asset_link": main_asset_link,
            "copy_link": post_copy_link
        }
        tag = f"Asset: {main_asset_link}" if main_asset_link else f"Folder: {folder_link}"
        print(f"  ✓ LinkedIn #{post_num:02d} Synced -> {tag}", flush=True)

    # 6. Update Google Sheet
    if sheet_id:
        print("\n==================================================================", flush=True)
        print("UPDATING GOOGLE SPREADSHEET TABS WITH DIRECT GOOGLE DRIVE LINKS", flush=True)
        print("==================================================================", flush=True)

        ensure_sheet_columns(sheet_id, token, 16)

        # A. TikTok Content Calendar: Columns M (Asset/Video Link) & N (Folder Link)
        tt_m_vals = [["Google Drive Video / Asset Link"]]
        tt_n_vals = [["Google Drive Post Folder Link"]]
        for i in range(1, 26):
            info = tiktok_links.get(i, {})
            v_link = info.get("video_link")
            s_link = info.get("script_link")
            f_link = info.get("folder_link", "")

            if v_link:
                m_cell = f'=HYPERLINK("{v_link}", "▶ View / Download MP4 Video")'
            elif s_link:
                m_cell = f'=HYPERLINK("{s_link}", "📄 View Script & Directions")'
            else:
                m_cell = f'=HYPERLINK("{f_link}", "📁 Open Post Folder")' if f_link else ""

            n_cell = f'=HYPERLINK("{f_link}", "📁 Open Post Folder (Drive)")' if f_link else ""

            tt_m_vals.append([m_cell])
            tt_n_vals.append([n_cell])

        update_sheet_range(sheet_id, "TikTok Content Calendar!M1:M26", tt_m_vals, token)
        update_sheet_range(sheet_id, "TikTok Content Calendar!N1:N26", tt_n_vals, token)
        print("✓ Updated TikTok Content Calendar (Columns M & N: Direct MP4 Videos & Post Folders)!", flush=True)

        try:
            from tools.add_tiktok_ready_to_paste_column import build_ready_to_paste_caption
            from generate_tiktok_engine import VIDEOS
            col_o_vals = [["Ready-to-Paste TikTok Post Caption (Copy & Paste with PDF Link)"]]
            for v in VIDEOS:
                col_o_vals.append([build_ready_to_paste_caption(v)])
            update_sheet_range(sheet_id, "TikTok Content Calendar!O1:O26", col_o_vals, token)
            print("✓ Updated TikTok Content Calendar (Column O: Ready-to-Paste Captions with PDF Links)!", flush=True)
        except Exception as e:
            print(f"Note: Column O sync skipped: {e}", flush=True)

        # B. LinkedIn Content Calendar: Columns K (Asset Link) & L (Folder Link)
        # Headers at row 1
        update_sheet_range(sheet_id, "LinkedIn Content Calendar!K1:L1", [["Google Drive Asset Link", "Google Drive Post Folder Link"]], token)

        # Featured Section Rows (Row 3 = Apex, Row 4 = Summit)
        sc_link_val = sc_link or root_link
        if featured_links.get("apex"):
            update_sheet_range(sheet_id, "LinkedIn Content Calendar!K3:L3", [[f'=HYPERLINK("{featured_links["apex"]}", "📄 Download Apex Audit Sample PDF")', f'=HYPERLINK("{sc_link_val}", "📁 Open Featured Showcase Folder")']], token)
        if featured_links.get("summit"):
            update_sheet_range(sheet_id, "LinkedIn Content Calendar!K4:L4", [[f'=HYPERLINK("{featured_links["summit"]}", "📄 Download Summit Audit Sample PDF")', f'=HYPERLINK("{sc_link_val}", "📁 Open Featured Showcase Folder")']], token)

        # Posts 1 to 25 at Rows 8 to 32
        li_k_vals = []
        li_l_vals = []
        for i in range(1, 26):
            info = linkedin_links.get(i, {})
            a_link = info.get("asset_link")
            f_link = info.get("folder_link", "")

            if a_link:
                k_cell = f'=HYPERLINK("{a_link}", "📄 Download Attached Asset (Drive)")'
            elif f_link:
                k_cell = f'=HYPERLINK("{f_link}", "📁 Open Post Folder (Drive)")'
            else:
                k_cell = ""

            l_cell = f'=HYPERLINK("{f_link}", "📁 Open Post Folder (Drive)")' if f_link else ""

            li_k_vals.append([k_cell])
            li_l_vals.append([l_cell])

        update_sheet_range(sheet_id, "LinkedIn Content Calendar!K8:K32", li_k_vals, token)
        update_sheet_range(sheet_id, "LinkedIn Content Calendar!L8:L32", li_l_vals, token)
        print("✓ Updated LinkedIn Content Calendar (Columns K & L: Direct Carousels, PDFs & Post Folders)!", flush=True)

        # C. Outreach Pipeline Tab: Direct Clickable Drive Links & Ready-to-Send Copy
        try:
            from tools.sync_outreach_pipeline_assets import sync_outreach_pipeline
            sync_outreach_pipeline()
        except Exception as e:
            print(f"Note: Outreach Pipeline sync skipped: {e}", flush=True)

    print("\n==================================================================", flush=True)
    print("SUCCESS: ALL 50 SOCIAL POSTS, CAROUSELS, VIDEOS, AND ASSETS SYNCED TO DRIVE & SPREADSHEET!", flush=True)
    print(f"Master Google Drive Folder: {root_link}", flush=True)
    print("==================================================================", flush=True)

if __name__ == "__main__":
    sync_all()
