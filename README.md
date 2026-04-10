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
5. [The 10 Sections — Full Walkthrough](#5-the-10-sections--full-walkthrough)
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
- Helps users **plan SIPs, evaluate IPOs, and manage their portfolio** with risk metrics
- Stores all data locally in a **SQLite database** with auto-save so nothing is lost between sessions
- Exports portfolio data to **Excel/CSV** for offline use

---

## 2. Who built it?

This is a 6th Semester B.Tech project (2026).

| Name | Role |
|---|---|
| Aman Arun | Lead Developer |
| Rohit Fogla | Backend & Data |
| Vanshita Mehta | UI/UX & Frontend |
| Disita Tirthani | AI & Analytics |

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
|-- main_ultimate_final.py        <- SINGLE ENTRY POINT. Always run this.
|-- .env                          <- API keys (gitignored, never pushed)
|-- .gitignore
|-- README.md
|
|-- sections/                     <- All 10 feature modules
|   |-- 01_dashboard/             <- Live market overview (built into main)
|   |-- 02_stock_intelligence/    <- Stock analysis engine
|   |-- 03_mutual_fund_sip/       <- MF real-time fetcher + SIP calculator
|   |-- 04_ipo_intelligence/      <- IPO tracker + live GMP engine
|   |-- 05_smart_money_tracker/   <- FII/DII + bulk/block deals
|   |-- 06_agentic_ai_hub/        <- Multi-agent AI investment system
|   |-- 07_portfolio_risk/        <- Portfolio manager + risk metrics
|   |-- 08_news_sentiment/        <- News fetcher + sentiment analysis
|   |-- 09_ai_assistant/          <- Groq AI chat assistant
|   `-- 10_advanced_analytics/    <- Sector heatmaps + correlation analysis
|
|-- core/                         <- Shared config, data services, run scripts
|   |-- config.py                 <- All constants, stock universe, API keys
|   |-- data_service.py           <- Centralised data fetching layer
|   |-- data_sync_service.py      <- Background sync service
|   `-- requirements.txt          <- All Python dependencies
|
|-- data/                         <- SQLite database (auto-created on first run)
|   `-- sarthak_nivesh.db
|
|-- exports/                      <- Excel/CSV portfolio exports land here
|-- docs/                         <- All markdown documentation
|-- tests/                        <- Test and verification scripts
|-- modules/                      <- Shared utility helpers
`-- scripts_archive/              <- Old versions kept for reference
```

**How imports work:** `main_ultimate_final.py` adds all `sections/` subfolders and `core/` to `sys.path` at startup, so every module imports cleanly without any path changes needed.

---

## 5. The 10 Sections — Full Walkthrough

### Section 1 — Live Market Dashboard

The home screen. Loads automatically when you open the app.

What you see:
- NIFTY 50 and SENSEX live price with % change
- Top 5 gainers and top 5 losers from the 50-stock universe
- Market breadth indicators
- Quick action buttons: SIP Calculator, Stock Screener, AI Chat

The dashboard fetches NIFTY/SENSEX from Yahoo Finance (`^NSEI`, `^BSESN`). If Yahoo Finance is slow, it falls back to calculating an approximate index movement from the top 5 Nifty stocks.

---

### Section 2 — Stock Intelligence

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

### Section 3 — Mutual Fund Center + SIP Calculator

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

### Section 4 — IPO Intelligence Hub

Tracks all active, upcoming, and recently listed IPOs with live GMP (Grey Market Premium).

What you can do:
- See currently open IPOs with subscription status, price band, lot size, issue size
- View GMP (Grey Market Premium) — the unofficial premium at which IPO shares trade before listing
- Get an AI-generated IPO score (0-100) based on subscription, GMP, sector, and financials
- See recommended action: APPLY / AVOID / NEUTRAL with reasoning
- Track upcoming IPOs with open/close dates
- View recently listed IPOs with listing gain/loss

How GMP is sourced:
The system scrapes GMP data from public financial sites (Chittorgarh, IPO Watch) using BeautifulSoup. If scraping fails, it falls back to a curated list of recent IPOs with their last known status.

Key files:
- `sections/04_ipo_intelligence/realtime_ipo_analyzer.py` — live IPO data engine
- `sections/04_ipo_intelligence/ipo_live_engine.py` — GMP scraper
- `sections/04_ipo_intelligence/ipo_predictor.py` — scoring model

---

### Section 5 — Smart Money Tracker

Tracks what Foreign Institutional Investors (FII) and Domestic Institutional Investors (DII) are buying and selling.

What you can do:
- View daily FII/DII net buy/sell data (equity + debt)
- See bulk deals and block deals from NSE
- Track which sectors are seeing institutional inflows vs outflows
- View a 30-day FII/DII flow chart
- See top stocks with highest institutional activity

Why this matters: FII/DII flows are one of the strongest leading indicators of market direction. When FIIs are net buyers for multiple consecutive days, it usually signals bullish momentum.

Key files:
- `sections/05_smart_money_tracker/smart_money_live.py` — live FII/DII data
- `sections/05_smart_money_tracker/smart_money_tracker.py` — fallback static tracker

---

### Section 6 — Agentic AI Hub

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
- `sections/06_agentic_ai_hub/agentic_ai_system.py` — multi-agent coordination

---

### Section 7 — Portfolio & Risk Manager

A personal portfolio tracker with professional risk metrics.

What you can do:
- Add stocks to your portfolio with buy price, quantity, and date
- See real-time P&L (profit/loss) for each holding
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

### Section 8 — News & Sentiment Analysis

Real-time financial news with AI-powered sentiment scoring.

What you can do:
- Read latest market news from Economic Times, Moneycontrol, and Google Finance RSS feeds
- See sentiment score for each article (Positive / Negative / Neutral) using TextBlob + VADER
- View sector-wise sentiment heatmap (which sectors are in positive/negative news)
- See trending topics extracted from headlines
- Filter news by sector or keyword

How sentiment works:
Each headline and summary is passed through both TextBlob (linguistic analysis) and VADER (financial-domain sentiment). The combined score determines the sentiment label and intensity.

Key files:
- `sections/08_news_sentiment/realtime_news_fetcher.py` — RSS feed aggregator
- `sections/08_news_sentiment/sentiment_analyzer.py` — TextBlob + VADER pipeline

---

### Section 9 — AI Investment Assistant

A conversational AI chatbot that answers investment questions using live market data.

What you can do:
- Ask anything: "What is the RSI of TCS?", "Compare HDFC Bank vs ICICI Bank", "Best SIP for 10 years?"
- Quick action buttons for common queries (no typing needed)
- The assistant fetches live data before answering, so responses are always current
- Full conversation history within the session

How it works:
1. Your question is sent to `GroqAIAnalyzer`
2. It fetches relevant live data (stock price, news, technicals) based on the question
3. The data + question are sent to Groq Llama 3.3 70B
4. The response is streamed back to the UI

Without a Groq API key, the assistant uses `enhanced_quick_actions.py` which provides rule-based answers with live data.

Key files:
- `sections/09_ai_assistant/groq_ai_analyzer.py` — Groq API integration
- `sections/09_ai_assistant/ai_investment_assistant.py` — chat UI
- `sections/09_ai_assistant/enhanced_quick_actions.py` — rule-based fallback

---

### Section 10 — Advanced Analytics

Macro-level market analysis tools for experienced investors.

What you can do:
- Sector Heatmap: See which sectors are up/down today with colour-coded intensity
- Correlation Matrix: See how correlated different stocks are (useful for diversification)
- Rolling Returns: Compare rolling 1M/3M/6M/1Y returns across stocks
- Volatility Analysis: See which stocks are most/least volatile
- Price Alerts: Set price targets and get notified when a stock crosses them

Key files:
- `sections/10_advanced_analytics/advanced_analytics_realtime.py` — main analytics engine
- `sections/10_advanced_analytics/advanced_analytics_alerts.py` — price alert system

---

## 6. How the Code is Organised

```
User opens browser
        |
        v
main_ultimate_final.py          <- Streamlit entry point
        |
        |-- Adds all sections/ and core/ to sys.path
        |-- Loads .env (GROQ_API_KEY etc.)
        |-- Sets up page config and dark theme CSS
        |-- Defines the 50+ stock universe (INDIAN_STOCKS dict)
        |-- Imports all section modules (with try/except fallbacks)
        |
        |-- Sidebar navigation -> user picks a section
        |
        |-- Section 1: Dashboard (inline in main)
        |-- Section 2: calls stock_analyzer.py
        |-- Section 3: calls realtime_mutual_fund_fetcher.py
        |-- Section 4: calls realtime_ipo_analyzer.py
        |-- Section 5: calls smart_money_live.py
        |-- Section 6: calls agentic_ai_hub.py
        |-- Section 7: calls portfolio_risk_manager.py
        |-- Section 8: calls realtime_news_fetcher.py
        |-- Section 9: calls groq_ai_analyzer.py
        `-- Section 10: calls advanced_analytics_realtime.py
```

**Caching strategy:** All data-fetching functions use `@st.cache_data` with TTL values:
- Stock prices: 5 minutes
- Mutual fund NAV: 30 minutes
- News: 10 minutes
- IPO data: 30 minutes

This means the app is fast on repeated interactions but always shows reasonably fresh data.

**Graceful degradation:** Every external module import is wrapped in `try/except`. If a module fails to import, the app still runs — it just shows a warning for that section instead of crashing.

---

## 7. Data Sources

| Data Type | Source | Update Frequency |
|---|---|---|
| Stock prices (50+ stocks) | Yahoo Finance via yfinance | Every 5 min (cached) |
| NIFTY 50 / SENSEX index | Yahoo Finance (^NSEI, ^BSESN) | Every 5 min |
| Mutual fund NAV (2400+ funds) | AMFI NAV file + mfapi.in | Daily (AMFI updates once/day) |
| IPO data + GMP | Chittorgarh, IPO Watch (scraped) | Every 30 min |
| FII/DII flows | NSE India website (scraped) | Daily |
| Financial news | Economic Times, Moneycontrol, Google Finance RSS | Every 10 min |
| AI responses | Groq API (Llama 3.3 70B) | On demand |

All data is fetched at runtime — there is no pre-downloaded static dataset (except the SQLite portfolio database which is user-generated).

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

**.env file (root folder) — for secrets:**
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free Groq API key at https://console.groq.com (no credit card needed).

**core/config.py — for everything else:**
- `STOCK_SYMBOLS` — the full 100+ stock universe with NSE ticker symbols
- `NEWS_SOURCES` — RSS feed URLs for news aggregation
- `DATABASE_PATH` — path to the SQLite database
- `TEAM_MEMBERS` — project team names
- `PREDICTION_DAYS` — forecast horizons (7, 30, 90 days)

You do not need to edit `config.py` to run the app. It works out of the box.

---

## 10. Database

The app uses a local SQLite database at `data/sarthak_nivesh.db`. It is created automatically on first run.

What gets stored:
- Your portfolio holdings (stock, buy price, quantity, date)
- Price alert settings
- Session history for the AI assistant

The database is managed by `sections/07_portfolio_risk/database_manager.py` using the `SarthakNiveshDB` class. All writes are auto-committed. The file is gitignored so your personal portfolio data is never pushed to GitHub.

---

## 11. Key Files Reference

| File | What it does |
|---|---|
| `main_ultimate_final.py` | Single entry point. Run this with `streamlit run`. |
| `core/config.py` | All constants: stock universe, API keys, paths, team info |
| `core/data_service.py` | Centralised data fetching layer used by multiple sections |
| `core/requirements.txt` | All Python dependencies with pinned versions |
| `sections/02_stock_intelligence/stock_analyzer.py` | Technical analysis engine (RSI, MACD, Bollinger Bands) |
| `sections/03_mutual_fund_sip/realtime_mutual_fund_fetcher.py` | Fetches 2400+ fund NAVs from AMFI |
| `sections/04_ipo_intelligence/realtime_ipo_analyzer.py` | Live IPO data + GMP scraper |
| `sections/05_smart_money_tracker/smart_money_live.py` | Live FII/DII flow tracker |
| `sections/06_agentic_ai_hub/agentic_ai_hub.py` | Multi-agent AI orchestrator |
| `sections/07_portfolio_risk/portfolio_risk_manager.py` | Portfolio P&L + risk metrics (Beta, Sharpe, VaR) |
| `sections/07_portfolio_risk/database_manager.py` | SQLite read/write for portfolio data |
| `sections/08_news_sentiment/realtime_news_fetcher.py` | RSS news aggregator |
| `sections/08_news_sentiment/sentiment_analyzer.py` | TextBlob + VADER sentiment pipeline |
| `sections/09_ai_assistant/groq_ai_analyzer.py` | Groq Llama 3.3 70B integration |
| `sections/10_advanced_analytics/advanced_analytics_realtime.py` | Sector heatmaps, correlation matrix |
| `data/sarthak_nivesh.db` | Local SQLite database (auto-created) |

---

## 12. Common Issues and Fixes

**App crashes on startup with ImportError**
All section imports are wrapped in try/except, so the app should not crash. If it does, run:
```bash
pip install -r core/requirements.txt
```

**NIFTY/SENSEX shows 0 or N/A**
Yahoo Finance occasionally rate-limits requests. The app has 4 fallback methods including calculating approximate index movement from top 5 stocks. Wait 1-2 minutes and refresh.

**Mutual funds show "No data"**
AMFI updates their NAV file once per day (usually after 8 PM IST). If you run the app before that, the previous day's NAV is shown. If the AMFI server is down, the section will show an error message.

**AI assistant gives generic answers**
Make sure your `GROQ_API_KEY` is set in the `.env` file. The key must start with `gsk_`. Without it, the assistant uses the rule-based fallback.

**Port 8501 already in use**
```bash
streamlit run main_ultimate_final.py --server.port 8502
```

**Slow first load**
The first load fetches live data from multiple sources simultaneously. Subsequent loads are fast because of Streamlit's `@st.cache_data` caching. Expect 15-30 seconds on first load.

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
