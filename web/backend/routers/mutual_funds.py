"""Mutual Funds router — live AMFI NAV + mfapi.in returns."""
from fastapi import APIRouter, Query
import requests
import numpy as np
from datetime import datetime

router = APIRouter()

CATEGORY_KEYWORDS = {
    "Large Cap":   ["large cap fund", "bluechip", "top 100"],
    "Mid Cap":     ["mid cap fund", "midcap fund"],
    "Small Cap":   ["small cap fund", "smallcap fund"],
    "Flexi Cap":   ["flexi cap fund", "flexicap fund", "multi cap fund"],
    "Index Funds": ["index fund", "nifty 50 index", "sensex index"],
    "ELSS":        ["elss", "tax saver fund", "tax saving fund"],
    "Debt":        ["gilt fund", "liquid fund", "overnight fund", "short term debt",
                    "money market fund", "ultra short", "low duration"],
    "Hybrid":      ["hybrid fund", "balanced advantage", "aggressive hybrid"],
    "Gold":        ["gold fund", "gold etf", "silver fund"],
}

def _fetch_amfi():
    r = requests.get("https://www.amfiindia.com/spages/NAVAll.txt", timeout=20)
    if r.status_code != 200:
        return []
    funds = []
    for line in r.text.strip().split("\n"):
        parts = line.strip().split(";")
        if len(parts) < 6:
            continue
        try:
            code = parts[0].strip()
            name = parts[3].strip()
            nav  = float(parts[4].strip())
            date = parts[5].strip()
            nl   = name.lower()
            if "direct" not in nl or "growth" not in nl or nav <= 0:
                continue
            cat = "Others"
            for c, kws in CATEGORY_KEYWORDS.items():
                if any(kw in nl for kw in kws):
                    cat = c
                    break
            if cat == "Others":
                continue
            funds.append({"scheme_code": code, "name": name,
                          "nav": nav, "nav_date": date, "category": cat})
        except Exception:
            continue
    return funds

def _cagr(code, years=3):
    try:
        r = requests.get(f"https://api.mfapi.in/mf/{code}", timeout=10)
        if r.status_code != 200:
            return None
        data = list(reversed(r.json().get("data", [])))
        if len(data) < years * 200:
            return None
        latest = float(data[-1]["nav"])
        old    = float(data[-(years * 365)]["nav"])
        if old <= 0:
            return None
        return round(((latest / old) ** (1.0 / years) - 1) * 100, 2)
    except Exception:
        return None

@router.get("/categories")
def get_categories():
    return list(CATEGORY_KEYWORDS.keys())

@router.get("/funds")
def get_funds(category: str = Query(...), limit: int = Query(20)):
    funds = _fetch_amfi()
    filtered = [f for f in funds if f["category"] == category]
    filtered = sorted(filtered, key=lambda x: x["nav"], reverse=True)[:limit]
    # Enrich top 10 with 1Y CAGR
    for f in filtered[:10]:
        f["return_1y"] = _cagr(f["scheme_code"], years=1)
        f["return_3y"] = _cagr(f["scheme_code"], years=3)
    return {"funds": filtered, "total": len(filtered),
            "timestamp": datetime.now().isoformat()}

@router.get("/nav_history")
def get_nav_history(scheme_code: str = Query(...), days: int = Query(365)):
    try:
        r = requests.get(f"https://api.mfapi.in/mf/{scheme_code}", timeout=12)
        if r.status_code != 200:
            return {"error": "mfapi unavailable"}
        data = list(reversed(r.json().get("data", [])))[-days:]
        return {
            "dates": [d["date"] for d in data],
            "navs":  [float(d["nav"]) for d in data],
        }
    except Exception as e:
        return {"error": str(e)}
