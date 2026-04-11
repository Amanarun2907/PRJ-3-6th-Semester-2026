"""Advanced Analytics router — sector heatmap, correlation, breadth, volume."""
from fastapi import APIRouter
import yfinance as yf, numpy as np, pandas as pd
from datetime import datetime

router = APIRouter()

SECTOR_STOCKS = {
    "Banking":  ["HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","KOTAKBANK.NS","AXISBANK.NS"],
    "IT":       ["TCS.NS","INFY.NS","WIPRO.NS","HCLTECH.NS","TECHM.NS"],
    "Auto":     ["MARUTI.NS","TATAMOTORS.NS","M&M.NS","BAJAJ-AUTO.NS"],
    "Pharma":   ["SUNPHARMA.NS","DRREDDY.NS","CIPLA.NS","DIVISLAB.NS"],
    "FMCG":     ["HINDUNILVR.NS","ITC.NS","NESTLEIND.NS","BRITANNIA.NS"],
    "Energy":   ["RELIANCE.NS","ONGC.NS","BPCL.NS","IOC.NS"],
    "Telecom":  ["BHARTIARTL.NS"],
    "Metals":   ["TATASTEEL.NS","HINDALCO.NS","JSWSTEEL.NS"],
}

CORR_STOCKS = {
    "RELIANCE":"RELIANCE.NS","TCS":"TCS.NS","HDFCBANK":"HDFCBANK.NS",
    "INFY":"INFY.NS","ICICIBANK":"ICICIBANK.NS","HINDUNILVR":"HINDUNILVR.NS",
    "ITC":"ITC.NS","SBIN":"SBIN.NS",
}

@router.get("/sector_heatmap")
def sector_heatmap():
    result = {}
    for sector, tickers in SECTOR_STOCKS.items():
        changes = []
        for t in tickers:
            try:
                hist = yf.Ticker(t).history(period="2d")
                if len(hist) >= 2:
                    changes.append(float((hist["Close"].iloc[-1]-hist["Close"].iloc[-2])/hist["Close"].iloc[-2]*100))
            except Exception: pass
        if changes: result[sector] = round(float(np.mean(changes)),2)
    return {"sectors": result, "timestamp": datetime.now().isoformat()}

@router.get("/correlation")
def correlation(period: str = "3mo"):
    data = {}
    for name, sym in CORR_STOCKS.items():
        try:
            hist = yf.Ticker(sym).history(period=period)
            if not hist.empty and len(hist) > 20:
                data[name] = hist["Close"].pct_change().dropna()
        except Exception: pass
    if len(data) < 2: return {"error": "Insufficient data"}
    df   = pd.DataFrame(data).dropna()
    corr = df.corr().round(3)
    return {"stocks": corr.columns.tolist(),
            "matrix": corr.values.tolist(),
            "timestamp": datetime.now().isoformat()}

@router.get("/volume_analysis")
def volume_analysis():
    stocks = list(CORR_STOCKS.values())
    result = []
    for sym in stocks:
        try:
            hist = yf.Ticker(sym).history(period="5d")
            if len(hist) >= 2:
                cv = float(hist["Volume"].iloc[-1])
                av = float(hist["Volume"].mean())
                cp = float(hist["Close"].iloc[-1])
                pp = float(hist["Close"].iloc[-2])
                result.append({
                    "symbol":       sym.replace(".NS",""),
                    "current_vol":  int(cv),
                    "avg_vol":      int(av),
                    "vol_ratio":    round(cv/av,2) if av else 1,
                    "price_change": round((cp-pp)/pp*100,2),
                    "alert":        "High" if cv/av > 1.5 else "Normal",
                })
        except Exception: pass
    return sorted(result, key=lambda x: x["vol_ratio"], reverse=True)

@router.get("/market_breadth")
def market_breadth():
    all_stocks = [s for tickers in SECTOR_STOCKS.values() for s in tickers]
    adv = dec = unch = 0
    for sym in all_stocks:
        try:
            hist = yf.Ticker(sym).history(period="2d")
            if len(hist) >= 2:
                chg = float((hist["Close"].iloc[-1]-hist["Close"].iloc[-2])/hist["Close"].iloc[-2]*100)
                if chg > 0.05: adv += 1
                elif chg < -0.05: dec += 1
                else: unch += 1
        except Exception: pass
    total = adv+dec+unch or 1
    return {"advancing":adv,"declining":dec,"unchanged":unch,"total":total,
            "ad_ratio":round(adv/max(dec,1),2),
            "strength":round(adv/total*100,1),
            "sentiment":"Bullish" if adv/total>0.6 else "Bearish" if adv/total<0.4 else "Neutral"}
