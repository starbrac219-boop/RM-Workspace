"""Build a store for you: (1) Shopify-import CSV you upload in 2 minutes, or
(2) create DRAFT products directly via Shopify Admin API when token is set.
Supplier fulfilment/ordering stays yours (AliExpress/CJ/agent) as you said."""
import csv, json, urllib.request
from .. import config
from .research import research

def copy_for(p):
    return (f"{p['product']} — řeší problém rychle a jednoduše. "
            f"✅ Ověřená kvalita ✅ Rychlé odeslání ✅ Vrácení do 30 dnů. "
            f"Objednej dnes za {p['price_czk']} Kč!")

def export_csv(products=None, path=None):
    products = products or research()
    path = path or (config.SHOPIFY_DIR / "products_import.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published",
                    "Option1 Name", "Variant Price", "Variant Compare At Price", "Variant Requires Shipping", "Status"])
        for p in products:
            handle = p["product"].lower().replace(" ", "-")
            w.writerow([handle, p["product"], f"<p>{copy_for(p)}</p>", "RM Workspace", "Dropshipping",
                        "viral,2026,tiktok", "FALSE", "Title", p["price_czk"], int(p["price_czk"] * 1.6), "TRUE", "draft"])
    return path

def push_to_shopify(products=None):
    """Creates DRAFT products (never auto-publishes). Returns per-product result."""
    if not (config.SHOPIFY_STORE and config.SHOPIFY_ACCESS_TOKEN):
        return {"status": "blocked", "reason": "Set SHOPIFY_STORE + SHOPIFY_ACCESS_TOKEN in .env (SETUP.md step 5), or use the CSV export."}
    out = []
    for p in (products or research()):
        body = json.dumps({"product": {"title": p["product"], "body_html": copy_for(p), "status": "draft",
                                       "variants": [{"price": f"{p['price_czk']}.00"}]}}).encode()
        req = urllib.request.Request(f"https://{config.SHOPIFY_STORE}/admin/api/2024-10/products.json",
                                     data=body, method="POST",
                                     headers={"X-Shopify-Access-Token": config.SHOPIFY_ACCESS_TOKEN, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            out.append({"product": p["product"], "shopify_id": json.load(r)["product"]["id"], "status": "draft created"})
    return out
