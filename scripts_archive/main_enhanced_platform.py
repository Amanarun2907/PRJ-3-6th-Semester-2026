# सार्थक निवेश - ENHANCED Investment Intelligence Platform
# ENHANCED VERSION: 50+ Stocks, 50+ Mutual Funds, Dark Theme, Real-time Dynamic Features
# Team: Aman Jain, Rohit Fogla, Vanshita Mehta, Disita Tirthani

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

# Import enhanced configuration
from config_enhanced import *

# Page Configuration
st.set_page_config(
    page_title="सार्थक निवेश - Enhanced Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PROFESSIONAL DARK THEME CSS - PERFECT VISIBILITY
st.markdown("""
<style>
    /* DARK PROFESSIONAL THEME */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        color: #ffffff !important;
    }
    
    /* ALL TEXT - WHITE AND BOLD */
    h1, h2, h3, h4, h5, h6, p, div, span, label, .stMarkdown, .stText {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* HEADERS - GRADIENT BACKGROUND */
    h1, h2, h3 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3) !important;
        margin: 1rem 0 !important;
        font-weight: 900 !important;
    }
    
    /* SIDEBAR - DARK WITH GRADIENT */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
        border-right: 3px solid #667eea !important;
    }
    
    .css-1d391kg *, [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    
    /* SELECTBOX & INPUTS - DARK WITH NEON BORDERS */
    .stSelectbox > div > div, .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #16213e !important;
        color: #ffffff !important;
        border: 2px solid #667eea !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }
    
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* BUTTONS - GRADIENT WITH GLOW */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        padding: 1rem 2rem !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* METRICS - DARK CARDS WITH GLOW */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%) !important;
        border: 2px solid #667eea !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3), 0 0 20px rgba(102, 126, 234, 0.2) !important;
    }
    
    [data-testid="metric-container"] * {
        color: #ffffff !important;
        font-weight: 900 !important;
    }
    
    /* CHARTS - DARK BACKGROUND */
    .js-plotly-plot, .plotly-graph-div {
        background-color: #16213e !important;
        border: 2px solid #667eea !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* DATAFRAMES - DARK WITH CONTRAST */
    .dataframe, .stDataFrame {
        background-color: #16213e !important;
        border: 2px solid #667eea !important;
        border-radius: 12px !important;
    }
    
    .dataframe th {
        background-color: #667eea !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        padding: 15px !important;
    }
    
    .dataframe td {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: 12px !important;
        border: 1px solid #667eea !important;
    }
    
    /* TABS - DARK THEME */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #16213e !important;
        border-bottom: 3px solid #667eea !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border: 2px solid #667eea !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 1rem 2rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        font-weight: 900 !important;
    }
    
    /* ALERTS - DARK WITH COLORS */
    .stSuccess {
        background-color: #10b981 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
    }
    
    .stInfo {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
    }
    
    .stWarning {
        background-color: #f59e0b !important;
        color: #000000 !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
    }
    
    .stError {
        background-color: #ef4444 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
    }
    
    /* EXPANDERS - DARK THEME */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%) !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        border: 2px solid #667eea !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    /* CUSTOM CARDS */
    .metric-card {
        background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
        border: 2px solid #667eea;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3), 0 0 20px rgba(102, 126, 234, 0.2);
    }
    
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    }
    
    /* SCROLLBAR - DARK */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Platform Header with Live Time
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🚀 सार्थक निवेश - Enhanced Platform")
        st.subheader("50+ Stocks | 50+ Mutual Funds | Real-time Intelligence")
    with col2:
        current_time = datetime.now().strftime("%d %b %Y, %I:%M %p")
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <h4>🕐 Live Time</h4>
            <p style="font-size: 1.1rem;">{current_time}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.title("🎯 Platform Modules")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Choose Module",
        [
            "🏠 Ultimate Dashboard",
            "📊 Real-time Stock Intelligence (50+ Stocks)", 
            "💰 Mutual Fund Center (50+ Funds)",
            "🚀 IPO Intelligence Hub",
            "🛡️ Risk Management & Portfolio",
            "📰 News & Sentiment Intelligence",
            "🤖 AI Investment Assistant",
            "📈 Advanced Market Analytics",
            "❓ Help & Documentation"
        ]
    )
    
    # Platform Stats in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Platform Stats")
    st.sidebar.metric("Total Stocks", len(STOCK_SYMBOLS))
    st.sidebar.metric("Total Mutual Funds", len(ALL_MUTUAL_FUNDS))
    st.sidebar.metric("Data Sources", len(NEWS_SOURCES))
    st.sidebar.metric("Update Frequency", "15 minutes")
    
    # Route to pages
    if page == "🏠 Ultimate Dashboard":
        show_ultimate_dashboard()
    elif "Stock Intelligence" in page:
        show_realtime_stock_intelligence()
    elif "Mutual Fund" in page:
        show_mutual_fund_center()
    elif "IPO Intelligence" in page:
        show_ipo_intelligence()
    elif "Risk Management" in page:
        show_risk_management()
    elif "News & Sentiment" in page:
        show_news_sentiment()
    elif "AI Investment" in page:
        show_ai_assistant()
    elif "Market Analytics" in page:
        show_market_analytics()
    elif "Help" in page:
        show_help_documentation()

def show_ultimate_dashboard():
    st.header("🏠 Ultimate Investment Intelligence Dashboard")
    
    # Real-time Market Status
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <h3>📊</h3>
            <h4>Stock Analysis</h4>
            <p>50+ Stocks</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <h3>💰</h3>
            <h4>Mutual Funds</h4>
            <p>50+ Funds</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <h3>🚀</h3>
            <h4>IPO Intel</h4>
            <p>Live Tracking</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <h3>📰</h3>
            <h4>News AI</h4>
            <p>Real-time</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <h3>🤖</h3>
            <h4>AI Assistant</h4>
            <p>24/7 Active</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Live Market Data
    st.subheader("📈 Live Market Intelligence")
    
    try:
        # Fetch NIFTY 50 data
        nifty = yf.Ticker("^NSEI")
        nifty_data = nifty.history(period="5d")
        
        if not nifty_data.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                nifty_current = nifty_data['Close'].iloc[-1]
                nifty_prev = nifty_data['Close'].iloc[-2] if len(nifty_data) > 1 else nifty_current
                nifty_change = ((nifty_current - nifty_prev) / nifty_prev) * 100
                st.metric("NIFTY 50", f"{nifty_current:.2f}", delta=f"{nifty_change:.2f}%")
            
            with col2:
                volatility = nifty_data['Close'].pct_change().std() * np.sqrt(252) * 100
                st.metric("Market Volatility", f"{volatility:.1f}%")
            
            with col3:
                sentiment = "🟢 Bullish" if nifty_change > 0 else "🔴 Bearish"
                st.metric("Market Sentiment", sentiment)
            
            with col4:
                volume = nifty_data['Volume'].iloc[-1]
                st.metric("Volume", f"{volume/1e6:.1f}M")
            
            # NIFTY Chart
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=nifty_data.index,
                open=nifty_data['Open'],
                high=nifty_data['High'],
                low=nifty_data['Low'],
                close=nifty_data['Close'],
                name="NIFTY 50"
            ))
            
            fig.update_layout(
                title="NIFTY 50 - Live Market Data",
                xaxis_title="Date",
                yaxis_title="Price",
                height=500,
                template="plotly_dark",
                plot_bgcolor='#16213e',
                paper_bgcolor='#16213e',
                font=dict(color='white', size=14, family='Arial Black')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.info("📊 Connecting to live market data...")
    
    # Top Gainers & Losers
    st.subheader("🔥 Top Movers Today")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🟢 Top Gainers")
        # Sample data - in production, fetch real-time
        gainers_data = {
            'Stock': ['Adani Green', 'Tata Motors', 'HDFC Bank', 'Reliance', 'TCS'],
            'Price': ['₹1,245', '₹892', '₹1,678', '₹2,456', '₹3,567'],
            'Change': ['+5.8%', '+4.2%', '+3.9%', '+3.5%', '+3.1%']
        }
        st.dataframe(pd.DataFrame(gainers_data), use_container_width=True)
    
    with col2:
        st.markdown("### 🔴 Top Losers")
        losers_data = {
            'Stock': ['Zee Entertainment', 'Biocon', 'Cipla', 'ITC', 'Wipro'],
            'Price': ['₹234', '₹456', '₹1,234', '₹456', '₹567'],
            'Change': ['-4.2%', '-3.8%', '-3.5%', '-2.9%', '-2.5%']
        }
        st.dataframe(pd.DataFrame(losers_data), use_container_width=True)

if __name__ == "__main__":
    main()
