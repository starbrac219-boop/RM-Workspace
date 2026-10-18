# RM Workspace — AI Clipper + AI Dropshipping

A local service that runs **only while your PC is on**. No server, no hosting fees.

## 🎬 AI Clipper (MrBeast only)
Checks MrBeast's channel (`UCX6OQ3DkcsbYNE6H8uQQuVA`, changeable in `.env`) for new videos →
picks the strongest hook moment → makes a **9:16 (1080×1920)** clip with blurred background →
burns in **pro word-highlight captions** → uploads as a Short to **your** channel.
Ships in safe `DRY_RUN` mode: it only *plans* clips until you finish **SETUP.md**.

## 🛒 AI Dropshipping
Scores candidate products (trend / margin / competition / shipping) → prices them in **CZK**
(…9 endings, ~60% margin) → generates product copy → exports a **Shopify import CSV**
or creates draft products via the Shopify Admin API. Supplier ordering stays yours.

## Quick start
```bash
python run.py dashboard   # http://localhost:8000
python run.py scan        # demo clip plan (offline)
python run.py research    # TOP products in CZK
python run.py export      # outputs/shopify/products_import.csv
python run.py schedule    # run forever while PC is on
```
👉 **Read [SETUP.md](SETUP.md) — it lists exactly what you must do (rights, ffmpeg,
YouTube login, Shopify) before anything posts automatically.**

## Layout
- `rm_service/clipper/` discover → moments → subtitles → render (ffmpeg) → upload (YouTube API)
- `rm_service/dropship/` research (CZK pricing) → shopify_export (CSV / Admin API)
- `rm_service/app.py` local dashboard · `run.py` CLI · `tests/` unit tests
