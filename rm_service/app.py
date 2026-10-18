"""Local dashboard — stdlib only. Run: python run.py dashboard  ->  http://localhost:8000"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from . import config, store
from .clipper.pipeline import run_once
from .dropship.research import research
from .dropship.shopify_export import export_csv

PAGE = """<!doctype html><html lang="cs"><head><meta charset="utf-8"><title>RM Workspace</title>
<style>body{font-family:system-ui;background:#0f1115;color:#eee;margin:0;padding:24px}h1{color:#ffd60a}
.card{background:#1a1d24;border-radius:14px;padding:18px;margin:14px 0}button,a.btn{background:#ffd60a;color:#111;
border:0;padding:10px 16px;border-radius:9px;font-weight:700;text-decoration:none;cursor:pointer;margin-right:8px}
table{width:100%;border-collapse:collapse}td,th{padding:7px;border-bottom:1px solid #333;text-align:left}pre{white-space:pre-wrap;color:#9f9}</style></head>
<body><h1>💼 RM Workspace — AI Clipper + Dropshipping</h1>
<p>MrBeast-only clipper (9:16, pro captions) • Product research v CZK • Běží, jen když je PC zapnuté.</p>
<div class="card"><h2>🎬 Clipper</h2>
<a class="btn" href="/action/scan">▶ Zkontrolovat nové MrBeast video (demo)</a>
<a class="btn" href="/api/videos">Stav videí (JSON)</a><pre id="v"></pre></div>
<div class="card"><h2>🛒 Dropshipping — TOP produkty</h2>
<a class="btn" href="/action/research">▶ Nový research</a>
<a class="btn" href="/action/export">⬇ Vygenerovat Shopify CSV</a><pre id="p"></pre></div>
<div class="card"><h2>⚠️ Než zapneš auto-posting</h2><p id="s"></p></div>
<script>
fetch('/api/status').then(r=>r.json()).then(d=>document.getElementById('s').textContent=JSON.stringify(d,null,2));
fetch('/api/products').then(r=>r.json()).then(d=>document.getElementById('p').textContent=d.map(x=>x.score+' | '+x.product+' | '+x.price_czk+' Kč | marže '+x.margin_pct+'% | '+x.verdict).join('\\n'));
fetch('/api/videos').then(r=>r.json()).then(d=>document.getElementById('v').textContent=d.map(x=>x.status+' — '+x.title).join('\\n')||'(zatím nic — klikni na scan)');
</script></body></html>"""

def status():
    return {"dry_run": config.DRY_RUN, "auto_post": config.AUTO_POST,
            "i_have_rights_to_clip": config.I_HAVE_RIGHTS_TO_CLIP,
            "mrbeast_channel_id": config.MRBEAST_CHANNEL_ID,
            "check_every_minutes": config.CHECK_EVERY_MINUTES,
            "shopify_configured": bool(config.SHOPIFY_STORE and config.SHOPIFY_ACCESS_TOKEN),
            "next_step": "Dokud není v .env I_HAVE_RIGHTS_TO_CLIP=true + AUTO_POST=true, nic se samo nepostuje — vše se jen připraví ke kontrole."}

class H(BaseHTTPRequestHandler):
    def _send(self, body, ctype="application/json"):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(200); self.send_header("Content-Type", ctype); self.send_header("Content-Length", len(b)); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        routes = {"/": lambda: self._send(PAGE, "text/html; charset=utf-8"),
                  "/api/status": lambda: self._send(json.dumps(status(), ensure_ascii=False)),
                  "/api/products": lambda: self._send(json.dumps(research(), ensure_ascii=False)),
                  "/api/videos": lambda: self._send(json.dumps(store.all_videos(), ensure_ascii=False)),
                  "/action/scan": lambda: self._send(json.dumps(run_once(use_demo=True), ensure_ascii=False, indent=2)),
                  "/action/research": lambda: self._send(json.dumps(research(), ensure_ascii=False, indent=2)),
                  "/action/export": lambda: self._send(json.dumps({"csv": str(export_csv())}, ensure_ascii=False))}
        (routes.get(self.path) or (lambda: self._send('{"error":"not found"}')))()
    def log_message(self, *a): pass

def serve(port=8000):
    print(f"RM Workspace dashboard: http://localhost:{port}")
    HTTPServer(("0.0.0.0", port), H).serve_forever()
