"""Upload a Short to YOUR channel via YouTube Data API v3 (OAuth — your own login).
Needs client_secret.json from Google Cloud (SETUP.md step 3). Never uploads without
AUTO_POST=true + I_HAVE_RIGHTS_TO_CLIP=true."""
from pathlib import Path
from .. import config

def upload_short(file_path, title, description=""):
    if not config.I_HAVE_RIGHTS_TO_CLIP:
        return {"status": "blocked", "reason": "Set I_HAVE_RIGHTS_TO_CLIP=true in .env only if you have permission/licence to clip this content."}
    if not config.AUTO_POST:
        return {"status": "skipped", "reason": "AUTO_POST=false — file is ready in outputs/clips for manual review/upload."}
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        return {"status": "blocked", "reason": "pip install -r requirements.txt (google API client missing)"}
    secret = Path(__file__).resolve().parents[2] / "client_secret.json"
    if not secret.exists():
        return {"status": "blocked", "reason": "client_secret.json missing — SETUP.md step 3"}
    flow = InstalledAppFlow.from_client_secrets_file(str(secret), ["https://www.googleapis.com/auth/youtube.upload"])
    creds = flow.run_local_server(port=0)
    yt = build("youtube", "v3", credentials=creds)
    body = {"snippet": {"title": title[:100], "description": description, "categoryId": "24"},
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}
    resp = yt.videos().insert(part="snippet,status", body=body,
                              media_body=MediaFileUpload(str(file_path), resumable=True)).execute()
    return {"status": "uploaded", "youtube_id": resp["id"], "url": f"https://youtube.com/shorts/{resp['id']}"}
