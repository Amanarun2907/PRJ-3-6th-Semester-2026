# सार्थक निवेश — Sarthak Nivesh

### India's AI-Powered Real-Time Investment Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red?logo=streamlit)](https://streamlit.io/)
[![Groq AI](https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange)](https://console.groq.com/)
[![NSE/BSE](https://img.shields.io/badge/Data-NSE%20%7C%20BSE%20%7C%20AMFI-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

> **सार्थक निवेश** (meaning *Meaningful Investment*) is a full-stack, real-time investment intelligence platform built for Indian retail investors. It tracks 50+ stocks, 2400+ mutual funds, live IPO GMP, institutional FII/DII flows, and delivers AI-powered analysis — all inside a single Streamlit app.

---

## Table of Contents

1. [What is this project?](#1-what-is-this-project)
2. [Who built it?](#2-who-built-it)
3. [Quick Start — Run in 5 minutes](#3-quick-start--run-in-5-minutes)
4. [Project Structure](#4-project-structure)
5. [All 12 Modules — Full Walkthrough](#5-all-12-modules--full-walkthrough)
6. [How the Code is Organised](#6-how-the-code-is-organised)
7. [Data Sources](#7-data-sources)
8. [Technology Stack](#8-technology-stack)
9. [Configuration and API Keys](#9-configuration-and-api-keys)
10. [Database](#10-database)
11. [Key Files Reference](#11-key-files-reference)
12. [Common Issues and Fixes](#12-common-issues-and-fixes)
13. [Disclaimer](#13-disclaimer)

---

## 1. What is this project?

Most Indian retail investors make decisions based on tips, social media, or outdated data. Professional tools are either too expensive or too complex. **सार्थक निवेश** bridges that gap by giving every retail investor access to institutional-grade data and analysis — completely free.

Here is what the platform does end-to-end:

- Pulls **live market data** from NSE, BSE, AMFI, Yahoo Finance, and news RSS feeds every few minutes
- Runs **technical and fundamental analysis** automatically on 50+ stocks across 10 sectors
- Tracks **what big institutions (FII/DII) are doing** with their money in real time
- Provides a **multi-agent AI system** powered by Groq Llama 3.3 70B that can research, analyse, and answer investment questions
- Helps users **plan SIPs with inflation-adjusted goals**, evaluate IPOs, and manage their portfolio with risk metrics
- Explains portfolio losses in plain language (English or Hindi) using live data + AI
- Stores all data locally in a **SQLite database** with auto-save so nothing is lost between sessions
- Exports portfolio data to **Excel/CSV** for offline use

---

## 2. Who built it?

This is a 6th Semester B.Tech project (2026).

| Name | Batch |
|---|---|
| Aman Jain | B.Tech 2023–27 |

GitHub: https://github.com/Amanarun2907/PRJ-3-6th-Semester-2026

---

## 3. Quick Start — Run in 5 minutes

```bash
# 1. Clone the repo
git clone https://github.com/Amanarun2907/PRJ-3-6th-Semester-2026.git
cd PRJ-3-6th-Semester-2026

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Mac / Linux

# 4. Install all dependencies
pip install -r core/requirements.txt

# 5. Add your Groq API key (free at https://console.groq.com)
# Edit the .env file in the root folder:
# GROQ_API_KEY=your_key_here

# 6. Run the app
streamlit run main_ultimate_final.py
```

The app opens automatically at **http://localhost:8501**

> The app works without a Groq API key. The AI assistant falls back to a smart rule-based engine using live market data. For full LLM-powered responses, add the key.

---

## 4. Project Structure

```
PRJ-3-6th-Semester-2026/
|
|-- main_ultimate_final.py              <- SINGLE ENTRY POINT. Always run this.
|-- .env                                <- API keys (gitignored, never pushed)
|-- .gitignore
|-- README.md
|
|-- sections/                           <- All feature modules
|   |-- 01_dashboard/                   <- Live market overview (built into main)
|   |-- 02_stock_intelligence/          <- Stock analysis engine
|   |-- 03_mutual_fund_sip/             <- MF fetcher + SIP calculator + Goal Planner
|   |   |-- realtime_mutual_fund_fetcher.py
|   |   `-- sip_goal_planner.py         <- NEW: Inflation-adjusted SIP Goal Planner
|   |-- 04_ipo_intelligence/            <- IPO tracker + live GMP engine
|   |-- 05_smart_money_tracker/         <- FII/DII + bulk/block deals
|   |-- 06_agentic_ai_hub/              <- Multi-agent AI investment system
|   |-- 07_portfolio_risk/              <- Portfolio manager + risk metrics
|   |   |-- portfolio_risk_manager.py
|   |   |-- database_manager.py
|   |   `-- explain_my_loss.py          <- NEW: AI Finance Coach
|   |-- 08_news_sentiment/              <- News fetcher + sentiment analysis
|   |-- 09_ai_assistant/                <- Groq AI chat assistant
|   `-- 10_advanced_analytics/          <- Sector heatmaps + correlation analysis
|
|-- core/                               <- Shared config, data services
|   |-- config.py                       <- All constants, stock universe, API keys
|   |-- data_service.py                 <- Centralised data fetching layer
|   |-- data_sync_service.py            <- Background sync service
|   `-- requirements.txt                <- All Python dependencies
|
|-- data/                               <- SQLite database (auto-created on first run)
|   `-- sarthak_nivesh.db
|
|-- exports/                            <- Excel/CSV portfolio exports land here
|-- docs/                               <- All markdown documentation
|-- tests/                              <- Test and verification scripts
|-- modules/                            <- Shared utility helpers
`-- scripts_archive/                    <- Old versions kept for reference
```

**How imports work:** `main_ultimate_final.py` adds all `sections/` subfolders and `core/` to `sys.path` at startup, so every module imports cleanly without any path changes needed.

---

## 5. All 12 Modules — Full Walkthrough

### Module 1 — Live Market Dashboard

The home screen. Loads automatically when you open the app.

What you see:
- NIFTY 50 and SENSEX live price with % change
- Top 5 gainers and top 5 losers from the 50-stock universe
- Market breadth indicators
- Quick action buttons: SIP Calculator, Stock Screener, AI Chat

The dashboard fetches NIFTY/SENSEX from Yahoo Finance (`^NSEI`, `^BSESN`). If Yahoo Finance is slow, it falls back to calculating an approximate index movement from the top 5 Nifty stocks.

---

### Module 2 — Stock Intelligence

Deep-dive analysis for any of the 50+ tracked stocks.

What you can do:
- Select any stock from the dropdown (covers Banking, IT, FMCG, Auto, Pharma, Energy, Metals, Cement, Telecom, Real Estate)
- View interactive candlestick charts with volume (powered by Plotly)
- See technical indicators: RSI, MACD, Bollinger Bands, Moving Averages (20/50/200 day)
- Get a buy/hold/sell signal generated from the combined indicator score
- View fundamental data: P/E ratio, market cap, 52-week high/low, dividend yield
- Compare two stocks side by side

Key files:
- `sections/02_stock_intelligence/stock_analyzer.py` — core analysis logic
- `sections/02_stock_intelligence/market_intelligence.py` — market-wide signals
- `sections/02_stock_intelligence/professional_analyzer.py` — advanced scoring

---

### Module 3 — Mutual Fund Center + SIP Calculator

Real-time mutual fund data for 2400+ schemes, fetched live from AMFI and mfapi.in.

What you can do:
- Browse funds by category: Large Cap, Mid Cap, Small Cap, Flexi Cap, Index Funds, ELSS, Debt, Hybrid, Gold & Silver
- See live NAV, 1Y/3Y/5Y returns, expense ratio, AUM, fund manager
- View NAV history chart (up to 1 year) for any fund
- SIP Calculator: enter monthly amount, duration, and expected return to see projected corpus with a growth chart
- Compare up to 3 funds side by side
- Filter by fund house, minimum SIP amount, or star rating

How the data is fetched:
1. `RealtimeMutualFundFetcher` hits the AMFI NAV file (updated daily by AMFI)
2. For historical NAV, it calls `https://api.mfapi.in/mf/{scheme_code}`
3. Returns are calculated from the NAV history
4. Funds are categorised by parsing the scheme name

Key files:
- `sections/03_mutual_fund_sip/realtime_mutual_fund_fetcher.py` — AMFI + mfapi integration
- `sections/03_mutual_fund_sip/mutual_fund_sip_system.py` — SIP calculator logic

---

### Module 4 — IPO Intelligence Hub

Tracks all active, upcoming, and recently listed IPOs with live GMP (Grey Market Premium).

What you can do:
- See currently open IPOs with subscription status, price band, lot size, issue size
- View GMP (Grey Market Premium) — the unofficial premium at which IPO shares trade before listing
- Get an AI-generated IPO score (0–100) based on subscription, GMP, category, and issue size
- See recommended action: APPLY / AVOID / NEUTRAL with reasoning
- Track upcoming IPOs with open/close dates
- View recently listed IPOs with listing gain/loss

How GMP is sourced:
The system scrapes GMP data from public financial sites (Chittorgarh, Moneycontrol) using BeautifulSoup. The IPO score uses real multi-factor scoring: issue size, category (Mainboard vs SME), subscription times, GMP, and status.

Key files:
- `sections/04_ipo_intelligence/realtime_ipo_analyzer.py` — live IPO data engine + real scoring
- `sections/04_ipo_intelligence/ipo_live_engine.py` — GMP scraper
- `sections/04_ipo_intelligence/ipo_predictor.py` — scoring model

---

### Module 5 — Smart Money Tracker

Tracks what Foreign Institutional Investors (FII) and Domestic Institutional Investors (DII) are buying and selling.

What you can do:
- View today's real FII/DII net buy/sell data from NSE API (`/api/fiidiiTradeReact`)
- See bulk deals and block deals from NSE
- Track which sectors are seeing institutional inflows vs outflows
- View a 20-day FII/DII flow chart (today = real NSE data, history = Nifty-proxy estimates clearly labelled)
- See top stocks with unusual volume activity

Data transparency: Row 1 in the table is always real NSE data. Historical rows are Nifty-proxy estimates and are clearly labelled "Estimated" in both the chart and table.

Key files:
- `sections/05_smart_money_tracker/smart_money_live.py` — live FII/DII data from NSE API

---

### Module 6 — Agentic AI Hub

A multi-agent AI system where specialised AI agents collaborate to answer complex investment questions.

Agents available:
- Research Agent — fetches live data about a stock or sector
- Analysis Agent — runs technical and fundamental analysis
- Risk Agent — evaluates risk factors and red flags
- Portfolio Agent — suggests allocation based on your goals
- News Agent — summarises recent news and its market impact

How it works:
1. You type a query like "Should I invest in Reliance right now?"
2. The orchestrator routes it to the relevant agents
3. Each agent fetches live data and generates its part of the answer
4. The final response is synthesised and shown with source attribution

Powered by Groq Llama 3.3 70B. Falls back to rule-based analysis if no API key is set.

Key files:
- `sections/06_agentic_ai_hub/agentic_ai_hub.py` — main UI and orchestrator
- `sections/06_agentic_ai_hub/agentic_ai_engine.py` — agent logic

---

### Module 7 — Portfolio & Risk Manager

A personal portfolio tracker with professional risk metrics.

What you can do:
- Add stocks to your portfolio with buy price, quantity, and date
- See real-time P&L (profit/loss) for each holding fetched live from Yahoo Finance
- View portfolio allocation pie chart by sector
- Risk metrics: Portfolio Beta, Sharpe Ratio, Value at Risk (VaR), Max Drawdown
- Diversification score with suggestions to improve it
- Export your portfolio to Excel with one click
- All data is auto-saved to the local SQLite database

Risk metrics explained:
- Beta: How much your portfolio moves relative to NIFTY (1.0 = same as market)
- Sharpe Ratio: Return per unit of risk (higher is better, >1 is good)
- VaR (95%): Maximum expected loss on a bad day with 95% confidence
- Max Drawdown: Largest peak-to-trough decline in portfolio value

Key files:
- `sections/07_portfolio_risk/portfolio_risk_manager.py` — core risk calculations
- `sections/07_portfolio_risk/database_manager.py` — SQLite persistence
- `sections/07_portfolio_risk/excel_exporter.py` — Excel export

---

### Module 8 — News & Sentiment Analysis

Real-time financial news with AI-powered sentiment scoring.

What you can do:
- Read latest market news from Economic Times, Moneycontrol, and Google Finance RSS feeds
- See sentiment score for each article (Positive / Negative / Neutral) using TextBlob + VADER
- View sector-wise sentiment heatmap (which sectors are in positive/negative news)
- See trending topics extracted from headlines
- Filter news by sector or keyword

Key files:
- `sections/08_news_sentiment/realtime_news_fetcher.py` — RSS feed aggregator
- `sections/08_news_sentiment/sentiment_analyzer.py` — TextBlob + VADER pipeline

---

### Module 9 — AI Investment Assistant

A conversational AI chatbot that answers investment questions using live market data.

What you can do:
- Ask anything: "What is the RSI of TCS?", "Compare HDFC Bank vs ICICI Bank", "Best SIP for 10 years?"
- Quick action buttons for common queries (no typing needed)
- The assistant fetches live data before answering, so responses are always current
- Full conversation history within the session

Key files:
- `sections/09_ai_assistant/groq_ai_analyzer.py` — Groq API integration
- `sections/09_ai_assistant/ai_investment_assistant.py` — chat UI
- `sections/09_ai_assistant/enhanced_quick_actions.py` — rule-based fallback

---

### Module 10 — Advanced Analytics

Macro-level market analysis tools for experienced investors.

What you can do:
- Sector Heatmap: See which sectors are up/down today with colour-coded intensity
- Correlation Matrix: See how correlated different stocks are (useful for diversification)
- Momentum Tracker: Top gainers and losers with live price data
- Volume Intelligence: Detect unusual volume activity across 15 stocks
- Sector Rotation Radar: Visualise which sectors are rotating in/out of favour
- Market Breadth Gauge: Advancing vs declining stocks with A/D ratio

Key files:
- `sections/10_advanced_analytics/advanced_analytics_realtime.py` — main analytics engine
- `sections/10_advanced_analytics/advanced_analytics_alerts.py` — price alert system

---

### Module 11 — 🧠 AI Finance Coach — Explain My Portfolio (NEW)

The real-world problem it solves: Most retail investors panic-sell during market crashes because they don't understand why their portfolio is down. This module explains it in plain language.

How it works:
1. Reads your actual holdings from the SQLite database
2. Fetches today's live price change for every holding via Yahoo Finance
3. Fetches live FII/DII data from NSE API
4. Fetches live sector performance across 10 sectors
5. Fetches live NIFTY 50 change
6. Fetches latest market news from Google Finance RSS
7. Sends all of it to Groq Llama 3.3 70B
8. Returns a plain-language explanation with 4 sections: what happened, main culprits, sell/hold recommendation, one calming insight

Features:
- English and Hindi language toggle
- 6 interactive Plotly charts: today's ₹ P&L per stock, % change bar, portfolio allocation donut, overall P&L bubble chart, sector heatmap, FII/DII gauge
- SELL / HOLD / REVIEW signal card based on AI analysis
- 100% real-time data — no dummy numbers ever

Key file:
- `sections/07_portfolio_risk/explain_my_loss.py`

---

### Module 12 — 🎯 SIP Goal Planner — Inflation-Adjusted (NEW)

The real-world problem it solves: Indians save for specific goals but have no tool that tells them exactly how much SIP they need today, accounting for inflation, to hit a future goal in today's money.

How it works:
1. User enters goal name, target amount in today's ₹, years to goal, inflation rate, existing savings
2. System calculates the inflation-adjusted future value needed
3. Downloads the live AMFI NAV file to find real Direct-Growth funds matching each risk profile
4. Fetches 3Y CAGR for each fund from mfapi.in using the real scheme codes
5. Reverse-calculates the monthly SIP needed for Conservative / Moderate / Aggressive profiles
6. Shows a recommended fund basket from live AMFI data
7. Saves goals to SQLite DB and tracks them over time

Features:
- 3 tabs: Plan a New Goal, My Saved Goals, Recommended Funds (Live AMFI)
- 7 interactive charts: SIP growth projection, inflation impact, SIP comparison, corpus breakdown, goal progress gauge, saved goals overview, per-goal mini chart
- All fund data fetched live from AMFI NAV file — no hardcoded scheme codes
- All returns computed from real NAV history via mfapi.in

Key file:
- `sections/03_mutual_fund_sip/sip_goal_planner.py`

---

## 6. How the Code is Organised

```
User opens browser
        |
        v
main_ultimate_final.py              <- Streamlit entry point
        |
        |-- Adds all sections/ and core/ to sys.path
        |-- Loads .env (GROQ_API_KEY etc.)
        |-- Sets up page config and dark theme CSS
        |-- Defines the 50+ stock universe (INDIAN_STOCKS dict)
        |-- Imports all section modules (with try/except fallbacks)
        |
        |-- Sidebar navigation (12 modules) -> user picks a section
        |
        |-- Module 1:  Dashboard (inline in main)
        |-- Module 2:  calls stock_analyzer.py
        |-- Module 3:  calls realtime_mutual_fund_fetcher.py
        |-- Module 4:  calls sip_goal_planner.py              <- NEW
        |-- Module 5:  calls realtime_ipo_analyzer.py
        |-- Module 6:  calls smart_money_live.py
        |-- Module 7:  calls agentic_ai_hub.py
        |-- Module 8:  calls portfolio_risk_manager.py
        |-- Module 9:  calls explain_my_loss.py               <- NEW
        |-- Module 10: calls realtime_news_fetcher.py
        |-- Module 11: calls groq_ai_analyzer.py
        `-- Module 12: calls advanced_analytics_realtime.py
```

Caching strategy — all data-fetching functions use `@st.cache_data` with TTL values:
- Stock prices: 5 minutes
- Mutual fund NAV: 30 minutes
- News: 10 minutes
- IPO data: 30 minutes

Graceful degradation: Every external module import is wrapped in `try/except`. If a module fails to import, the app still runs — it just shows a warning for that section instead of crashing.

---

## 7. Data Sources

| Data Type | Source | Update Frequency |
|---|---|---|
| Stock prices (50+ stocks) | Yahoo Finance via yfinance | Every 5 min (cached) |
| NIFTY 50 / SENSEX index | Yahoo Finance (`^NSEI`, `^BSESN`) | Every 5 min |
| Mutual fund NAV (2400+ funds) | AMFI NAV file + mfapi.in | Daily (AMFI updates once/day) |
| SIP Goal Planner fund returns | AMFI NAV file + mfapi.in 3Y CAGR | Live on page load |
| IPO data + GMP | Chittorgarh, Moneycontrol (scraped) | Every 30 min |
| FII/DII flows | NSE India API (`/api/fiidiiTradeReact`) | Daily |
| Financial news | Economic Times, Moneycontrol, Google Finance RSS | Every 10 min |
| AI explanations | Groq API (Llama 3.3 70B) | On demand |
| Portfolio data | User's local SQLite DB | Real-time on add/delete |

All data is fetched at runtime — there is no pre-downloaded static dataset.

---

## 8. Technology Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit 1.28+ |
| Charts | Plotly (interactive), Matplotlib, Seaborn |
| Stock data | yfinance, Alpha Vantage |
| Mutual fund data | AMFI NAV file, mfapi.in REST API |
| Web scraping | BeautifulSoup4, requests, lxml |
| AI / LLM | Groq API (Llama 3.3 70B) |
| Sentiment analysis | TextBlob, VADER Sentiment |
| Machine learning | scikit-learn, XGBoost, Prophet |
| Database | SQLite3 (via Python stdlib) |
| Excel export | openpyxl |
| Environment config | python-dotenv |
| Language | Python 3.10+ |

---

## 9. Configuration and API Keys

All configuration lives in two places:

`.env` file (root folder) — for secrets:
```
GROQ_API_KEY=your_groq_api_key_here
ALPHA_VANTAGE_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```
Get a free Groq API key at https://console.groq.com (no credit card needed).

`core/config.py` — for everything else:
- `STOCK_SYMBOLS` — the full 100+ stock universe with NSE ticker symbols
- `NEWS_SOURCES` — RSS feed URLs for news aggregation
- `DATABASE_PATH` — path to the SQLite database
- `PREDICTION_DAYS` — forecast horizons (7, 30, 90 days)

API keys are never hardcoded. They are always loaded from `.env` via `python-dotenv`. The `.env` file is gitignored and never pushed to GitHub.

---

## 10. Database

The app uses a local SQLite database at `data/sarthak_nivesh.db`. It is created automatically on first run.

What gets stored:

| Table | Contents |
|---|---|
| `portfolio_holdings` | Your stock holdings (symbol, buy price, quantity, date, sector) |
| `sip_goals` | Your saved SIP goals (target, years, inflation, monthly SIP, risk profile) |
| `stock_data` | Historical stock price snapshots |
| `sector_performance` | Sector % change history |
| `news_sentiment` | News articles with sentiment scores |
| `market_breadth` | Daily advancing/declining stock counts |
| `volume_analysis` | Unusual volume activity records |
| `alert_events` | Triggered price/news alerts |

The database is managed by `sections/07_portfolio_risk/database_manager.py`. The file is gitignored so your personal data is never pushed to GitHub.

---

## 11. Key Files Reference

| File | What it does |
|---|---|
| `main_ultimate_final.py` | Single entry point. Run this with `streamlit run`. |
| `core/config.py` | All constants: stock universe, API keys loaded from env, paths |
| `core/data_service.py` | Centralised data fetching layer used by multiple sections |
| `core/requirements.txt` | All Python dependencies with pinned versions |
| `sections/02_stock_intelligence/stock_analyzer.py` | Technical analysis engine (RSI, MACD, Bollinger Bands) |
| `sections/03_mutual_fund_sip/realtime_mutual_fund_fetcher.py` | Fetches 2400+ fund NAVs from AMFI |
| `sections/03_mutual_fund_sip/sip_goal_planner.py` | SIP Goal Planner — live AMFI returns, inflation math, 7 charts |
| `sections/04_ipo_intelligence/realtime_ipo_analyzer.py` | Live IPO data + real multi-factor scoring |
| `sections/05_smart_money_tracker/smart_money_live.py` | Live FII/DII flow from NSE API |
| `sections/06_agentic_ai_hub/agentic_ai_hub.py` | Multi-agent AI orchestrator |
| `sections/07_portfolio_risk/portfolio_risk_manager.py` | Portfolio P&L + risk metrics (Beta, Sharpe, VaR) |
| `sections/07_portfolio_risk/database_manager.py` | SQLite read/write for all platform data |
| `sections/07_portfolio_risk/explain_my_loss.py` | AI Finance Coach — explains portfolio moves in English/Hindi |
| `sections/08_news_sentiment/realtime_news_fetcher.py` | RSS news aggregator |
| `sections/08_news_sentiment/sentiment_analyzer.py` | TextBlob + VADER sentiment pipeline |
| `sections/09_ai_assistant/groq_ai_analyzer.py` | Groq Llama 3.3 70B integration |
| `sections/10_advanced_analytics/advanced_analytics_realtime.py` | Sector heatmaps, correlation matrix, market breadth |
| `data/sarthak_nivesh.db` | Local SQLite database (auto-created) |

---

## 12. Common Issues and Fixes

**App crashes on startup with ImportError**
All section imports are wrapped in try/except, so the app should not crash. If it does, run:
```bash
pip install -r core/requirements.txt
```

**NIFTY/SENSEX shows 0 or N/A**
Yahoo Finance occasionally rate-limits requests. The app has 4 fallback methods. Wait 1–2 minutes and refresh.

**Mutual funds show "No data"**
AMFI updates their NAV file once per day (usually after 8 PM IST). If the AMFI server is temporarily down, the section will show an error message.

**SIP Goal Planner shows "Could not fetch funds"**
This means the AMFI NAV file or mfapi.in is temporarily unreachable. Check your internet connection and try again. The app will show fallback return rates if live data is unavailable.

**Portfolio shows empty after adding stocks**
This was a known bug (`.NS` suffix doubling) that has been fixed. If you still see it, clear your browser cache and restart the app.

**AI Finance Coach shows no explanation**
Make sure your `GROQ_API_KEY` is set in the `.env` file. The key must start with `gsk_`. Get a free key at https://console.groq.com.

**Port 8501 already in use**
```bash
streamlit run main_ultimate_final.py --server.port 8502
```

**Slow first load**
The first load fetches live data from multiple sources simultaneously. Subsequent loads are fast because of Streamlit's `@st.cache_data` caching. Expect 15–30 seconds on first load.

---

## 13. Disclaimer

This platform is built for **educational purposes** as part of a B.Tech academic project.

- Nothing on this platform is financial advice
- Stock prices, NAVs, and IPO data are fetched from public sources and may have delays
- Past returns shown for mutual funds do not guarantee future performance
- Always consult a SEBI-registered financial advisor before making investment decisions
- The developers are not responsible for any financial decisions made based on this platform

---

*Built with love for Indian retail investors. सार्थक निवेश — Invest Meaningfully.*
