"""Product research: scores candidate products on trend, margin, competition, shipping.
Seed signals are refreshed/extendable — plug Google Trends / TikTok / Amazon data into `candidates()`.
CZK pricing: selling = supplier_cost_usd * USD_TO_CZK * PRICE_MULTIPLIER, rounded to x9 CZK (Czech price psychology)."""
from .. import config

def czk_price(cost_usd):
    raw = cost_usd * config.USD_TO_CZK * config.PRICE_MULTIPLIER
    return int(raw // 10 * 10 + 9)  # ...9 ending, e.g. 499 CZK

# name, supplier cost USD, trend 0-100, competition 0-100 (lower=better), weight kg, solves_problem
CANDIDATES = [
    ("Mini projektor s WiFi 2026", 28.0, 88, 55, 0.9, True),
    ("Chytrý difuzér s aplikací", 9.5, 76, 48, 0.5, True),
    ("Levitující LED lampa", 18.0, 71, 40, 0.8, False),
    ("Silikonový odstraňovač vodního kamene", 3.2, 82, 62, 0.2, True),
    ("Přenosný mixér USB-C", 7.8, 68, 70, 0.4, True),
    ("LED pásek s pohybovým senzorem", 4.5, 79, 58, 0.3, True),
    ("Ergonomický polštář z paměťové pěny", 12.0, 74, 52, 1.1, True),
    ("Mini klimatizace do pokoje", 21.0, 85, 60, 1.6, True),
    ("Chytrý dávkovač krmiva s kamerou", 24.0, 81, 38, 1.2, True),
    ("Magnetický nabíjecí kabel 3v1", 2.8, 64, 78, 0.1, False),
]

def score(p):
    name, cost, trend, comp, weight, solves = p
    margin = (czk_price(cost) - cost * config.USD_TO_CZK) / czk_price(cost) * 100
    s = trend * 0.45 + (100 - comp) * 0.25 + min(margin, 80) * 0.2 + (10 if solves else 0) + (5 if weight < 0.5 else 0)
    return {"product": name, "supplier_cost_usd": cost, "price_czk": czk_price(cost),
            "margin_pct": round(margin), "trend": trend, "competition": comp,
            "score": round(s, 1), "verdict": "🔥 TEST IT" if s >= 70 else ("👀 watch" if s >= 55 else "❌ skip")}

def research(top=5):
    return sorted((score(p) for p in CANDIDATES), key=lambda x: -x["score"])[:top]
