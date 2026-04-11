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
- Live IPO data with scoring — should you apply or avoid?
- FII/DII tracker — what are big institutions buying today?
- AI that explains your portfolio losses in plain Hindi or English
- SIP calculator that accounts for inflation and recommends real funds
- News with sentiment analysis — is the market mood positive or negative?

---

## Table of Contents

1. [Two Versions of the App](#1-two-versions-of-the-app)
2. [Who built it?](#2-who-built-it)
3. [Run the Streamlit App](#3-run-the-streamlit-app-option-a)
4. [Run the React Website](#4-run-the-react-website-option-b)
5. [Project Folder Structure](#5-project-folder-structure)
6. [All 12 Features Explained](#6-all-12-features-explained)
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
| Features | All 12 modules | All 12 modules |

Both use 100% real-time data. Neither has dummy or fake data.

---

## 2. Who built it?

This is a 6th Semester B.Tech project (2026).

| Name | Batch |
|---|---|
| Aman Jain | B.Tech 2023–27 |

GitHub: https://github.com/Amanarun2907/PRJ-3-6th-Semester-2026

---

## 3. Run the Streamlit App (Option A)

This is the simplest way to run the project. You only need Python.

### Step 1 — Download the project

```bash
git clone https://github.com/Amanarun2907/PRJ-3-6th-Semester-2026.git
cd PRJ-3-6th-Semester-2026
```

### Step 2 — Create a virtual environment

A virtual environment keeps this project's packages separate from your system Python.

```bash
python -m venv .venv
```

### Step 3 — Activate the virtual environment

```bash
# Windows
.venv\Scripts\activate

# Mac or Linux
source .venv/bin/activate
```

You will see `(.venv)` appear at the start of your terminal line. That means it worked.

### Step 4 — Install all required packages

```bash
pip install -r core/requirements.txt
```

This installs everything the project needs (Streamlit, yfinance, pandas, etc.). It takes 2-3 minutes.

### Step 5 — Add your Groq API key (free)

The AI features need a Groq API key. Get one free at https://console.groq.com (no credit card needed).

Open the `.env` file in the root folder and add your key:

```
GROQ_API_KEY=your_key_here
```

The app works without this key too — the AI assistant will use a rule-based fallback.

### Step 6 — Run the app

```bash
streamlit run main_ultimate_final.py
```

The app opens automatically at **http://localhost:8501**

---

## 4. Run the React Website (Option B)

The React website has two parts — a Python backend (FastAPI) and a React frontend. You need to run both at the same time in two separate terminals.

### Requirements

- Python 3.10 or higher
- Node.js 18 or higher (download from https://nodejs.org)

### Terminal 1 — Start the Backend

```bash
cd "C:\Users\YourName\path\to\PRJ-3\web\backend"
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

Wait until you see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Terminal 2 — Start the Frontend

Open a second terminal (keep Terminal 1 running):

```bash
cd "C:\Users\YourName\path\to\PRJ-3\web\frontend"
npm install
npm start
```

Wait until you see:
```
Compiled successfully!
Local: http://localhost:3000
```

### Open the website

Go to **http://localhost:3000** in your browser.

> Both terminals must stay open. If you close either one, the website stops working.

### What the warnings mean (safe to ignore)

When running `npm start` you may see these — they are NOT errors:
- `Failed to parse source map` — harmless plotly.js warning
- `Proxy error: Could not proxy /favicon.ico` — browser requesting an icon, not a real error
- `DeprecationWarning` — old webpack internal warning, does not affect the app

---

## 5. Project Folder Structure

```
PRJ-3-6th-Semester-2026/
|
|-- main_ultimate_final.py        <- Streamlit app entry point. Run this for Option A.
|-- .env                          <- Your API keys (never pushed to GitHub)
|-- README.md                     <- This file
|
|-- sections/                     <- All feature modules for Streamlit
|   |-- 02_stock_intelligence/    <- Stock charts, RSI, MACD, Bollinger Bands
|   |-- 03_mutual_fund_sip/       <- 2400+ live funds + SIP Goal Planner
|   |-- 04_ipo_intelligence/      <- Live IPO data + scoring
|   |-- 05_smart_money_tracker/   <- FII/DII from NSE API
|   |-- 06_agentic_ai_hub/        <- Multi-agent AI system
|   |-- 07_portfolio_risk/        <- Portfolio P&L + AI Finance Coach
|   |-- 08_news_sentiment/        <- Live news + sentiment analysis
|   |-- 09_ai_assistant/          <- Groq AI chat
|   `-- 10_advanced_analytics/    <- Sector heatmaps, correlation
|
|-- web/                          <- React website (Option B)
|   |-- backend/                  <- FastAPI Python server
|   |   |-- main.py               <- API entry point
|   |   |-- routers/              <- One file per feature module
|   |   `-- requirements.txt      <- Backend Python packages
|   `-- frontend/                 <- React app
|       |-- src/
|       |   |-- pages/            <- One page per module
|       |   |-- components/       <- Reusable UI components
|       |   `-- api.js            <- All API calls in one place
|       `-- package.json          <- Frontend packages
|
|-- core/                         <- Shared config and utilities
|   |-- config.py                 <- Stock universe, API keys, paths
|   `-- requirements.txt          <- Streamlit app Python packages
|
|-- data/                         <- SQLite database (auto-created)
|   `-- sarthak_nivesh.db         <- Your portfolio and goals are stored here
|
`-- exports/                      <- Excel/CSV exports land here
```

---

## 6. All 12 Features Explained

### 1. Live Market Dashboard
The home screen. Shows NIFTY 50 and SENSEX live prices, top 5 gainers, top 5 losers, and market breadth (how many stocks are up vs down today). All data is fetched live from Yahoo Finance every time you load the page.

### 2. Stock Intelligence
Pick any of 50+ NSE stocks and see:
- Candlestick price chart with MA20, MA50, MA200 lines
- RSI indicator (above 70 = overbought, below 30 = oversold)
- MACD chart (shows momentum direction)
- Bollinger Bands (shows price volatility)
- A BUY / HOLD / SELL signal based on all indicators combined
- Fundamental data: P/E ratio, market cap, 52-week high/low

### 3. Mutual Fund Center
Browse 2400+ real mutual funds fetched live from AMFI (India's official mutual fund body). See live NAV, 1-year and 3-year returns, expense ratio. Click any fund to see its NAV history chart for the past year.

### 4. SIP Goal Planner
Tell the planner your goal (child's education, home, retirement, etc.), how many years you have, and the inflation rate. It:
- Calculates how much more you'll need due to inflation
- Fetches real 3-year returns from live AMFI data
- Tells you exactly how much to invest per month for Conservative, Moderate, and Aggressive profiles
- Recommends the best real mutual funds for your profile
- Gets Groq AI to write a personalized financial plan for you
- Saves your goals to the database

### 5. IPO Intelligence Hub
Live IPO data scraped from ipowatch.in. Shows all Open, Upcoming, and Closed IPOs with:
- Price band, issue size, open/close dates
- A score from 0-100 based on issue size, category (Mainboard vs SME), subscription, and GMP
- APPLY / NEUTRAL / AVOID recommendation
- Charts: score distribution, status breakdown, category analysis

### 6. Smart Money Tracker
Tracks what Foreign Institutional Investors (FII) and Domestic Institutional Investors (DII) are doing. Data comes directly from NSE's official API. When FIIs are buying heavily, it usually means the market will go up. When they sell, it often signals a fall.

### 7. Portfolio & Risk Manager
Add your own stocks with buy price and quantity. The app fetches live prices and shows:
- Real-time profit/loss for each holding
- Portfolio allocation pie chart
- P&L bar charts
- Export to Excel

### 8. AI Finance Coach — Explain My Portfolio
This is the most unique feature. Click one button and the AI:
1. Reads your actual portfolio from the database
2. Fetches today's live price changes for every stock you hold
3. Gets FII/DII data from NSE
4. Reads live sector performance
5. Fetches today's market news
6. Sends all of it to Groq Llama 3.3 70B
7. Gets back a plain-language explanation: "Your portfolio is down 2.3% today mainly because HDFC Bank fell after RBI's rate decision. FIIs sold ₹2,800 Cr. This is temporary."
Works in Hindi and English.

### 9. News & Sentiment Analysis
Live financial news from Economic Times, Moneycontrol, and Google Finance RSS feeds. Each headline is scored for sentiment (Positive/Negative/Neutral) using TextBlob and VADER. Shows a sector-wise sentiment heatmap.

### 10. AI Investment Assistant
A chat interface powered by Groq Llama 3.3 70B. Ask anything about Indian stocks, mutual funds, IPOs, or investment strategy. Has quick-action buttons for common questions.

### 11. Advanced Analytics
- Sector heatmap: which sectors are up/down today
- Correlation matrix: how correlated are different stocks (useful for diversification)
- Volume intelligence: which stocks have unusual trading volume
- Market breadth gauge

### 12. Agentic AI Hub
A multi-agent AI system where specialised agents (Research, Analysis, Risk, Portfolio, News) collaborate to answer complex investment questions.

---

## 7. Data Sources

| What | Where it comes from | How often updated |
|---|---|---|
| Stock prices (50+ stocks) | Yahoo Finance | Every 5 minutes |
| NIFTY 50 / SENSEX | Yahoo Finance | Every 5 minutes |
| Mutual fund NAV (2400+) | AMFI official NAV file | Once daily (after 8 PM IST) |
| Mutual fund returns | mfapi.in (NAV history) | Live on request |
| IPO data | ipowatch.in | Live on request |
| FII/DII flows | NSE India official API | Daily |
| Financial news | ET, Moneycontrol, Google Finance RSS | Every 10 minutes |
| AI responses | Groq API (Llama 3.3 70B) | On demand |

**Important:** All data is fetched live at runtime. There is no pre-downloaded or fake data anywhere in this project.

---

## 8. Technology Stack

### Streamlit App (Option A)
| What | Technology |
|---|---|
| UI Framework | Streamlit |
| Charts | Plotly |
| Stock data | yfinance |
| Mutual fund data | AMFI NAV file + mfapi.in |
| AI | Groq API (Llama 3.3 70B) |
| Sentiment | TextBlob + VADER |
| Database | SQLite |
| Language | Python 3.10+ |

### React Website (Option B)
| What | Technology |
|---|---|
| Frontend | React 18 + Plotly.js |
| Backend | FastAPI (Python) |
| Styling | Custom CSS (dark glassmorphism) |
| Charts | Plotly.js (interactive) |
| API calls | Axios |
| Notifications | react-hot-toast |

---

## 9. API Keys Setup

The project needs one API key to unlock AI features. Everything else works without any key.

### Groq API Key (free)

1. Go to https://console.groq.com
2. Sign up (free, no credit card)
3. Create an API key
4. Open the `.env` file in the root folder
5. Add this line:

```
GROQ_API_KEY=your_key_here
```

The key starts with `gsk_`. Without it, the AI assistant uses a rule-based fallback and still works — just without the LLM responses.

### Where the .env file is

```
PRJ-3-6th-Semester-2026/
|-- .env          <- Edit this file
```

The `.env` file is in `.gitignore` so your key is never pushed to GitHub.

---

## 10. Database

The app automatically creates a SQLite database at `data/sarthak_nivesh.db` the first time you run it. You don't need to set anything up.

What gets saved:
- Your portfolio holdings (stocks you add in Portfolio Manager)
- Your SIP goals (goals you save in SIP Goal Planner)
- Price alert settings

The database file is gitignored — your personal data never goes to GitHub.

---

## 11. Common Problems and Fixes

**Problem: `npm start` gives "package.json not found"**
You are in the wrong folder. Run this first:
```bash
cd web/frontend
npm start
```

**Problem: `uvicorn main:app` gives "cannot import module main"**
You are in the wrong folder. Run this first:
```bash
cd web/backend
python -m uvicorn main:app --reload --port 8000
```

**Problem: Dashboard shows no data / empty charts**
The backend is not running. Make sure Terminal 1 (backend) is running before opening the website.

**Problem: NIFTY/SENSEX shows 0**
Yahoo Finance occasionally rate-limits requests. Wait 1-2 minutes and click Refresh.

**Problem: Mutual funds show "No data"**
AMFI updates their NAV file once per day after 8 PM IST. If you run before that, the previous day's data shows. If AMFI is down, you'll see an error.

**Problem: AI gives no response**
Check that your `GROQ_API_KEY` is in the `.env` file and starts with `gsk_`.

**Problem: Port 8501 already in use (Streamlit)**
```bash
streamlit run main_ultimate_final.py --server.port 8502
```

**Problem: Port 8000 already in use (FastAPI)**
```bash
python -m uvicorn main:app --reload --port 8001
```
Then update `web/frontend/src/api.js` line 3 to use port 8001.

**Problem: First load is very slow**
Normal. The first load fetches live data from multiple sources. After that, Streamlit's caching makes it fast. Expect 15-30 seconds on first load.

---

## 12. Disclaimer

This platform is built for **educational purposes** as part of a B.Tech academic project.

- Nothing on this platform is financial advice
- Stock prices, NAVs, and IPO data are fetched from public sources and may have delays
- Past returns shown for mutual funds do not guarantee future performance
- Always consult a SEBI-registered financial advisor before making investment decisions
- The developers are not responsible for any financial decisions made based on this platform

---

*Built with love for Indian retail investors. सार्थक निवेश — Invest Meaningfully.*

*Aman Jain · B.Tech 2023–27 · 6th Semester Project 2026*
