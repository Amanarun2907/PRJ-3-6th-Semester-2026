"""Stock Intelligence router — live OHLCV, technicals, fundamentals."""
from fastapi import APIRouter, Query
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

router = APIRouter()

STOCKS = {
    "HDFCBANK.NS":"HDFC Bank","ICICIBANK.NS":"ICICI Bank","KOTAKBANK.NS":"Kotak Bank",
    "SBIN.NS":"State Bank","AXISBANK.NS":"Axis Bank","INDUSINDBK.NS":"IndusInd Bank",
    "BAJFINANCE.NS":"Bajaj Finance","TCS.NS":"TCS","INFY.NS":"Infosys",
    "WIPRO.NS":"Wipro","HCLTECH.NS":"HCL Tech","TECHM.NS":"Tech Mahindra",
    "RELIANCE.NS":"Reliance","ONGC.NS":"ONGC","NTPC.NS":"NTPC",
    "HINDUNILVR.NS":"HUL","ITC.NS":"ITC","NESTLEIND.NS":"Nestle",
    "MARUTI.NS":"Maruti","TATAMOTORS.NS":"Tata Motors","BAJAJ-AUTO.NS":"Bajaj Auto",
    "SUNPHARMA.NS":"Sun Pharma","DRREDDY.NS":"Dr Reddy","CIPLA.NS":"Cipla",
    "TATASTEEL.NS":"Tata Steel","HINDALCO.NS":"Hindalco","JSWSTEEL.NS":"JSW Steel",
    "LT.NS":"L&T","ULTRACEMCO.NS":"UltraTech","BHARTIARTL.NS":"Airtel",
    "TITAN.NS":"Titan","ASIANPAINT.NS":"Asian Paints","BAJAJFINSV.NS":"Bajaj Finserv",
    "ADANIPORTS.NS":"Adani Ports","COALINDIA.NS":"Coal India","M&M.NS":"M&M",
}

def _rsi(series, period=14):
    delta = series.diff()
    gain  = delta.clip(lower=0).rolling(period).mean()
    loss  = (-delta.clip(upper=0)).rolling(period).mean()
    rs    = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def _macd(series):
    ema12 = series.ewm(span=12, adjust=False).mean()
    ema26 = series.ewm(span=26, adjust=False).mean()
    macd  = ema12 - ema26
    signal= macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def _bollinger(series, period=20):
    sma  = series.rolling(period).mean()
    std  = series.rolling(period).std()
    return sma + 2*std, sma, sma - 2*std

@router.get("/list")
def list_stocks():
    return [{"symbol": k.replace(".NS",""), "name": v} for k, v in STOCKS.items()]

@router.get("/ohlcv")
def get_ohlcv(symbol: str = Query(...), period: str = Query("6mo")):
    sym = symbol if symbol.endswith(".NS") else symbol + ".NS"
    try:
        hist = yf.Ticker(sym).history(period=period)
        if hist.empty:
            return {"error": "No data"}
        hist.index = hist.index.strftime("%Y-%m-%d")
        return {
            "dates":  hist.index.tolist(),
            "open":   hist["Open"].round(2).tolist(),
            "high":   hist["High"].round(2).tolist(),
            "low":    hist["Low"].round(2).tolist(),
            "close":  hist["Close"].round(2).tolist(),
            "volume": hist["Volume"].tolist(),
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/technicals")
def get_technicals(symbol: str = Query(...)):
    sym = symbol if symbol.endswith(".NS") else symbol + ".NS"
    try:
        hist = yf.Ticker(sym).history(period="1y")
        if hist.empty or len(hist) < 30:
            return {"error": "Insufficient data"}
        close = hist["Close"]
        rsi   = _rsi(close)
        macd, signal = _macd(close)
        bb_upper, bb_mid, bb_lower = _bollinger(close)
        ma20  = close.rolling(20).mean()
        ma50  = close.rolling(50).mean()
        ma200 = close.rolling(200).mean()

        # Signal
        score = 0
        if rsi.iloc[-1] < 40:   score += 1
        if rsi.iloc[-1] > 60:   score -= 1
        if macd.iloc[-1] > signal.iloc[-1]: score += 1
        else: score -= 1
        if close.iloc[-1] > ma50.iloc[-1]:  score += 1
        else: score -= 1
        signal_label = "BUY" if score >= 2 else "SELL" if score <= -2 else "HOLD"

        def _s(series):
            return [round(x, 2) if not np.isnan(x) else None for x in series.tolist()]

        return {
            "dates":    hist.index.strftime("%Y-%m-%d").tolist(),
            "close":    _s(close),
            "rsi":      _s(rsi),
            "macd":     _s(macd),
            "macd_signal": _s(signal),
            "bb_upper": _s(bb_upper),
            "bb_mid":   _s(bb_mid),
            "bb_lower": _s(bb_lower),
            "ma20":     _s(ma20),
            "ma50":     _s(ma50),
            "ma200":    _s(ma200),
            "signal":   signal_label,
            "rsi_latest": round(float(rsi.iloc[-1]), 2),
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/fundamentals")
def get_fundamentals(symbol: str = Query(...)):
    sym = symbol if symbol.endswith(".NS") else symbol + ".NS"
    try:
        info = yf.Ticker(sym).info
        return {
            "name":          info.get("longName", symbol),
            "sector":        info.get("sector", "N/A"),
            "market_cap":    info.get("marketCap", 0),
            "pe_ratio":      info.get("trailingPE", 0),
            "pb_ratio":      info.get("priceToBook", 0),
            "dividend_yield":info.get("dividendYield", 0),
            "week_52_high":  info.get("fiftyTwoWeekHigh", 0),
            "week_52_low":   info.get("fiftyTwoWeekLow", 0),
            "avg_volume":    info.get("averageVolume", 0),
            "description":   info.get("longBusinessSummary", "")[:300],
        }
    except Exception as e:
        return {"error": str(e)}
