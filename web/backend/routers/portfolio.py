"""Portfolio & Risk Manager router — SQLite + live yfinance prices."""
from fastapi import APIRouter, Body
import sqlite3, yfinance as yf, numpy as np, pandas as pd
from datetime import datetime
from pathlib import Path

router = APIRouter()
_DB = Path(__file__).resolve().parents[3] / "data" / "sarthak_nivesh.db"

def _conn(): return sqlite3.connect(_DB)

def _ensure():
    c = _conn()
    c.execute("""CREATE TABLE IF NOT EXISTS portfolio_holdings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT DEFAULT 'default',
        symbol TEXT NOT NULL, company_name TEXT,
        quantity REAL NOT NULL, buy_price REAL NOT NULL,
        buy_date DATE, sector TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    c.commit(); c.close()

@router.get("/holdings")
def get_holdings():
    _ensure()
    c = _conn()
    rows = c.execute(
        "SELECT id,symbol,company_name,quantity,buy_price,buy_date,sector FROM portfolio_holdings WHERE user_id='default'"
    ).fetchall()
    c.close()
    result = []
    for r in rows:
        id_, sym, name, qty, bp, bd, sec = r
        tsym = sym if sym.endswith(".NS") else sym+".NS"
        try:
            hist = yf.Ticker(tsym).history(period="2d")
            if hist.empty or len(hist) < 2: continue
            cp = float(hist["Close"].iloc[-1])
            pp = float(hist["Close"].iloc[-2])
            today_chg = (cp-pp)/pp*100
            invested  = qty*bp; curr_val = qty*cp
            result.append({
                "id": id_, "symbol": sym, "company_name": name,
                "quantity": qty, "buy_price": bp,
                "current_price": round(cp,2),
                "today_change_pct": round(today_chg,2),
                "invested": round(invested,2),
                "current_value": round(curr_val,2),
                "pnl": round(curr_val-invested,2),
                "pnl_pct": round((curr_val-invested)/invested*100,2) if invested else 0,
                "buy_date": bd, "sector": sec,
            })
        except Exception: continue
    return result

@router.post("/add")
def add_holding(data: dict = Body(...)):
    _ensure()
    c = _conn()
    c.execute("""INSERT INTO portfolio_holdings
        (symbol,company_name,quantity,buy_price,buy_date,sector)
        VALUES(?,?,?,?,?,?)""",
        (data["symbol"], data.get("company_name",""),
         data["quantity"], data["buy_price"],
         data.get("buy_date", datetime.now().strftime("%Y-%m-%d")),
         data.get("sector","Others")))
    c.commit(); c.close()
    return {"status": "added"}

@router.delete("/delete/{holding_id}")
def delete_holding(holding_id: int):
    c = _conn()
    c.execute("DELETE FROM portfolio_holdings WHERE id=?", (holding_id,))
    c.commit(); c.close()
    return {"status": "deleted"}

@router.get("/metrics")
def get_metrics():
    holdings = get_holdings()
    if not holdings:
        return {"empty": True}
    total_inv  = sum(h["invested"] for h in holdings)
    total_curr = sum(h["current_value"] for h in holdings)
    total_pnl  = total_curr - total_inv
    today_pnl  = sum(h["current_value"] - h["invested"] /
                     (1 + h["pnl_pct"]/100) * (1 + h["today_change_pct"]/100)
                     for h in holdings if h["invested"] > 0)
    sectors = {}
    for h in holdings:
        s = h.get("sector","Others")
        sectors[s] = sectors.get(s,0) + h["current_value"]
    return {
        "total_invested":  round(total_inv,2),
        "total_current":   round(total_curr,2),
        "total_pnl":       round(total_pnl,2),
        "total_pnl_pct":   round(total_pnl/total_inv*100,2) if total_inv else 0,
        "num_holdings":    len(holdings),
        "sector_allocation": sectors,
    }
