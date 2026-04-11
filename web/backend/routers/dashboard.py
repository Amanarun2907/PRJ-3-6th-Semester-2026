"""Dashboard router — live NIFTY, SENSEX, gainers, losers, market breadth."""
from fastapi import APIRouter
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

router = APIRouter()

INDIAN_STOCKS = {
    "HDFCBANK.NS":"HDFC Bank","ICICIBANK.NS":"ICICI Bank","KOTAKBANK.NS":"Kotak Bank",
    "SBIN.NS":"State Bank","AXISBANK.NS":"Axis Bank","TCS.NS":"TCS",
    "INFY.NS":"Infosys","WIPRO.NS":"Wipro","HCLTECH.NS":"HCL Tech",
    "RELIANCE.NS":"Reliance","HINDUNILVR.NS":"HUL","ITC.NS":"ITC",
    "MARUTI.NS":"Maruti","TATAMOTORS.NS":"Tata Motors","SUNPHARMA.NS":"Sun Pharma",
    "DRREDDY.NS":"Dr Reddy","BAJFINANCE.NS":"Bajaj Finance","LT.NS":"L&T",
    "BHARTIARTL.NS":"Airtel","TITAN.NS":"Titan",
}

def _pct(hist):
    if hist.empty or len(hist) < 2:
        return 0.0
    return float(((hist["Close"].iloc[-1] - hist["Close"].iloc[-2]) / hist["Close"].iloc[-2]) * 100)

def _index(symbol):
    try:
        hist = yf.Ticker(symbol).history(period="2d")
        if hist.empty or len(hist) < 2:
            return None
        return {
            "value": round(float(hist["Close"].iloc[-1]), 2),
            "change_pct": round(_pct(hist), 2),
            "change_pts": round(float(hist["Close"].iloc[-1] - hist["Close"].iloc[-2]), 2),
        }
    except Exception:
        return None

@router.get("/indices")
def get_indices():
    nifty  = _index("^NSEI")
    sensex = _index("^BSESN")
    return {
        "nifty":  nifty  or {"value": 0, "change_pct": 0, "change_pts": 0},
        "sensex": sensex or {"value": 0, "change_pct": 0, "change_pts": 0},
        "timestamp": datetime.now().isoformat(),
    }

@router.get("/movers")
def get_movers():
    gainers, losers = [], []
    for sym, name in INDIAN_STOCKS.items():
        try:
            hist = yf.Ticker(sym).history(period="2d")
            if hist.empty or len(hist) < 2:
                continue
            chg = _pct(hist)
            price = round(float(hist["Close"].iloc[-1]), 2)
            item = {"symbol": sym.replace(".NS",""), "name": name,
                    "price": price, "change_pct": round(chg, 2)}
            if chg > 0:
                gainers.append(item)
            else:
                losers.append(item)
        except Exception:
            continue
    gainers = sorted(gainers, key=lambda x: x["change_pct"], reverse=True)[:5]
    losers  = sorted(losers,  key=lambda x: x["change_pct"])[:5]
    return {"gainers": gainers, "losers": losers, "timestamp": datetime.now().isoformat()}

@router.get("/breadth")
def get_breadth():
    advancing = declining = unchanged = 0
    for sym in INDIAN_STOCKS:
        try:
            hist = yf.Ticker(sym).history(period="2d")
            if hist.empty or len(hist) < 2:
                continue
            chg = _pct(hist)
            if chg > 0.05:   advancing += 1
            elif chg < -0.05: declining += 1
            else:             unchanged += 1
        except Exception:
            continue
    total = advancing + declining + unchanged or 1
    return {
        "advancing": advancing, "declining": declining, "unchanged": unchanged,
        "total": total,
        "ad_ratio": round(advancing / max(declining, 1), 2),
        "strength": round(advancing / total * 100, 1),
    }
