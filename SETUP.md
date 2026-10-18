# SETUP — what YOU must do so it works (10–20 min, one time)

The service is built and runs in **safe DRY_RUN mode** out of the box: it plans clips and
researches products, but renders/uploads **nothing** until you finish the steps below.

## ⚖️ Step 0 — Rights (important, read first)
Re-uploading clips of MrBeast videos to your own channel is **copyrighted content**.
YouTube can strike/terminate channels for it and Shorts made of reused content can be
rejected from monetisation ("reused content policy"). Only set
`I_HAVE_RIGHTS_TO_CLIP=true` if one of these is true: you have written permission/a
licence from MrBeast's team, the video is Creative Commons, or it's your own content
(change `MRBEAST_CHANNEL_ID` in `.env`). Safer long-term model used by big clippers:
get permission, add your own commentary/reaction so the clip is transformative, always
credit + link the original (the uploader does this automatically).

## 1) Install Python
Windows: python.org → Python 3.11+ → tick **"Add python.exe to PATH"**.

## 2) Install the heavy tools (one time, in this folder)
```
pip install -r requirements.txt
winget install Gyan.FFmpeg        (or download ffmpeg from ffmpeg.org and add to PATH)
```
Check: `ffmpeg -version` and `yt-dlp --version` both print something.

## 3) YouTube upload login (your channel)
1. console.cloud.google.com → create project → enable **YouTube Data API v3**.
2. Credentials → OAuth client ID (Desktop) → download → save as `client_secret.json` in this folder.
3. First real upload opens a browser — log in with **your** channel account and allow it.

## 4) Turn it on (.env)
Copy `.env.example` to `.env`, then when ready set:
```
DRY_RUN=false
AUTO_POST=true
I_HAVE_RIGHTS_TO_CLIP=true   ← only with permission (Step 0)
```

## 5) Shopify
1. Create store at shopify.com (trial is fine).
2. Easiest: `python run.py export` → Shopify admin → Products → Import → upload
   `outputs/shopify/products_import.csv` (products land as **drafts**, in CZK-ready prices).
3. Fully automatic (optional): Settings → Apps → Develop apps → Admin API token →
   put `SHOPIFY_STORE=...myshopify.com` + `SHOPIFY_ACCESS_TOKEN=...` in `.env` →
   `python run.py push-shopify` (still drafts only — you publish after checking supplier).
   Supplier ordering/fulfilment stays yours, as you wanted.

## 6) Run it while your PC is on
```
python run.py dashboard    # http://localhost:8000
python run.py schedule     # auto-checks for new videos + refreshes research
```
Auto-start with Windows: `Win+R` → `shell:startup` → create a shortcut to
`start_on_windows.bat` (included). PC off / asleep = service paused; it catches up on next start.

## What you do NOT need
No server, no hosting fees, no OpenAI key (built-in heuristics pick hooks & price products;
an `OPENAI_API_KEY` in `.env` is optional for smarter picks later).
