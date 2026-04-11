"""
Agentic AI Hub — Multi-Agent Investment Intelligence
6 specialist agents run in sequence, each fetching live data,
then a Master Agent synthesises a complete investment report.

Agents:
  1. Stock Intelligence Agent  — live prices, technicals, signals
  2. Market Analysis Agent     — NIFTY, SENSEX, breadth, sector heatmap
  3. Smart Money Agent         — FII/DII flows from NSE API
  4. News & Sentiment Agent    — live RSS headlines + VADER sentiment
  5. Risk Management Agent     — volatility, correlation, VaR estimate
  6. Advanced Analytics Agent  — sector rotation, volume anomalies
  7. Master Report Agent       — synthesises all 6 into final report
"""
from fastapi import APIRouter, Body
import os, requests, yfinance as yf, feedparser, re
import numpy as np, pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

router = APIRouter()
_vader = SentimentIntensityAnalyzer()

_HDR = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/html, */*",
    "Referer": "https://www.nseindia.com/",
}

WATCHLIST = [
    "RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS",
    "HINDUNILVR.NS","ITC.NS","SBIN.NS","BHARTIARTL.NS","KOTAKBANK.NS",
    "LT.NS","AXISBANK.NS","WIPRO.NS","MARUTI.NS","TITAN.NS",
    "BAJFINANCE.NS","SUNPHARMA.NS","TATASTEEL.NS","NTPC.NS","ADANIPORTS.NS",
]
SECTOR_MAP = {
    "Banking":  ["HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","KOTAKBANK.NS","AXISBANK.NS"],
    "IT":       ["TCS.NS","INFY.NS","WIPRO.NS","HCLTECH.NS"],
    "Energy":   ["RELIANCE.NS","ONGC.NS","NTPC.NS"],
    "FMCG":     ["HINDUNILVR.NS","ITC.NS","NESTLEIND.NS"],
    "Auto":     ["MARUTI.NS","TATAMOTORS.NS","BAJAJ-AUTO.NS"],
    "Pharma":   ["SUNPHARMA.NS","DRREDDY.NS","CIPLA.NS"],
    "Metals":   ["TATASTEEL.NS","HINDALCO.NS","JSWSTEEL.NS"],
    "Telecom":  ["BHARTIARTL.NS"],
}

# ── Groq helper ───────────────────────────────────────────────────────────────

def _groq(prompt: str, system: str, max_tokens: int = 600) -> str:
    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        return "⚠️ GROQ_API_KEY not set. Add it to .env for AI analysis."
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {key}"},
            json={"model": "llama-3.3-70b-versatile", "temperature": 0.55,
                  "max_tokens": max_tokens,
                  "messages": [
                      {"role": "system", "content": system},
                      {"role": "user",   "content": prompt},
                  ]},
            timeout=40,
        )
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        return f"Groq error {r.status_code}"
    except Exception as e:
        return f"Groq call failed: {e}"

# ── Agent 1: Stock Intelligence ───────────────────────────────────────────────

def agent_stock_intelligence(query: str) -> dict:
    """Fetch live prices + technicals for top stocks."""
    results = []
    for sym in WATCHLIST[:12]:
        try:
            hist = yf.Ticker(sym).history(period="3mo")
            if hist.empty or len(hist) < 20:
                continue
            close = hist["Close"]
            # RSI
            delta = close.diff()
            gain  = delta.clip(lower=0).rolling(14).mean()
            loss  = (-delta.clip(upper=0)).rolling(14).mean()
            rs    = gain / loss.replace(0, np.nan)
            rsi   = float((100 - 100/(1+rs)).iloc[-1])
            # MACD
            ema12 = close.ewm(span=12).mean()
            ema26 = close.ewm(span=26).mean()
            macd  = float((ema12 - ema26).iloc[-1])
            sig   = float((ema12 - ema26).ewm(span=9).mean().iloc[-1])
            # Price change
            chg   = float((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100)
            price = float(close.iloc[-1])
            # Signal
            score = 0
            if rsi < 40: score += 1
            if rsi > 60: score -= 1
            if macd > sig: score += 1
            else: score -= 1
            if close.iloc[-1] > close.rolling(50).mean().iloc[-1]: score += 1
            else: score -= 1
            signal = "BUY" if score >= 2 else "SELL" if score <= -2 else "HOLD"
            results.append({
                "symbol": sym.replace(".NS",""),
                "price":  round(price, 2),
                "change_pct": round(chg, 2),
                "rsi":    round(rsi, 1),
                "macd_signal": signal,
            })
        except Exception:
            continue

    # AI analysis
    top_buy  = [r for r in results if r["macd_signal"] == "BUY"][:3]
    top_sell = [r for r in results if r["macd_signal"] == "SELL"][:3]
    data_txt = "\n".join([
        f"  {r['symbol']}: ₹{r['price']} | {r['change_pct']:+.2f}% | RSI {r['rsi']} | {r['macd_signal']}"
        for r in results
    ])
    analysis = _groq(
        f"User query: {query}\n\nLive stock data:\n{data_txt}\n\n"
        "Provide a 3-4 sentence stock market analysis. Highlight top BUY and SELL signals. "
        "Mention specific stocks with their RSI and price action.",
        "You are a stock market analyst. Be concise and data-driven.",
        max_tokens=250,
    )
    return {
        "agent": "Stock Intelligence",
        "icon":  "📊",
        "stocks": results,
        "top_buy":  top_buy,
        "top_sell": top_sell,
        "analysis": analysis,
        "status": "complete",
    }

# ── Agent 2: Market Analysis ──────────────────────────────────────────────────

def agent_market_analysis(query: str) -> dict:
    """NIFTY, SENSEX, sector performance."""
    indices = {}
    for name, sym in [("NIFTY 50","^NSEI"),("SENSEX","^BSESN")]:
        try:
            hist = yf.Ticker(sym).history(period="5d")
            if len(hist) >= 2:
                chg = float((hist["Close"].iloc[-1]-hist["Close"].iloc[-2])/hist["Close"].iloc[-2]*100)
                indices[name] = {"value": round(float(hist["Close"].iloc[-1]),2),
                                 "change_pct": round(chg,2)}
        except Exception:
            pass

    sector_perf = {}
    for sector, tickers in SECTOR_MAP.items():
        changes = []
        for t in tickers:
            try:
                hist = yf.Ticker(t).history(period="2d")
                if len(hist) >= 2:
                    changes.append(float((hist["Close"].iloc[-1]-hist["Close"].iloc[-2])/hist["Close"].iloc[-2]*100))
            except Exception:
                pass
        if changes:
            sector_perf[sector] = round(float(np.mean(changes)), 2)

    best   = max(sector_perf, key=sector_perf.get) if sector_perf else "N/A"
    worst  = min(sector_perf, key=sector_perf.get) if sector_perf else "N/A"
    idx_txt = "\n".join([f"  {k}: {v['value']:,.0f} ({v['change_pct']:+.2f}%)" for k,v in indices.items()])
    sec_txt = "\n".join([f"  {k}: {v:+.2f}%" for k,v in sorted(sector_perf.items(), key=lambda x: x[1], reverse=True)])

    analysis = _groq(
        f"User query: {query}\n\nMarket data:\n{idx_txt}\n\nSector performance:\n{sec_txt}\n\n"
        "Provide a 3-4 sentence market analysis. Comment on index direction, "
        "best and worst sectors, and overall market mood.",
        "You are a market analyst. Be concise and specific.",
        max_tokens=250,
    )
    return {
        "agent":       "Market Analysis",
        "icon":        "📈",
        "indices":     indices,
        "sector_perf": sector_perf,
        "best_sector": best,
        "worst_sector":worst,
        "analysis":    analysis,
        "status":      "complete",
    }

# ── Agent 3: Smart Money ──────────────────────────────────────────────────────

def agent_smart_money(query: str) -> dict:
    """FII/DII from NSE API."""
    def _n(v):
        try:
            m = re.findall(r"-?\d+\.?\d*", str(v).replace(",",""))
            return float(m[0]) if m else 0.0
        except Exception: return 0.0

    fii_net = dii_net = None
    date_str = ""
    source = "Unavailable"
    try:
        sess = requests.Session(); sess.headers.update(_HDR)
        r = sess.get("https://www.nseindia.com/api/fiidiiTradeReact", timeout=15)
        if r.status_code == 200:
            data = r.json()
            fii = next((x for x in data if "FII" in x.get("category","").upper()), None)
            dii = next((x for x in data if "DII" in x.get("category","").upper()), None)
            if fii or dii:
                fii_net  = _n((fii or {}).get("netValue", 0))
                dii_net  = _n((dii or {}).get("netValue", 0))
                date_str = (fii or dii or {}).get("date","")
                source   = "NSE Live"
    except Exception as e:
        print(f"FII/DII error: {e}")

    signal = "NEUTRAL"
    if fii_net is not None and dii_net is not None:
        if fii_net > 1000 and dii_net > 1000:   signal = "STRONG BUY"
        elif fii_net > 0 and dii_net > 0:        signal = "BUY"
        elif fii_net < -1000 and dii_net < -1000:signal = "STRONG SELL"
        elif fii_net < 0 and dii_net < 0:        signal = "SELL"

    data_txt = (f"FII Net: ₹{fii_net:+,.0f} Cr | DII Net: ₹{dii_net:+,.0f} Cr | Date: {date_str}"
                if fii_net is not None else "FII/DII data unavailable")
    analysis = _groq(
        f"User query: {query}\n\nInstitutional flow data:\n{data_txt}\n\n"
        "Provide a 2-3 sentence analysis of what institutional investors are doing "
        "and what it means for retail investors.",
        "You are an institutional flow analyst. Be direct.",
        max_tokens=200,
    )
    return {
        "agent":   "Smart Money Tracker",
        "icon":    "🏦",
        "fii_net": fii_net,
        "dii_net": dii_net,
        "date":    date_str,
        "source":  source,
        "signal":  signal,
        "analysis":analysis,
        "status":  "complete",
    }

# ── Agent 4: News & Sentiment ─────────────────────────────────────────────────

def agent_news_sentiment(query: str) -> dict:
    """Live RSS news + VADER sentiment."""
    articles = []
    feeds = [
        ("https://news.google.com/rss/search?q=indian+stock+market+NSE+BSE&hl=en-IN&gl=IN&ceid=IN:en", "Google Finance"),
        ("https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms", "Economic Times"),
    ]
    for url, src in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:
                title = entry.get("title","")
                if not title: continue
                score = _vader.polarity_scores(title)["compound"]
                articles.append({
                    "title":     title,
                    "source":    src,
                    "sentiment": "Positive" if score>0.05 else "Negative" if score<-0.05 else "Neutral",
                    "score":     round(score,3),
                })
        except Exception:
            pass

    pos = sum(1 for a in articles if a["sentiment"]=="Positive")
    neg = sum(1 for a in articles if a["sentiment"]=="Negative")
    neu = sum(1 for a in articles if a["sentiment"]=="Neutral")
    avg_score = round(float(np.mean([a["score"] for a in articles])),3) if articles else 0
    overall = "Positive" if avg_score>0.05 else "Negative" if avg_score<-0.05 else "Neutral"

    headlines = "\n".join([f"  [{a['sentiment']}] {a['title'][:70]}" for a in articles[:8]])
    analysis = _groq(
        f"User query: {query}\n\nLatest market headlines:\n{headlines}\n\n"
        f"Overall sentiment: {overall} (score: {avg_score})\n\n"
        "Provide a 3-4 sentence news sentiment analysis. What are the key themes? "
        "How does the news sentiment affect investment decisions?",
        "You are a financial news analyst. Be concise.",
        max_tokens=250,
    )
    return {
        "agent":     "News & Sentiment",
        "icon":      "📰",
        "articles":  articles[:10],
        "positive":  pos,
        "negative":  neg,
        "neutral":   neu,
        "avg_score": avg_score,
        "overall":   overall,
        "analysis":  analysis,
        "status":    "complete",
    }

# ── Agent 5: Risk Management ──────────────────────────────────────────────────

def agent_risk_management(query: str) -> dict:
    """Volatility, correlation, VaR estimate."""
    returns_data = {}
    for sym in WATCHLIST[:10]:
        try:
            hist = yf.Ticker(sym).history(period="1y")
            if not hist.empty and len(hist) > 50:
                returns_data[sym.replace(".NS","")] = hist["Close"].pct_change().dropna()
        except Exception:
            pass

    risk_metrics = {}
    if returns_data:
        df = pd.DataFrame(returns_data).dropna()
        for col in df.columns:
            vol  = float(df[col].std() * np.sqrt(252) * 100)
            var  = float(np.percentile(df[col], 5) * 100)
            risk_metrics[col] = {"volatility": round(vol,2), "var_95": round(var,2)}

    # Portfolio-level (equal weight)
    if len(returns_data) > 1:
        df = pd.DataFrame(returns_data).dropna()
        port_ret = df.mean(axis=1)
        port_vol = float(port_ret.std() * np.sqrt(252) * 100)
        port_var = float(np.percentile(port_ret, 5) * 100)
        corr_matrix = df.corr()
        avg_corr = float(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean())
    else:
        port_vol = port_var = avg_corr = 0

    risk_txt = "\n".join([
        f"  {sym}: Volatility {m['volatility']}% | VaR(95%) {m['var_95']}%"
        for sym, m in list(risk_metrics.items())[:8]
    ])
    analysis = _groq(
        f"User query: {query}\n\nRisk metrics:\n{risk_txt}\n"
        f"Portfolio volatility: {port_vol:.1f}% | Portfolio VaR(95%): {port_var:.2f}% | "
        f"Avg correlation: {avg_corr:.2f}\n\n"
        "Provide a 3-4 sentence risk assessment. Which stocks are most/least risky? "
        "What does the correlation level mean for diversification?",
        "You are a risk management expert. Be specific and actionable.",
        max_tokens=250,
    )
    return {
        "agent":        "Risk Management",
        "icon":         "🛡️",
        "risk_metrics": risk_metrics,
        "portfolio_volatility": round(port_vol,2),
        "portfolio_var":        round(port_var,2),
        "avg_correlation":      round(avg_corr,3),
        "analysis":     analysis,
        "status":       "complete",
    }

# ── Agent 6: Advanced Analytics ───────────────────────────────────────────────

def agent_advanced_analytics(query: str) -> dict:
    """Volume anomalies + sector rotation signals."""
    volume_alerts = []
    for sym in WATCHLIST[:15]:
        try:
            hist = yf.Ticker(sym).history(period="10d")
            if len(hist) >= 5:
                cv = float(hist["Volume"].iloc[-1])
                av = float(hist["Volume"].mean())
                vr = cv / av if av > 0 else 1
                cp = float(hist["Close"].iloc[-1])
                pp = float(hist["Close"].iloc[-2])
                chg = (cp-pp)/pp*100
                if vr > 1.5:
                    volume_alerts.append({
                        "symbol":       sym.replace(".NS",""),
                        "volume_ratio": round(vr,2),
                        "price_change": round(chg,2),
                        "signal":       "Bullish Breakout" if chg>0 else "Bearish Breakdown",
                    })
        except Exception:
            pass

    # Sector momentum (1M vs 1W)
    sector_momentum = {}
    for sector, tickers in SECTOR_MAP.items():
        week_changes, month_changes = [], []
        for t in tickers:
            try:
                hist = yf.Ticker(t).history(period="1mo")
                if len(hist) >= 5:
                    week_changes.append(float((hist["Close"].iloc[-1]-hist["Close"].iloc[-5])/hist["Close"].iloc[-5]*100))
                    month_changes.append(float((hist["Close"].iloc[-1]-hist["Close"].iloc[0])/hist["Close"].iloc[0]*100))
            except Exception:
                pass
        if week_changes:
            sector_momentum[sector] = {
                "week":  round(float(np.mean(week_changes)),2),
                "month": round(float(np.mean(month_changes)),2),
            }

    alerts_txt = "\n".join([
        f"  {a['symbol']}: {a['volume_ratio']}x volume | {a['price_change']:+.2f}% | {a['signal']}"
        for a in volume_alerts[:6]
    ]) or "  No unusual volume detected"
    momentum_txt = "\n".join([
        f"  {s}: 1W {v['week']:+.2f}% | 1M {v['month']:+.2f}%"
        for s,v in sorted(sector_momentum.items(), key=lambda x: x[1]['week'], reverse=True)
    ])
    analysis = _groq(
        f"User query: {query}\n\nVolume anomalies:\n{alerts_txt}\n\nSector momentum:\n{momentum_txt}\n\n"
        "Provide a 3-4 sentence advanced analytics insight. Which sectors show rotation? "
        "What do the volume anomalies suggest?",
        "You are an advanced market analytics expert. Be specific.",
        max_tokens=250,
    )
    return {
        "agent":            "Advanced Analytics",
        "icon":             "📈",
        "volume_alerts":    volume_alerts,
        "sector_momentum":  sector_momentum,
        "analysis":         analysis,
        "status":           "complete",
    }

# ── Master Report Agent ───────────────────────────────────────────────────────

def agent_master_report(query: str, agent_results: list) -> str:
    """Synthesise all 6 agent outputs into a final investment report."""
    summaries = "\n\n".join([
        f"=== {r['agent']} ===\n{r.get('analysis','No analysis')}"
        for r in agent_results
    ])
    prompt = f"""
You are the Master Investment Advisor. You have received reports from 6 specialist agents.
Synthesise them into a comprehensive investment report for this query: "{query}"

Agent Reports:
{summaries}

Write a structured investment report with these sections:
1. **Executive Summary** (2-3 sentences — overall market verdict)
2. **Top Investment Opportunities** (3 specific stocks/sectors with reasoning)
3. **Key Risks to Watch** (3 specific risks from the data)
4. **Smart Money Signal** (what institutions are doing and what it means)
5. **Recommended Action Plan** (3 concrete steps for the investor)
6. **Confidence Level** (High/Medium/Low with one sentence reason)

Be specific, data-driven, and actionable. Use ₹ for amounts. Under 400 words.
""".strip()
    return _groq(
        prompt,
        "You are a senior investment advisor synthesising multi-agent research. "
        "Be authoritative, specific, and actionable.",
        max_tokens=700,
    )

# ── Route ─────────────────────────────────────────────────────────────────────

@router.post("/run")
def run_agents(data: dict):
    query = data.get("query", "Give me a complete market analysis and investment recommendation")
    agents_to_run = data.get("agents", ["stock","market","smartmoney","news","risk","analytics"])

    results = []
    agent_map = {
        "stock":      agent_stock_intelligence,
        "market":     agent_market_analysis,
        "smartmoney": agent_smart_money,
        "news":       agent_news_sentiment,
        "risk":       agent_risk_management,
        "analytics":  agent_advanced_analytics,
    }

    for agent_id in agents_to_run:
        if agent_id in agent_map:
            try:
                result = agent_map[agent_id](query)
                results.append(result)
            except Exception as e:
                results.append({
                    "agent":    agent_id,
                    "icon":     "⚠️",
                    "analysis": f"Agent failed: {e}",
                    "status":   "error",
                })

    # Master report
    master = agent_master_report(query, results)

    return {
        "query":         query,
        "agent_results": results,
        "master_report": master,
        "timestamp":     datetime.now().isoformat(),
        "agents_run":    len(results),
    }
