# सार्थक निवेश — Sarthak Nivesh

### India's AI-Powered Real-Time Investment Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red?logo=streamlit)](https://streamlit.io/)
[![React](https://img.shields.io/badge/React-18%2B-61dafb?logo=react)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Groq AI](https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange)](https://console.groq.com/)
[![NSE/BSE](https://img.shields.io/badge/Data-NSE%20%7C%20BSE%20%7C%20AMFI-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

> **सार्थक निवेश** (meaning *Meaningful Investment*) is a complete, real-time investment intelligence platform for Indian retail investors. It comes in two versions — a Streamlit app and a full-stack React website — both powered by live data from NSE, BSE, AMFI, and Yahoo Finance. Zero dummy data. Everything is live.

---

## What does this project do? (Simple explanation)

Imagine you are a regular person who wants to invest in stocks or mutual funds in India. You don't know where to start. You don't understand why your portfolio went down today. You don't know how much to save every month to buy a house in 10 years.

This platform solves all of that — for free.

It gives you the same tools that professional investors use:
- Live stock prices and charts for 50+ NSE stocks
- 2400+ mutual fund NAVs updated daily from AMFI
- Live IPO data with scoring, financials, peer comparison, and AI exit strategy
- FII/DII tracker — what are big institutions buying today?
- AI Finance Coach that explains your portfolio losses in plain Hindi or English
- SIP Goal Planner with inflation-adjusted targets and live fund recommendations
- Agentic AI Hub — 6 specialist AI agents that collaborate to give a complete investment report
- News with sentiment analysis — is the market mood positive or negative?

---

## Table of Contents

1. [Two Versions of the App](#1-two-versions-of-the-app)
2. [Who built it?](#2-who-built-it)
3. [Run the Streamlit App](#3-run-the-streamlit-app-option-a)
4. [Run the React Website](#4-run-the-react-website-option-b)
5. [Project Folder Structure](#5-project-folder-structure)
6. [All 13 Features Explained](#6-all-13-features-explained)
7. [Data Sources](#7-data-sources)
8. [Technology Stack](#8-technology-stack)
9. [API Keys Setup](#9-api-keys-setup)
10. [Database](#10-database)
11. [Common Problems and Fixes](#11-common-problems-and-fixes)
12. [Disclaimer](#12-disclaimer)

---

## 1. Two Versions of the App

This project has **two separate interfaces** that share the same data and logic:

| | Streamlit App | React Website |
|---|---|---|
| What it is | Python web app | Full-stack website |
| How to run | `streamlit run main_ultimate_final.py` | Backend + Frontend separately |
| Best for | Quick use, development | Hackathon demo, public sharing |
| Port | 8501 | Frontend: 3000, Backend: 8000 |
| Features | All 13 modules | All 13 modules |

Both use 100% real-time data. Neither has dummy or fake data anywhere.

---

## 2. Who built it?

This is a 6th Semester B.Tech project (2026).

| Name | Batch |
|---|---|
| Aman Jain | B.Tech 2023–27 |

GitHub: https://github.com/Amanarun2907/PRJ-3-6th-Semester-2026

---

## 3. Run the Streamlit App (Option A)

This is the simplest way. You only need Python.

### Step 1 — Download the project

```bash
git clone https://github.com/Amanarun2907/PRJ-3-6th-Semester-2026.git
cd PRJ-3-6th-Semester-2026
```

### Step 2 — Create and activate virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### Step 3 — Install packages

```bash
pip install -r core/requirements.txt
```

### Step 4 — Add your Groq API key

Open the `.env` file and add:
```
GROQ_API_KEY=your_key_here
```
Get a free key at https://console.groq.com (no credit card needed).

### Step 5 — Run

```bash
streamlit run main_ultimate_final.py
```

Opens at **http://localhost:8501**

---

## 4. Run the React Website (Option B)

You need Python and Node.js (https://nodejs.org).

### Terminal 1 — Backend

```bash
cd web/backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

Wait for: `Application startup complete.`

### Terminal 2 — Frontend

```bash
cd web/frontend
npm install
npm start
```

Wait for: `Compiled successfully!`

### Open browser

Go to **http://localhost:3000**

Both terminals must stay open. The backend runs on port 8000, frontend on port 3000.

> The warnings you see (`Failed to parse source map`, `Proxy error: favicon.ico`) are harmless. They do not affect the app.

---

## 5. Project Folder Structure

```
PRJ-3-6th-Semester-2026/
|
|-- main_ultimate_final.py        <- Streamlit app. Run this for Option A.
|-- .env                          <- Your API keys (never pushed to GitHub)
|-- README.md
|
|-- sections/                     <- Streamlit feature modules
|   |-- 02_stock_intelligence/
|   |-- 03_mutual_fund_sip/
|   |   |-- sip_goal_planner.py   <- SIP Goal Planner with live AMFI data
|   |-- 04_ipo_intelligence/
|   |-- 05_smart_money_tracker/
|   |-- 06_agentic_ai_hub/
|   |-- 07_portfolio_risk/
|   |   |-- explain_my_loss.py    <- AI Finance Coach
|   |-- 08_news_sentiment/
|   |-- 09_ai_assistant/
|   `-- 10_advanced_analytics/
|
|-- web/                          <- React website (Option B)
|   |-- backend/                  <- FastAPI Python server
|   |   |-- main.py               <- API entry point
|   |   |-- routers/
|   |   |   |-- dashboard.py      <- NIFTY, SENSEX, gainers, losers
|   |   |   |-- stocks.py         <- OHLCV, technicals, fundamentals
|   |   |   |-- mutual_funds.py   <- Live AMFI NAV + mfapi.in returns
|   |   |   |-- sip_goals.py      <- SIP calculator + AI advice
|   |   |   |-- ipo.py            <- Live IPO data + AI exit strategy
|   |   |   |-- smart_money.py    <- FII/DII from NSE API
|   |   |   |-- portfolio.py      <- Portfolio P&L + risk metrics
|   |   |   |-- news.py           <- RSS feeds + VADER sentiment
|   |   |   |-- ai_assistant.py   <- Groq chat + AI Finance Coach
|   |   |   |-- analytics.py      <- Sector heatmap, correlation, breadth
|   |   |   `-- agentic.py        <- 6 specialist agents + master report
|   |   `-- requirements.txt
|   `-- frontend/                 <- React app
|       |-- src/
|       |   |-- pages/            <- One page per module (13 pages)
|       |   |-- components/       <- Sidebar, PlotlyChart
|       |   `-- api.js            <- All API calls
|       `-- package.json
|
|-- core/                         <- Shared config
|   |-- config.py
|   `-- requirements.txt          <- Streamlit app packages
|
|-- data/                         <- SQLite database (auto-created)
|   `-- sarthak_nivesh.db
|
`-- exports/                      <- Excel/CSV exports
```

---

## 6. All 13 Features Explained

### 1. Live Market Dashboard
The home screen. Shows NIFTY 50 and SENSEX live prices with point change, top 5 gainers, top 5 losers, and market breadth (how many stocks are up vs down). All data is live from Yahoo Finance.

### 2. Stock Intelligence
Pick any of 50+ NSE stocks and see:
- Candlestick chart with MA20, MA50, MA200 overlaid
- RSI (overbought/oversold zones highlighted)
- MACD with histogram
- Bollinger Bands
- BUY / HOLD / SELL signal from combined indicators
- Fundamental data: P/E, market cap, 52-week high/low, dividend yield

### 3. Mutual Fund Center
Browse 2400+ real mutual funds from AMFI. See live NAV, 1Y/3Y returns, expense ratio. Click any fund to see its 1-year NAV history chart.

### 4. SIP Goal Planner
The most practical feature for common investors. You tell it:
- Your goal (child's education, home, retirement, etc.)
- How many years you have
- Inflation rate

It calculates how much more you'll need due to inflation, fetches real 3-year returns from live AMFI data, tells you exactly how much to invest monthly for Conservative/Moderate/Aggressive profiles, recommends the best real mutual funds, and gets Groq AI to write a personalised financial plan. Saves goals to the database.

### 5. IPO Intelligence Hub
The most advanced IPO analysis tool available for free. For every IPO it shows:
- Live data from ipowatch.in (Open/Upcoming/Closed status)
- IPO score 0-100 based on issue size, category, subscription, GMP, financials
- APPLY / NEUTRAL / AVOID recommendation
- Click any IPO card to open a full analysis modal with:
  - Financial KPIs: ROE, ROCE, EBITDA Margin, PAT Margin, Debt/Equity, EPS, P/E, RoNW, NAV
  - Revenue and PAT history (3-4 years)
  - Peer comparison table
  - Promoter holding pre and post issue
  - Use of IPO proceeds
  - Investor allocation (QIB/NII/Retail %)
  - IPO Quality Radar chart
  - **AI Exit Strategy** — Groq AI tells you: should you apply, sell on listing day or hold, what % gain to target on listing, 30/60/90 day price targets, recommended split (e.g. sell 50% on listing, hold 50% for 90 days), and stop loss level

### 6. Smart Money Tracker
Tracks what Foreign Institutional Investors (FII) and Domestic Institutional Investors (DII) are doing. Data comes directly from NSE's official API. Shows FII/DII net flows, bulk deals, block deals, and sector-wise money flow.

### 7. Portfolio & Risk Manager
Add your own stocks with buy price and quantity. The app fetches live prices and shows real-time P&L, portfolio allocation pie chart, and P&L bar charts.

### 8. AI Finance Coach — Explain My Portfolio
The most emotionally intelligent feature. Click one button and the AI:
1. Reads your actual portfolio from the database
2. Fetches today's live price changes for every stock
3. Gets FII/DII data from NSE
4. Reads live sector performance
5. Fetches today's market news
6. Sends all of it to Groq Llama 3.3 70B
7. Returns a plain-language explanation in Hindi or English: "Your portfolio is down 2.3% today mainly because HDFC Bank fell after RBI's rate decision. FIIs sold ₹2,800 Cr. This is temporary."

### 9. Agentic AI Investment Hub
The most powerful feature. 6 specialist AI agents run simultaneously, each fetching live data from their domain, then a Master Agent synthesises everything into a complete investment report.

**The 6 agents:**
- Stock Intelligence Agent — live prices, RSI, MACD, BUY/SELL signals for 20 stocks
- Market Analysis Agent — NIFTY, SENSEX, 8-sector performance
- Smart Money Agent — live FII/DII flows from NSE API
- News & Sentiment Agent — live RSS headlines + VADER sentiment scoring
- Risk Management Agent — volatility, VaR(95%), correlation matrix
- Advanced Analytics Agent — volume anomalies, sector rotation, momentum

**The Master Report includes:**
- Executive Summary
- Top 3 Investment Opportunities with reasoning
- Key Risks to Watch
- Smart Money Signal interpretation
- Recommended Action Plan (3 concrete steps)
- Confidence Level

**Sample queries to try:**
- "Analyse the current Indian stock market and tell me where to invest today"
- "Which stocks should I buy this week based on technicals and FII activity?"
- "Give me a complete weekly market intelligence report with top 3 recommendations"

### 10. News & Sentiment Analysis
Live financial news from Economic Times, Moneycontrol, and Google Finance RSS. Each headline is scored for sentiment using TextBlob and VADER. Shows a sector-wise sentiment heatmap and sentiment timeline chart.

### 11. AI Investment Assistant
A chat interface powered by Groq Llama 3.3 70B. Ask anything about Indian stocks, mutual funds, IPOs, or investment strategy. Has 10 quick-action buttons for common questions.

### 12. Advanced Analytics
- Sector heatmap: which sectors are up/down today
- Correlation matrix: how correlated are different stocks
- Volume intelligence: unusual volume activity detection
- Market breadth gauge with A/D ratio

### 13. Agentic AI Hub (Streamlit version)
The Streamlit version also has a multi-agent AI system in `sections/06_agentic_ai_hub/` that works similarly to the React version.

---

## 7. Data Sources

| What | Where it comes from | How often |
|---|---|---|
| Stock prices (50+ stocks) | Yahoo Finance (yfinance) | Every 5 min |
| NIFTY 50 / SENSEX | Yahoo Finance (`^NSEI`, `^BSESN`) | Every 5 min |
| Mutual fund NAV (2400+) | AMFI official NAV file | Daily after 8 PM IST |
| Mutual fund returns | mfapi.in (NAV history) | Live on request |
| IPO data + details | ipowatch.in (scraped) | Live on request |
| FII/DII flows | NSE India official API | Daily |
| Bulk/Block deals | NSE India official API | Daily |
| Financial news | ET, Moneycontrol, Google Finance RSS | Every 10 min |
| AI responses | Groq API (Llama 3.3 70B) | On demand |
| Portfolio data | User's local SQLite DB | Real-time |

**Zero dummy data.** Everything is fetched live at runtime.

---

## 8. Technology Stack

### Streamlit App
| Layer | Technology |
|---|---|
| UI | Streamlit |
| Charts | Plotly |
| Stock data | yfinance |
| Mutual fund data | AMFI NAV file + mfapi.in |
| AI | Groq API (Llama 3.3 70B) |
| Sentiment | TextBlob + VADER |
| Database | SQLite |
| Language | Python 3.10+ |

### React Website
| Layer | Technology |
|---|---|
| Frontend | React 18 |
| Charts | Plotly.js (interactive) |
| Backend | FastAPI (Python) |
| Styling | Custom CSS (dark glassmorphism) |
| API calls | Axios |
| Notifications | react-hot-toast |
| Web scraping | BeautifulSoup4 |

---

## 9. API Keys Setup

Only one key is needed. Everything else works without any key.

### Groq API Key (free, no credit card)

1. Go to https://console.groq.com
2. Sign up and create an API key
3. Open the `.env` file in the root folder
4. Add this line:

```
GROQ_API_KEY=gsk_your_key_here
```

Without this key:
- AI Finance Coach uses rule-based fallback
- IPO AI analysis shows "API key not configured"
- Agentic AI Hub shows placeholder text
- SIP AI advice is skipped

---

## 10. Database

The app automatically creates `data/sarthak_nivesh.db` on first run.

| Table | What it stores |
|---|---|
| `portfolio_holdings` | Your stocks (symbol, buy price, quantity, date, sector) |
| `sip_goals` | Your SIP goals (target, years, inflation, monthly SIP, risk profile) |
| `stock_data` | Historical price snapshots |
| `sector_performance` | Sector % change history |
| `news_sentiment` | News articles with sentiment scores |
| `market_breadth` | Daily advancing/declining counts |

The database file is gitignored — your personal data never goes to GitHub.

---

## 11. Common Problems and Fixes

**`npm start` gives "package.json not found"**
You are in the wrong folder. Run:
```bash
cd web/frontend
npm start
```

**`uvicorn main:app` gives "cannot import module main"**
You are in the wrong folder. Run:
```bash
cd web/backend
python -m uvicorn main:app --reload --port 8000
```

**Dashboard shows no data / empty charts**
The backend is not running. Start Terminal 1 (backend) first, then open the website.

**IPO modal shows all N/A**
This is fixed in the latest version. Pull the latest code:
```bash
git pull origin master
```

**NIFTY/SENSEX shows 0**
Yahoo Finance rate-limits occasionally. Wait 1-2 minutes and click Refresh.

**Mutual funds show "No data"**
AMFI updates their NAV file once per day after 8 PM IST. If AMFI is temporarily down, you'll see an error.

**AI gives no response**
Check that `GROQ_API_KEY` is in the `.env` file and starts with `gsk_`.

**Agentic AI Hub takes too long**
It runs 6 agents + 7 Groq API calls. This takes 60-120 seconds. This is normal — it's doing real work.

**Port already in use**
```bash
# Streamlit
streamlit run main_ultimate_final.py --server.port 8502

# FastAPI
python -m uvicorn main:app --reload --port 8001
```

---

## 12. Disclaimer

This platform is built for **educational purposes** as part of a B.Tech academic project.

- Nothing on this platform is financial advice
- Stock prices, NAVs, and IPO data are fetched from public sources and may have delays
- Past returns shown for mutual funds do not guarantee future performance
- The IPO AI exit strategy is for educational purposes only — actual returns depend on market conditions
- Always consult a SEBI-registered financial advisor before making investment decisions
- The developers are not responsible for any financial decisions made based on this platform

---

*Built with love for Indian retail investors. सार्थक निवेश — Invest Meaningfully.*

*Aman Jain · B.Tech 2023–27 · 6th Semester Project 2026*
