#!/usr/bin/env python3
"""RM Workspace — AI Clipper (MrBeast only) + AI Dropshipping (CZK / Shopify)

  python run.py dashboard     # web dashboard on http://localhost:8000
  python run.py scan          # check for a new MrBeast video (demo mode = offline sample)
  python run.py scan --live   # real RSS check (needs internet)
  python run.py research      # TOP dropshipping products + CZK prices
  python run.py export        # Shopify import CSV -> outputs/shopify/products_import.csv
  python run.py schedule      # run forever while PC is on (checks every CHECK_EVERY_MINUTES)
"""
import json, sys, time
sys.path.insert(0, ".")
from rm_service import config
from rm_service.clipper.pipeline import run_once
from rm_service.dropship.research import research
from rm_service.dropship.shopify_export import export_csv, push_to_shopify

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dashboard"
    if cmd == "dashboard":
        from rm_service.app import serve; serve()
    elif cmd == "scan":
        print(json.dumps(run_once(use_demo="--live" not in sys.argv), ensure_ascii=False, indent=2))
    elif cmd == "research":
        for p in research(10): print(f"{p['score']:>5} | {p['product']:<42} | {p['price_czk']:>5} Kč | marže {p['margin_pct']}% | {p['verdict']}")
    elif cmd == "export":
        print("Shopify CSV:", export_csv(research(10)))
    elif cmd == "push-shopify":
        print(json.dumps(push_to_shopify(), ensure_ascii=False, indent=2))
    elif cmd == "schedule":
        print(f"Scheduler běží — kontrola každých {config.CHECK_EVERY_MINUTES} min. Ctrl+C = stop.")
        while True:
            try: print(run_once()); print(export_csv())
            except Exception as e: print("Chyba (běžím dál):", e)
            time.sleep(config.CHECK_EVERY_MINUTES * 60)
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
