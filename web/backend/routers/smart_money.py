"""Smart Money Tracker — live FII/DII from NSE API + bulk/block deals."""
from fastapi import APIRouter
import requests, re, yfinance as yf
import numpy as np
from datetime import datetime

router = APIRouter()

_HDR = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0",
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
}

SECTOR_STOCKS = {
    "Banking":  ["HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","KOTAKBANK.NS","AXISBANK.NS"],
    "IT":       ["TCS.NS","INFY.NS","WIPRO.NS","HCLTECH.NS"],
    "Pharma":   ["SUNPHARMA.NS","DRREDDY.NS","CIPLA.NS"],
    "Auto":     ["MARUTI.NS","TATAMOTORS.NS","BAJAJ-AUTO.NS"],
    "Energy":   ["RELIANCE.NS","ONGC.NS","NTPC.NS"],
    "FMCG":     ["HINDUNILVR.NS","ITC.NS","NESTLEIND.NS"],
    "Metals":   ["TATASTEEL.NS","HINDALCO.NS","JSWSTEEL.NS"],
}

def _n(v):
    try:
        v = str(v).replace(",","").replace("(","-").replace(")","").strip()
        m = re.findall(r"-?\d+\.?\d*", v)
        return float(m[0]) if m else 0.0
    except Exception: return 0.0

@router.get("/fii_dii")
def get_fii_dii():
    sess = requests.Session(); sess.headers.update(_HDR)
    try:
        r = sess.get("https://www.nseindia.com/api/fiidiiTradeReact", timeout=15)
        if r.status_code == 200:
            data = r.json()
            fii = next((x for x in data if "FII" in x.get("category","").upper()), None)
            dii = next((x for x in data if "DII" in x.get("category","").upper()), None)
            if fii or dii:
                fii_net = _n((fii or {}).get("netValue", 0))
                dii_net = _n((dii or {}).get("netValue", 0))
                return {
                    "fii_net":  fii_net,
                    "dii_net":  dii_net,
                    "fii_buy":  _n((fii or {}).get("buyValue", 0)),
                    "fii_sell": _n((fii or {}).get("sellValue", 0)),
                    "dii_buy":  _n((dii or {}).get("buyValue", 0)),
                    "dii_sell": _n((dii or {}).get("sellValue", 0)),
                    "date":     (fii or dii or {}).get("date", datetime.now().strftime("%d-%b-%Y")),
                    "source":   "NSE Live",
                    "signal":   "STRONG BUY" if fii_net>1000 and dii_net>1000
                                else "BUY" if fii_net>0 and dii_net>0
                                else "STRONG SELL" if fii_net<-1000 and dii_net<-1000
                                else "SELL" if fii_net<0 and dii_net<0 else "MIXED",
                }
    except Exception as e:
        print(f"NSE FII/DII error: {e}")
    return {"fii_net": None, "dii_net": None, "source": "Unavailable"}

@router.get("/bulk_deals")
def get_bulk_deals():
    sess = requests.Session(); sess.headers.update(_HDR)
    try:
        r = sess.get("https://www.nseindia.com/api/snapshot-capital-market-largedeal", timeout=15)
        if r.status_code == 200:
            deals = r.json().get("BULK_DEAL_DATA", [])
            return [{"symbol": d.get("symbol",""), "company": d.get("companyName",""),
                     "client": d.get("clientName",""), "type": d.get("dealType",""),
                     "qty": float(d.get("quantity",0) or 0),
                     "price": float(d.get("tradePrice",0) or 0),
                     "date": d.get("dealDate","")} for d in deals]
    except Exception as e:
        print(f"Bulk deals error: {e}")
    return []

@router.get("/block_deals")
def get_block_deals():
    sess = requests.Session(); sess.headers.update(_HDR)
    try:
        r = sess.get("https://www.nseindia.com/api/snapshot-capital-market-largedeal", timeout=15)
        if r.status_code == 200:
            deals = r.json().get("BLOCK_DEAL_DATA", [])
            return [{"symbol": d.get("symbol",""), "company": d.get("companyName",""),
                     "client": d.get("clientName",""),
                     "qty": float(d.get("quantity",0) or 0),
                     "price": float(d.get("tradePrice",0) or 0),
                     "date": d.get("dealDate","")} for d in deals]
    except Exception as e:
        print(f"Block deals error: {e}")
    return []

@router.get("/sector_flow")
def get_sector_flow():
    result = []
    for sector, tickers in SECTOR_STOCKS.items():
        changes, vols = [], []
        for t in tickers:
            try:
                ticker = yf.Ticker(t)
                price  = None
                prev   = None
                # Live price
                try:
                    p = ticker.fast_info.last_price
                    if p and not np.isnan(float(p)):
                        price = float(p)
                except Exception:
                    pass
                # Prev close
                try:
                    pc = ticker.fast_info.previous_close
                    if pc and not np.isnan(float(pc)):
                        prev = float(pc)
                except Exception:
                    pass
                # Fallback to daily history
                if price is None or prev is None:
                    hist   = ticker.history(period="5d")
                    closes = hist["Close"].dropna() if not hist.empty else None
                    if closes is not None and len(closes) >= 2:
                        price = float(closes.iloc[-1])
                        prev  = float(closes.iloc[-2])
                if price is None or prev is None or prev == 0:
                    continue
                chg = (price - prev) / prev * 100
                hist2 = ticker.history(period="5d")
                vol_ratio = 1.0
                if not hist2.empty:
                    vols_series = hist2["Volume"].dropna()
                    if len(vols_series) >= 2:
                        vol_ratio = float(vols_series.iloc[-1] / vols_series.mean()) if vols_series.mean() > 0 else 1.0
                changes.append(chg)
                vols.append(vol_ratio)
            except Exception:
                continue
        if changes:
            avg_chg = float(np.mean(changes))
            avg_vol = float(np.mean(vols))
            sig = "Strong Buy" if avg_vol > 1.3 and avg_chg > 2 else \
                  "Buy"        if avg_chg > 0 else \
                  "Sell"       if avg_chg < -2 else "Hold"
            result.append({
                "sector":            sector,
                "avg_change":        round(avg_chg, 2),
                "avg_volume_ratio":  round(avg_vol, 2),
                "signal":            sig,
            })
    return result

