"""
Google Drive & Sheets OAuth Setup Helper
Starts a temporary local server, opens browser for Google authentication with Drive + Sheets + GSC scopes,
captures authorization code, exchanges for permanent refresh token, and updates .env.
"""
import os
import sys
import json
import webbrowser
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PORT = 8080
REDIRECT_URI = f"http://localhost:{PORT}"

auth_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <html>
            <head><title>Authorization Successful</title></head>
            <body style="font-family: sans-serif; text-align: center; padding: 50px;">
              <h1 style="color: #0284c7;">Authentication Successful!</h1>
              <p>Google Drive & Google Sheets access granted. You may now close this tab and return to Antigravity.</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Error: Missing code parameter.")

    def log_message(self, format, *args):
        pass

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

def save_refresh_token(refresh_token):
    p = Path(".env")
    lines = []
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            lines = f.readlines()
    
    updated = False
    new_lines = []
    for line in lines:
        if line.startswith("GOOGLE_REFRESH_TOKEN="):
            new_lines.append(f"GOOGLE_REFRESH_TOKEN={refresh_token}\n")
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        new_lines.append(f"GOOGLE_REFRESH_TOKEN={refresh_token}\n")

    with open(p, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    mirror = Path("ai-business-auditor/.env")
    if mirror.parent.exists():
        with open(mirror, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

def main():
    env = load_env()
    client_id = env.get("GOOGLE_CLIENT_ID")
    client_secret = env.get("GOOGLE_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Error: GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET is missing in .env")
        sys.exit(1)

    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/webmasters.readonly"
    ]

    auth_params = {
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(auth_params)}"

    print("=" * 60)
    print("Google Drive & Sheets OAuth Setup Helper")
    print("=" * 60)
    print("Opening browser for authentication...")
    print(f"If browser does not open automatically, visit:\n{auth_url}\n")

    webbrowser.open(auth_url)

    server = HTTPServer(("localhost", PORT), OAuthHandler)
    print(f"Waiting for authorization callback on port {PORT}...")
    while auth_code is None:
        server.handle_request()

    print("\nAuthorization code received! Exchanging for refresh token...")

    token_url = "https://oauth2.googleapis.com/token"
    data = urllib.parse.urlencode({
        "code": auth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }).encode("utf-8")

    req = urllib.request.Request(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            refresh_token = resp_data.get("refresh_token")
            if refresh_token:
                print("\nSUCCESS! Refresh token obtained with Google Drive + Sheets permissions!")
                save_refresh_token(refresh_token)
                print("Saved GOOGLE_REFRESH_TOKEN to .env!")
            else:
                print("\nWarning: No refresh_token returned in response:")
                print(json.dumps(resp_data, indent=2))
    except Exception as e:
        print(f"\nToken exchange failed: {e}")

if __name__ == "__main__":
    main()
