"""RM Workspace — configuration loaded from .env (stdlib only, no python-dotenv needed)."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def _load_env():
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

_load_env()

def get(key, default=""):
    return os.environ.get(key, default)

def get_bool(key, default=False):
    return os.environ.get(key, str(default)).lower() in ("1", "true", "yes", "on")

def get_int(key, default=0):
    try: return int(os.environ.get(key, default))
    except ValueError: return default

# --- Safety / rights (read SETUP.md) ---
I_HAVE_RIGHTS_TO_CLIP = get_bool("I_HAVE_RIGHTS_TO_CLIP", False)  # permission / licence / CC / own content
AUTO_POST = get_bool("AUTO_POST", False)          # upload automatically when true
DRY_RUN = get_bool("DRY_RUN", True)               # True = plan everything, render/upload nothing real

# --- Clipper ---
MRBEAST_CHANNEL_ID = get("MRBEAST_CHANNEL_ID", "UCX6OQ3DkcsbYNE6H8uQQuVA")  # MrBeast official
YOUTUBE_API_KEY = get("YOUTUBE_API_KEY")
CLIP_LENGTH_SECONDS = get_int("CLIP_LENGTH_SECONDS", 45)
CHECK_EVERY_MINUTES = get_int("CHECK_EVERY_MINUTES", 60)

# --- AI (optional — heuristics work without any key) ---
OPENAI_API_KEY = get("OPENAI_API_KEY")

# --- Dropshipping ---
USD_TO_CZK = float(get("USD_TO_CZK", "23.0"))
PRICE_MULTIPLIER = float(get("PRICE_MULTIPLIER", "2.5"))   # supplier cost x this = selling price
SHOPIFY_STORE = get("SHOPIFY_STORE")                       # e.g. my-store.myshopify.com
SHOPIFY_ACCESS_TOKEN = get("SHOPIFY_ACCESS_TOKEN")

DATA_DIR = ROOT / "data"; DATA_DIR.mkdir(exist_ok=True)
CLIPS_DIR = ROOT / "outputs" / "clips"; CLIPS_DIR.mkdir(parents=True, exist_ok=True)
SHOPIFY_DIR = ROOT / "outputs" / "shopify"; SHOPIFY_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "state.db"
