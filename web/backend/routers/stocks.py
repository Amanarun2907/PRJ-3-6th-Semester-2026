"""Stock Intelligence router — live OHLCV, technicals, fundamentals."""
from fastapi import APIRouter, Query
import yfinance as yf
import pandas as pd
import numpy as np
import math
from datetime import datetime

router = APIRouter()

STOCKS = {
    "HDFCBANK.NS":"HDFC Bank","ICICIBANK.NS":"ICICI Bank","KOTAKBANK.NS":"Kotak Bank",
    "SBIN.NS":"State Bank","AXISBANK.NS":"Axis Bank","INDUSINDBK.NS":"IndusInd Bank",
    "BAJFINANCE.NS":"Bajaj Finance","TCS.NS":"TCS","INFY.NS":"Infosys",
    "WIPRO.NS":"Wipro","HCLTECH.NS":"HCL Tech","TECHM.NS":"Tech Mahindra",
    "RELIANCE.NS":"Reliance","ONGC.NS":"ONGC","NTPC.NS":"NTPC",
    "HINDUNILVR.NS":"HUL","ITC.NS":"ITC","NESTLEIND.NS":"Nestle",
    "MARUTI.NS":"Maruti","M&M.NS":"Mahindra","BAJAJ-AUTO.NS":"Bajaj Auto",
    "SUNPHARMA.NS":"Sun Pharma","DRREDDY.NS":"Dr Reddy","CIPLA.NS":"Cipla",
    "TATASTEEL.NS":"Tata Steel","HINDALCO.NS":"Hindalco","JSWSTEEL.NS":"JSW Steel",
    "LT.NS":"L&T","ULTRACEMCO.NS":"UltraTech","BHARTIARTL.NS":"Airtel",
    "TITAN.NS":"Titan","ASIANPAINT.NS":"Asian Paints","BAJAJFINSV.NS":"Bajaj Finserv",
    "ADANIPORTS.NS":"Adani Ports","COALINDIA.NS":"Coal India",
}


def _safe_float(v):
    try:
        f = float(v)
        return None if (math.isnan(f) or math.isinf(f)) else f
    except Exception:
        return None


def _rsi(series, period=14):
    delta = series.diff()
    gain  = delta.clip(lower=0).rolling(period).mean()
    loss  = (-delta.clip(upper=0)).rolling(period).mean()
    rs    = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def _macd(series):
    ema12  = series.ewm(span=12, adjust=False).mean()
    ema26  = series.ewm(span=26, adjust=False).mean()
    macd   = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal


def _bollinger(series, period=20):
    sma = series.rolling(period).mean()
    std = series.rolling(period).std()
    return sma + 2 * std, sma, sma - 2 * std


def _s(series):
    """Convert pandas series to list, replacing NaN with None."""
    return [round(float(x), 2) if pd.notna(x) and not math.isnan(float(x)) else None
            for x in series.tolist()]


@router.get("/list")
def list_stocks():
    return [{"symbol": k.replace(".NS", ""), "name": v} for k, v in STOCKS.items()]


@router.get("/ohlcv")
def get_ohlcv(symbol: str = Query(...), period: str = Query("6mo")):
    sym = symbol if symbol.endswith(".NS") else symbol + ".NS"
    try:
        hist = yf.Ticker(sym).history(period=period)
        if hist.empty:
            return {"error": "No data"}
        hist = hist.dropna(subset=["Close"])
        if hist.empty:
            return {"error": "No valid data"}
        hist.index = hist.index.strftime("%Y-%m-%d")
        return {
            "dates":  hist.index.tolist(),
            "open":   [round(float(v), 2) if pd.notna(v) else 0.0 for v in hist["Open"]],
            "high":   [round(float(v), 2) if pd.notna(v) else 0.0 for v in hist["High"]],
            "low":    [round(float(v), 2) if pd.notna(v) else 0.0 for v in hist["Low"]],
            "close":  [round(float(v), 2) if pd.notna(v) else 0.0 for v in hist["Close"]],
            "volume": [int(v) if pd.notna(v) else 0 for v in hist["Volume"]],
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/technicals")
def get_technicals(symbol: str = Query(...)):
    sym = symbol if symbol.endswith(".NS") else symbol + ".NS"
    try:
        hist = yf.Ticker(sym).history(period="1y")
        if hist.empty:
            return {"error": "No data"}
        hist  = hist.dropna(subset=["Close"])
        if len(hist) < 30:
            return {"error": "Insufficient data"}
        close = hist["Close"]
        rsi   = _rsi(close)
        macd, sig = _macd(close)
        bb_upper, bb_mid, bb_lower = _bollinger(close)
        ma20  = close.rolling(20).mean()
        ma50  = close.rolling(50).mean()
        ma200 = close.rolling(200).mean()

        rsi_last  = _safe_float(rsi.dropna().iloc[-1])  or 50.0
        macd_last = _safe_float(macd.dropna().iloc[-1]) or 0.0
        sig_last  = _safe_float(sig.dropna().iloc[-1])  or 0.0
        ma50_last = _safe_float(ma50.dropna().iloc[-1]) or float(close.iloc[-1])
        close_last= float(close.iloc[-1])

        score = 0
        if rsi_last < 40:           score += 1
        if rsi_last > 60:           score -= 1
        if macd_last > sig_last:    score += 1
        else:                       score -= 1
        if close_last > ma50_last:  score += 1
        else:                       score -= 1
        signal_label = "BUY" if score >= 2 else "SELL" if score <= -2 else "HOLD"

        return {
            "dates":       hist.index.strftime("%Y-%m-%d").tolist(),
            "close":       _s(close),
            "rsi":         _s(rsi),
            "macd":        _s(macd),
            "macd_signal": _s(sig),
            "bb_upper":    _s(bb_upper),
            "bb_mid":      _s(bb_mid),
            "bb_lower":    _s(bb_lower),
            "ma20":        _s(ma20),
            "ma50":        _s(ma50),
            "ma200":       _s(ma200),
            "signal":      signal_label,
            "rsi_latest":  round(rsi_last, 2),
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/fundamentals")
def get_fundamentals(symbol: str = Query(...)):
    sym = symbol if symbol.endswith(".NS") else symbol + ".NS"
    try:
        info = yf.Ticker(sym).info
        return {
            "name":           info.get("longName", symbol),
            "sector":         info.get("sector", "N/A"),
            "market_cap":     info.get("marketCap", 0) or 0,
            "pe_ratio":       info.get("trailingPE", 0) or 0,
            "pb_ratio":       info.get("priceToBook", 0) or 0,
            "dividend_yield": info.get("dividendYield", 0) or 0,
            "week_52_high":   info.get("fiftyTwoWeekHigh", 0) or 0,
            "week_52_low":    info.get("fiftyTwoWeekLow", 0) or 0,
            "avg_volume":     info.get("averageVolume", 0) or 0,
            "description":    (info.get("longBusinessSummary", "") or "")[:300],
        }
    except Exception as e:
        return {"error": str(e)}
