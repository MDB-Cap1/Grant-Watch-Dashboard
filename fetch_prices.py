import yfinance as yf
import json
from datetime import datetime

TICKERS = {
    "INTC": {"company": "Intel Corporation", "sector": "chips"},
    "MU":   {"company": "Micron Technology", "sector": "chips"},
    "GFS":  {"company": "GlobalFoundries", "sector": "chips"},
    "LNTH": {"company": "Lantheus Holdings", "sector": "biotech"},
    "BMY":  {"company": "Bristol Myers Squibb", "sector": "biotech"},
    "RCKT": {"company": "Rocket Pharmaceuticals", "sector": "biotech"},
    "LLY":  {"company": "Eli Lilly & Co.", "sector": "biotech"},
    "REGN": {"company": "Regeneron Pharmaceuticals", "sector": "biotech"},
    "ALB":  {"company": "Albemarle Corporation", "sector": "minerals"},
    "PLTR": {"company": "Palantir Technologies", "sector": "defense"},
}

prices = {}
for ticker, meta in TICKERS.items():
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="2d")
        info = t.fast_info

        current = round(float(info.last_price), 2)
        prev    = round(float(hist["Close"].iloc[-2]), 2) if len(hist) >= 2 else current
        change  = round(current - prev, 2)
        change_pct = round((change / prev) * 100, 2) if prev else 0
        week52_low  = round(float(info.fifty_two_week_low), 2)
        week52_high = round(float(info.fifty_two_week_high), 2)

        prices[ticker] = {
            "price": current,
            "change": change,
            "change_pct": change_pct,
            "week52_low": week52_low,
            "week52_high": week52_high,
            "company": meta["company"],
            "sector": meta["sector"],
        }
        print(f"  ✅ {ticker}: ${current} ({change_pct:+.2f}%)")
    except Exception as e:
        print(f"  ❌ {ticker} failed: {e}")

output = {
    "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    "prices": prices
}

with open("prices.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n✔ prices.json updated at {output['updated']}")
