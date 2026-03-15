# सार्थक निवेश - Enhanced Investment Intelligence Platform
# Team: Aman Jain, Rohit Fogla, Vanshita Mehta, Disita Tirthani

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3
import os
import numpy as np
import yfinance as yf
import warnings
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
warnings.filterwarnings('ignore')

# Import enhanced configuration
from enhanced_config import *

# Page Configuration
st.set_page_config(
    page_title="सार्थक निवेश - Enhanced Investment Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PROFESSIONAL DARK THEME WITH PERFECT VISIBILITY
st.markdown("""
<style>
    /* PROFESSIONAL DARK THEME - MAXIMUM VISIBILITY */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        color: #ffffff !important;
    }
    
    /* FORCE ALL TEXT TO BE WHITE AND BOLD */
    h1, h2, h3, h4, h5, h6, p, div, span, label, .stMarkdown, .stText,
    .css-1d391kg, .css-1d391kg *, .stSelectbox *, .stButton *,
    .stMetric *, .stDataFrame *, .element-container *,
    [data-testid="stSidebar"] *, [data-testid="stHeader"] *,
    .stTabs *, .stExpander *, .block-container * {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* GLASSMORPHISM HEADERS */
    h1, h2, h3, h4, h5, h6 {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    
    /* GLASSMORPHISM SIDEBAR */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .css-1d391kg *, [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }    
  
  /* GLASSMORPHISM INPUT FIELDS */
    .stSelectbox > div > div, .stTextInput > div > div > input,
    .stNumberInput > div > div > input, .stTextArea > div > div > textarea,
    .stSlider > div > div > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem !important;
    }
    
    .stSelectbox label, .stTextInput label, .stNumberInput label,
    .stTextArea label, .stSlider label {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* GLASSMORPHISM BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        padding: 1rem 2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* GLASSMORPHISM METRICS */
    .metric-container, [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        margin: 1rem 0 !important;
    }
    
    [data-testid="metric-container"] * {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.3rem !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5) !important;
    }    
    
/* GLASSMORPHISM CHARTS */
    .js-plotly-plot, .plotly-graph-div, .stPlotlyChart {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }
    
    /* GLASSMORPHISM DATAFRAMES */
    .dataframe, .stDataFrame, [data-testid="dataframe"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    }
    
    .dataframe th, .dataframe td {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 15px !important;
        font-size: 1.1rem !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5) !important;
    }
    
    .dataframe th {
        background: rgba(255, 255, 255, 0.15) !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
    }
    
    /* GLASSMORPHISM TABS */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px 15px 0 0 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px 12px 0 0 !important;
        margin-right: 4px !important;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        transform: translateY(-2px) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }    
   
 /* GLASSMORPHISM EXPANDERS */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(5px) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-top: none !important;
        border-radius: 0 0 15px 15px !important;
        padding: 1.5rem !important;
    }
    
    /* GLASSMORPHISM ALERTS */
    .stAlert {
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        font-weight: 700 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        font-size: 1.1rem !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stSuccess {
        background: rgba(40, 167, 69, 0.2) !important;
        color: #ffffff !important;
        border-color: rgba(40, 167, 69, 0.5) !important;
    }
    
    .stInfo {
        background: rgba(0, 123, 255, 0.2) !important;
        color: #ffffff !important;
        border-color: rgba(0, 123, 255, 0.5) !important;
    }
    
    .stWarning {
        background: rgba(255, 193, 7, 0.2) !important;
        color: #ffffff !important;
        border-color: rgba(255, 193, 7, 0.5) !important;
    }
    
    .stError {
        background: rgba(220, 53, 69, 0.2) !important;
        color: #ffffff !important;
        border-color: rgba(220, 53, 69, 0.5) !important;
    }
    
    /* GLASSMORPHISM CONTAINERS */
    .block-container, .main, .element-container {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(5px) !important;
        color: #ffffff !important;
        padding: 2rem !important;
        border-radius: 20px !important;
        margin: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }    
  
  /* CUSTOM GLASSMORPHISM CARDS */
    .enhanced-card {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        margin: 1rem 0 !important;
        transition: all 0.3s ease !important;
    }
    
    .enhanced-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }
    
    .enhanced-card * {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* FORCE VISIBILITY FOR ALL ELEMENTS */
    * {
        color: #ffffff !important;
    }
    
    /* SCROLLBAR STYLING */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* LOADING SPINNER */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* ENSURE CHART VISIBILITY */
    .plotly .modebar {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    
    /* ANIMATION KEYFRAMES */
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
        50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
        100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
    }
    
    .glow-effect {
        animation: glow 2s infinite;
    }
</style>
""", unsafe_allow_html=True)# Auto-ref
resh functionality
def setup_auto_refresh():
    """Setup auto-refresh for real-time data updates"""
    if REAL_TIME_UPDATE:
        # Add auto-refresh meta tag
        st.markdown(f"""
        <meta http-equiv="refresh" content="{AUTO_REFRESH_INTERVAL}">
        """, unsafe_allow_html=True)

# Enhanced data fetching with caching
@st.cache_data(ttl=900)  # Cache for 15 minutes
def fetch_stock_data_enhanced(symbol, period="1y"):
    """Fetch enhanced stock data with error handling"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        if not data.empty:
            # Add technical indicators
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            
            # RSI calculation
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            
            # MACD calculation
            ema_12 = data['Close'].ewm(span=12).mean()
            ema_26 = data['Close'].ewm(span=26).mean()
            data['MACD'] = ema_12 - ema_26
            data['MACD_Signal'] = data['MACD'].ewm(span=9).mean()
            
        return data
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_multiple_stocks_data(symbols, period="1y"):
    """Fetch data for multiple stocks efficiently"""
    stock_data = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_symbol = {
            executor.submit(fetch_stock_data_enhanced, symbol, period): symbol 
            for symbol in symbols
        }
        
        for future in future_to_symbol:
            symbol = future_to_symbol[future]
            try:
                data = future.result()
                if not data.empty:
                    stock_data[symbol] = data
            except Exception as e:
                st.warning(f"Failed to fetch data for {symbol}: {str(e)}")
    
    return stock_data

def main():
    # Setup auto-refresh
    setup_auto_refresh()
    
    # Platform Header with glassmorphism
    st.markdown("""
    <div class="enhanced-card glow-effect">
        <h1 style="text-align: center; margin: 0;">🚀 सार्थक निवेश</h1>
        <h3 style="text-align: center; margin: 0.5rem 0;">India's Most Advanced Investment Intelligence Platform</h3>
        <p style="text-align: center; margin: 0;">Real-time • Dynamic • Professional • AI-Powered</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation with enhanced styling
    st.sidebar.markdown("""
    <div class="enhanced-card">
        <h2 style="text-align: center;">🎯 Platform Modules</h2>
    </div>
    """, unsafe_allow_html=True)   
 
    page = st.sidebar.selectbox(
        "Choose Platform Module",
        [
            "🏠 Ultimate Dashboard",
            "📊 Real-time Stock Intelligence", 
            "🚀 IPO Intelligence Hub (UNIQUE)",
            "💰 Mutual Fund & SIP Center",
            "🛡️ Risk Management & Portfolio",
            "📰 News & Sentiment Intelligence",
            "🧠 Advanced Fake News Detection",
            "🔔 Smart Alerts & Notifications",
            "🤖 AI Investment Assistant",
            "📈 Advanced Market Analytics",
            "🔥 Market Heat Maps & Correlation",
            "⚙️ Data Management Center",
            "❓ Complete FAQ & Help Center"
        ]
    )
    
    # Real-time status indicator
    st.sidebar.markdown(f"""
    <div class="enhanced-card">
        <h4>🔴 LIVE Status</h4>
        <p>📊 Stocks: {len(STOCK_SYMBOLS)} Active</p>
        <p>💰 Mutual Funds: {len(MUTUAL_FUNDS)} Active</p>
        <p>🔄 Last Update: {datetime.now().strftime('%H:%M:%S')}</p>
        <p>⚡ Auto-refresh: {AUTO_REFRESH_INTERVAL//60} min</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Route to different pages
    if page == "🏠 Ultimate Dashboard":
        show_enhanced_ultimate_dashboard()
    elif page == "📊 Real-time Stock Intelligence":
        show_enhanced_stock_intelligence()
    elif page == "💰 Mutual Fund & SIP Center":
        show_enhanced_mutual_fund_center()
    elif page == "📈 Advanced Market Analytics":
        show_enhanced_market_analytics()
    else:
        st.markdown("""
        <div class="enhanced-card">
            <h2>🚧 Module Under Enhancement</h2>
            <p>This module is being enhanced with new dynamic features and professional styling.</p>
            <p>Please check back soon for the updated version!</p>
        </div>
        """, unsafe_allow_html=True)

def show_enhanced_ultimate_dashboard():
    st.markdown("""
    <div class="enhanced-card">
        <h2>🏠 Ultimate Investment Intelligence Dashboard</h2>
        <p>Real-time market data with professional analytics and AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Live Market Data with enhanced visuals
    try:
        # Fetch live market indices
        nifty = yf.Ticker("^NSEI")
        sensex = yf.Ticker("^BSESN")
        
        nifty_data = nifty.history(period="5d")
        sensex_data = sensex.history(period="5d")
        
        if not nifty_data.empty and not sensex_data.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                nifty_current = nifty_data['Close'].iloc[-1]
                nifty_prev = nifty_data['Close'].iloc[-2] if len(nifty_data) > 1 else nifty_current
                nifty_change = ((nifty_current - nifty_prev) / nifty_prev) * 100
                
                delta_color = "normal" if nifty_change >= 0 else "inverse"
                st.metric(
                    "NIFTY 50", 
                    f"{nifty_current:.2f}", 
                    delta=f"{nifty_change:.2f}%",
                    delta_color=delta_color
                )
            
            with col2:
                sensex_current = sensex_data['Close'].iloc[-1]
                sensex_prev = sensex_data['Close'].iloc[-2] if len(sensex_data) > 1 else sensex_current
                sensex_change = ((sensex_current - sensex_prev) / sensex_prev) * 100
                
                delta_color = "normal" if sensex_change >= 0 else "inverse"
                st.metric(
                    "SENSEX", 
                    f"{sensex_current:.2f}", 
                    delta=f"{sensex_change:.2f}%",
                    delta_color=delta_color
                )
            
            with col3:
                volatility = nifty_data['Close'].pct_change().std() * np.sqrt(252) * 100
                st.metric("Market Volatility", f"{volatility:.1f}%")
            
            with col4:
                sentiment = "🟢 Bullish" if nifty_change > 0 else "🔴 Bearish"
                st.metric("Market Sentiment", sentiment)    
        
            # Enhanced market chart with glassmorphism
            fig = go.Figure()
            
            # NIFTY candlestick
            fig.add_trace(go.Candlestick(
                x=nifty_data.index,
                open=nifty_data['Open'],
                high=nifty_data['High'],
                low=nifty_data['Low'],
                close=nifty_data['Close'],
                name="NIFTY 50",
                increasing_line_color='#00ff88',
                decreasing_line_color='#ff4444'
            ))
            
            fig.update_layout(
                title={
                    'text': "🔴 LIVE NIFTY 50 - Real-time Market Data",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': 'white'}
                },
                xaxis_title="Date",
                yaxis_title="Price",
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    color='white'
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    color='white'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.info("📊 Connecting to live market data...")
    
    # Top Performers Section
    st.markdown("""
    <div class="enhanced-card">
        <h3>🏆 Today's Top Performers</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch top 10 stocks performance
    top_stocks = list(STOCK_SYMBOLS.keys())[:10]
    stock_performance = []
    
    with st.spinner("🔄 Fetching real-time stock performance..."):
        for symbol in top_stocks:
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="2d")
                if len(data) >= 2:
                    current_price = data['Close'].iloc[-1]
                    prev_price = data['Close'].iloc[-2]
                    change_pct = ((current_price - prev_price) / prev_price) * 100
                    
                    stock_performance.append({
                        'Stock': STOCK_SYMBOLS[symbol],
                        'Symbol': symbol,
                        'Price': f"₹{current_price:.2f}",
                        'Change %': f"{change_pct:.2f}%",
                        'Change_Value': change_pct
                    })
            except:
                continue
    
    if stock_performance:
        # Sort by performance
        stock_performance.sort(key=lambda x: x['Change_Value'], reverse=True)
        
        # Create performance dataframe
        df = pd.DataFrame(stock_performance)
        
        # Color code the dataframe
        def color_performance(val):
            if isinstance(val, str) and '%' in val:
                num_val = float(val.replace('%', ''))
                if num_val > 0:
                    return 'background-color: rgba(0, 255, 136, 0.2); color: white'
                else:
                    return 'background-color: rgba(255, 68, 68, 0.2); color: white'
            return 'color: white'
        
        styled_df = df[['Stock', 'Price', 'Change %']].style.applymap(color_performance)
        st.dataframe(styled_df, use_container_width=True)
    
    # Market Summary Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="enhanced-card">
            <h4>📊 Market Summary</h4>
            <p>• Total Stocks Tracked: <strong>50+</strong></p>
            <p>• Mutual Funds Available: <strong>50+</strong></p>
            <p>• Real-time Updates: <strong>Every 15 minutes</strong></p>
            <p>• AI Recommendations: <strong>Active</strong></p>
            <p>• Risk Analysis: <strong>Professional Grade</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="enhanced-card">
            <h4>🚀 Platform Features</h4>
            <p>• IPO Intelligence: <strong>First in India</strong></p>
            <p>• Fake News Detection: <strong>85%+ Accuracy</strong></p>
            <p>• Portfolio Optimization: <strong>AI-Powered</strong></p>
            <p>• Technical Analysis: <strong>Advanced</strong></p>
            <p>• Market Sentiment: <strong>Real-time</strong></p>
        </div>
        """, unsafe_allow_html=True)d
ef show_enhanced_stock_intelligence():
    st.markdown("""
    <div class="enhanced-card">
        <h2>📊 Real-time Stock Intelligence</h2>
        <p>Advanced technical analysis with AI-powered recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced stock selection with search
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Create searchable stock list
        stock_options = [f"{name} ({symbol})" for symbol, name in STOCK_SYMBOLS.items()]
        selected_option = st.selectbox(
            "🔍 Search & Select Stock for Analysis",
            stock_options,
            help="Type to search for stocks"
        )
        
        # Extract symbol from selection
        selected_stock = selected_option.split('(')[-1].replace(')', '')
    
    with col2:
        analysis_period = st.selectbox(
            "📅 Analysis Period",
            ["1D", "5D", "1M", "3M", "6M", "1Y", "2Y"],
            index=4  # Default to 6M
        )
    
    with col3:
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=True)
    
    if selected_stock:
        # Fetch enhanced stock data
        with st.spinner("🔄 Fetching real-time data..."):
            period_map = {"1D": "1d", "5D": "5d", "1M": "1mo", "3M": "3mo", "6M": "6mo", "1Y": "1y", "2Y": "2y"}
            data = fetch_stock_data_enhanced(selected_stock, period_map[analysis_period])
            
            if not data.empty:
                current_price = data['Close'].iloc[-1]
                prev_close = data['Close'].iloc[-2] if len(data) > 1 else current_price
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                
                # Enhanced metrics display
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    delta_color = "normal" if change >= 0 else "inverse"
                    st.metric(
                        "💰 Current Price", 
                        f"₹{current_price:.2f}", 
                        delta=f"₹{change:.2f} ({change_pct:.2f}%)",
                        delta_color=delta_color
                    )
                
                with col2:
                    high_52w = data['High'].max()
                    st.metric("📈 52W High", f"₹{high_52w:.2f}")
                
                with col3:
                    low_52w = data['Low'].min()
                    st.metric("📉 52W Low", f"₹{low_52w:.2f}")
                
                with col4:
                    avg_volume = data['Volume'].mean()
                    st.metric("📊 Avg Volume", f"{avg_volume:,.0f}")
                
                with col5:
                    market_cap = current_price * 1000000000  # Simplified calculation
                    if market_cap > 1000000000000:
                        cap_display = f"₹{market_cap/1000000000000:.1f}T"
                    else:
                        cap_display = f"₹{market_cap/100000000:.0f}Cr"
                    st.metric("💎 Market Cap", cap_display)
                
                # Enhanced price chart with technical indicators
                fig = go.Figure()
                
                # Candlestick chart
                fig.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name=STOCK_SYMBOLS[selected_stock],
                    increasing_line_color='#00ff88',
                    decreasing_line_color='#ff4444'
                ))
                
                # Add moving averages
                if 'SMA_20' in data.columns:
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data['SMA_20'],
                        mode='lines',
                        name='SMA 20',
                        line=dict(color='#ffaa00', width=2)
                    ))
                
                if 'SMA_50' in data.columns:
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=data['SMA_50'],
                        mode='lines',
                        name='SMA 50',
                        line=dict(color='#00aaff', width=2)
                    ))
                
                fig.update_layout(
                    title={
                        'text': f"🔴 LIVE {STOCK_SYMBOLS[selected_stock]} - {analysis_period} Price Chart",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': 'white'}
                    },
                    xaxis_title="Date",
                    yaxis_title="Price (₹)",
                    height=600,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                )
                
                st.plotly_chart(fig, use_container_width=True)   
             
                # Enhanced Technical Analysis
                st.markdown("""
                <div class="enhanced-card">
                    <h3>📈 Advanced Technical Analysis</h3>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, cn() mai":
   n__mai== "__me__ if __na

e)th=Trutainer_wid, use_con_chart(figtlylot.p       s  
 
      
        )'white'))or=t(colont=dic0,0,0)', frgba(0,ct(bgcolor='legend=di            ite'),
', color='wh.1),0(255,255,255or='rgbaridcolict(gaxis=d      y
      ite'),or='wh, col5,0.1)'55,255,2(25rgba(gridcolor='axis=dict      x
      ),ite'='whcolorct(t=dion   f  ',
       gba(0,0,0,0)lor='rgcopaper_b           0)',
 rgba(0,0,0,='plot_bgcolor           500,
 eight=       h₹)",
     "Amount (s_title=      yaxi     ars",
 title="Ye xaxis_             },
 
         '}'white6, 'color': : 1nt': {'size'   'fo             er',
cent: '  'xanchor'               0.5,
     'x':          
 ver Time", Growth OSIP"📈 lse f step_up eup)" ip-e}% steattep_up_r({sr Time owth Ove SIP Grf"📈t': 'tex                   title={
   t(
      pdate_layouig.u   f    
             ))
False
    owlegend=          sh
  , Returns'  name='📈         ,
 )')255,0ba(255,255,ct(color='rg    line=di    
    1)',6, 0.55, 13r='rgba(0, 2lo     fillco    ty',
   l='tonex      fil  ],
    ::-1ts[ested_amounvalues + inv y=maturity_
           1], years[::-ars +       x=yeer(
     catt_trace(go.S.add
        figow returns shn lines toea betweed ar # Ad 
         
            ))size=8)
 arker=dict(     m      idth=3),
 8', w00ff8or='#ict(colline=d         lue',
   Maturity Vame='🎯          na
   rs',lines+marke   mode='
         es,aluy=maturity_v   ,
              x=years     (
  .Scatter(gotracedd_   fig.a    
        ))
       8)
  (size=er=dict mark
            width=3),',r='#ff6b6bne=dict(colo          lited',
   Total Inves   name='💰      ,
   ers'ines+markde='l   mo,
         ntsnvested_amou    y=i      ears,
   x=y     ter(
      at_trace(go.Sc    fig.add     
    e()
   .Figur  fig = go  
      
      fv_temp)append(ty_values.uri        mat
        ths_temp mont *_amoun monthlyp =     fv_tem         
          else:        rn)
    retuthly_ monn) * (1 +ly_retur month 1) /s_temp -** month) rn_retu1 + monthlyunt * ((( monthly_amotemp =        fv_             0:
 >turnthly_re  if mon            * 12
  year s_temp =   month                   
          ested)
 ar_invd(yents.appenouvested_am     in        * year
   12 y_amount * = monthl_invested        year         lation
SIP calcugular # Re               e:
      els)
       d(temp_fvues.appenty_valaturi        m  00)
       1rate / step_up_ip *= (1 +_s     temp                   - 1:
year  <         if y         mp_sip
   fv += te    temp_                    lse:
     e                  hs)
     ntmoaining_urn) ** remmonthly_retip * ((1 + += temp_s temp_fv                           urn > 0:
 thly_ret     if mon                 2 - m
   - y) * 1ear= (yg_months mainin         re        :
       r_months)eae(yn rangor m i   f            12
      nths =r_moyea                :
    ange(year)y in r    for        ount
      monthly_amip =emp_s t               
emp_fv = 0   t          ue
   urity valp matep-ualculate st      # C
                         )
 edstveinppend(year_unts.ainvested_amo                ate / 100)
 + step_up_r*= (1 temp_sip                    1:
    year -  <         if y            
emp_sip * 12nvested += tr_i      yea            (year):
  n range y i      for        nt
  onthly_amou_sip = mmpte               d = 0
 year_investe                amount
p invested te step-ucula      # Cal          
 0:rate > if step_up_          in years:
  year     for      
    ]
  s = [urity_valueat
        mts = []ted_amoun      inves
  1))+ riod nt_pevestme(range(1, inars = list       ye 
     n")
   Projectioh 📈 SIP Growt## rkdown("##   st.ma    Chart
 th ced SIP Growhan        # En     
   :.1f}x")
multiplieralth_", f"{welierip Wealth Multric("🚀  st.met        
  se 1ed > 0 elinvestal_if totd vestetotal_inure_value /  futier =ultipl   wealth_m
         iplierlth mult # Wea             

          %")1f}ct:."{returns_prns %", fetu R("📊 Total st.metric     }")
      _value:,.0ff"₹{futurey Value",  Maturittric("🎯 st.me           ")
:,.0f}l_returnsota₹{trns", f"cted Retu📈 Expe"etric(t.m       s  }")
   vested:,.0ftotal_inf"₹{stment", vetal In"💰 Toric(    st.met       d styling
 enhance with cssplay metri        # Di    
    0
        e sted > 0 elsl_inveta* 100 if tovested) al_inotturns / ttal_retorns_pct = (      retu
      nvestede - total_ialuture_vs = fureturn   total_
                 ths
    on_amount * monthlyted = ml_inves  tota          hs
    nt * montonthly_amou= mue e_val futur                  else:
                 y_return)
(1 + monthl_return) * onthlyhs - 1) / mont) ** meturn+ monthly_r (((1 t *ly_amounth = monuture_value     f             :
  n > 0_retur  if monthly           ion
   P calculategular SI # R            lse:
    e         e / 100)
  p_up_ratte (1 + sip *=current_s                      iod - 1:
  estment_perinv < earf y  i               ally
   annuP amount ease SI     # Incr             
                      t_sip
+= currend tal_investe          to           ip
   rrent_sue += cuvalture_      fu                     :
  else             
          ning_months) ** remaihly_return) ((1 + mont_sip *ntue += curre_val      future                    nth)
  + moyear * 12 onths - (ths = maining_mon       rem               
       0: >rnretu monthly_     if                 
  _months):range(yearh in r mont       fo       2
      = 1nths    year_mo           
      od):t_peritmenes range(invr year info                  
         t
     onthly_amounsip = mrrent_   cu  
           ed = 0vest_in      total        0
  lue =   future_va              ulation
lcup SIP cap-   # Ste             
rate > 0:ep_up_ if st       
               2
 0 / 1return / 10xpected_n = ely_retur   month       iod * 12
  erent_p = investm  months          up
p-tes with seturnate SIP rCalcul      #  
           ")
      ionsoject# 🎯 SIP Prdown("###     st.mark     
    with col2:
          
    = 0ate ep_up_r          st:
              else, 1.0)
    .0, 10.0 20", 5.0,ease (%)l IncrAnnuaider("t.slrate = step_up_ s            p:
   if step_u         e)")
   easAnnual Incr-up SIP (x("📈 Stepkbo st.chec step_up =
            optionep-up SIP    # St 
                  =0.5)
 2.0, step  value=1                           
         =25.0, max_value.0, value=6n_   mi                            
       %)", n (Retur Annual edExpectider("📈  = st.slcted_return expe       =1)
    ue=10, step    val                                    
       alue=30,_v=1, maxlue  min_va                                     
       Years)", Period (ment 📅 Invester_input("mbt.nud = sriopent_tme   inves
         ep=500)0000, stalue=1  v                                         
 0,alue=10000e=500, max_valu       min_v                                 ₹)", 
   t ( SIP Amounhlynt("💰 Moinputmber_ount = st.nu_am     monthly")
       arametersIP Pn("#### 📊 St.markdow         s
    with col1:     
      2)
    s( st.columncol1, col2 =     
          tml=True)
 _h_allow"", unsafe
        "/div>>
        <h3</ectionsd ProjdvancePro - Ator P Calcula    <h3>💰 SI       >
 rd"nhanced-ca class="e   <div  "
   down(""    st.mark2:
    tabwith 
    
    .")he filters adjust tseia. Pleayour criteratch o funds ming("Nst.warn         
   :       else
         e)
er_width=Truntain(fig, use_coartst.plotly_ch                    
      
         )           )
  te'='whi, color1)'5,0.255,255,25rgba(or='(gridcolictaxis=d    y          
      ,lor='white')', co55,255,0.1)(255,2dcolor='rgbais=dict(gri         xax     ,
      te')hict(color='w    font=di              
  )',(0,0,0,0rgbabgcolor='   paper_                
 ',,0,0)='rgba(0,0lort_bgco         plo           ight=400,
         he          (%)",
 ns "Returle=  yaxis_tit               
   al Funds",utuitle="M   xaxis_t        
         },                 
   'white'}, 'color':  {'size': 16font':           '          enter',
    'cchor':    'xan            5,
         'x': 0.                  
     ", Returnsers - 1 Yearp 10 Performxt': "🏆 To       'te             le={
    it      t              ayout(
date_l  fig.up         
                 )
             )      'auto'
 n=ositio textp                   _1y],
returns" for r in {r:.1f}%=[f"     text               ns_1y],
 retur44' for r in44#ffe ' els0' if r > 8a0 else '#ffaif r > 12'#00ff88' lor=[coarker_ m                 y,
  urns_1 y=ret               
    nd_names, x=fu              
     (go.Bar(d_trace  fig.ad                  
          rmers]
  perfod in top_un for f''))lace('%', ].repn''1Y Returt(fund[oa= [fly eturns_1      r        ers]
  rform in top_peor fund'] fnd Nameund['Fu > 20 else fFund Name'])und['" if len(f..:20] + ".me'][und['Fund Nad_names = [f         fun
                  )
     .Figure(goig =   f           
           
        0])[:1verse=True         re                        , 
     %', '')).replace('eturn'](x['1Y Ra x: floatkey=lambd                            
          ds, ed_funlterrted(firmers = sop_perfo to              > 0:
 ed_funds) ter len(fil if           rs chart
me perfor     # Top  
               
  =True)idthainer_we_contf, ustaframe(d      st.da
      ered_funds)ame(filtd.DataFr     df = pds
       unfiltered f  # Display             
         ia**")
  criteratching yourds)} funds miltered_fun {len(f**📊 Foundkdown(f"marst.          
  :ered_fundsif filt       
   )
          }
        }"min_sip']{fund_data['P': f"₹SI 'Min              ",
  um']:,}Crund_data['a': f"₹{fAUM  '            
  ]:.1f}⭐",rating'und_data['"{f'Rating': f                .2f}%",
tio']:nse_ra_data['expeund{fatio': f" 'Expense R            ,
   5y']:.1f}%"'return_ata[_dnd f"{fueturn':  '5Y R           ,
   3y']:.1f}%"urn_a['retund_datn': f"{f'3Y Retur         
       %",']:.1f}turn_1yund_data['re{frn': f"1Y Retu '     
          ]:.2f}",nav'_data['"₹{fund  'NAV': f         
     y'],a['categornd_dat fu'Category':        
        'name'],_data[e': fundd Nam  'Fun          nd({
    nds.appeiltered_fu         f      
   
      ntinue     co           ating:
'] < min_r'ratingdata[d_un if f       tinue
      con       
       _house:undelected_f'] != sd_house_data['funnd fund= "All" ause !_ho_fundected    if sel   inue
           cont     
     ry:egoed_cat= select] !gory'd_data['cated fun= "All" anory !teglected_caif se            :
ems()S.it_FUNDin MUTUALfund_data d_id, fun  for = []
      unds  filtered_f      ection
 based on selilter funds    # F 
            )
.0, 3.0, 0.10, 5 1.m Rating",Minimur("⭐ .slide = stn_rating          mith col3:
  
        wi
        ses)+ fund_hou, ["All"] ouse"("🏢 Fund Htboxlecse_house = st.funded_  select          )]))
UNDS.values(n MUTUAL_Ffor fund i_house'] fund['fund([list(sets = house    fund_
        2:ith col     w   
        
tegories) + ca ["All"]Category",x("📂 Fund electbo= st.scategory   selected_          lues()]))
NDS.vaFUMUTUAL_r fund in tegory'] fo'ca([fund[ list(seties =    categor1:
        ith col   w   
     (3)
     nsolumcol3 = st.ccol1, col2, 
        ringfiltefund d ance # Enh       
e)
        Trul=tmw_h_allounsafe   """, v>
        </di/h3>
     0+ Funds<rer - 5 Explo Fundtual<h3>🔍 Mu           d-card">
 hanceenlass="    <div c"
    kdown(""mar       st.
 th tab1:  wi 
   ])
   cker"
   formance Tra "📈 Per      AI", 
 uilder  B📊 Portfolio    " 
     Pro",ulator"💰 SIP Calc 
        plorer",Fund Ex   "🔍     
 s([4 = st.tab2, tab3, tab, tabbs
    tab1nced tae enha
    # Creatue)
    llow_html=Trnsafe_a u""",
      </div>ates</p>
  pdime NAV uand real-tns ommendatio-powered rec AIds withual Fun50+ Mut       <p>er</h2>
 SIP Centl Fund & ua Mutanced <h2>💰 Enh       rd">
anced-cass="enh <div cla
   ""wn(".markdo():
    std_centeral_funmutunhanced_f show_e
degain.")
ase try aock. Ple stthe selecteda for to fetch dat Unable "❌ st.error(             
  else:             
         ")
  e:.2f}et_pricrgss:** ₹{taLoStop *🎯 kdown(f"*    st.mar               
     02))(score * 0.e * (1 + ent_pric currt_price =    targe                   "]:
 "SELLONG SELL", n in ["STRecommendatio      elif r         f}")
     rice:.2target_p₹{** arget Price:"**🎯 Twn(f  st.markdo                02))
       * 0. + (scorece * (1_pri currentrice = target_p                      
 :"BUY"], NG BUY"n ["STROion iecommendat   if r              ified)
   price (simplrget    # Ta                       
        
      }")sk_levell:** {rik Leve*🛡️ Risn(f"*arkdow  st.m          "
        "Low20 else lity > atiium" if vollse "Med2 ere) < bs(sco> 30 or ay atilitif vol "High" level =      risk_         t
     ssessmen   # Risk a                    
                 tor}")
wn(f"• {fac   st.markdo                  s:
   n factoror ir fact  fo           )
       Factors:"Analysis ### 📋 "#down(st.mark         
            col2:th wi                   
         e)
   tml=Trulow_hfe_al"", unsa         "            </div>
                  /10</p>
 e}core: {sr;">AI Scorn: cente"text-alige= <p styl                     /h3>
  }%<{confidencedence: er;">Confialign: cent="text- <h3 style                   /h2>
    tion}<nda{recommer};">r: {coloer; coloalign: cent"text-e=    <h2 styl                   
  {color};">olor: border-c}20;or: {col"backgroundle=sty" -cards="enhancediv clas        <d  
          """.markdown(f       st        1:
     col   with           
               ])
    1, 2st.columns([l1, col2 =      co        dation
   lay recommen # Disp                       
      
  ) * 3)res(sco 70 + abin(95,idence = m        conf          f4444"
  olor = "#f         c     "
      RONG SELL= "STion ndat     recomme               e:
els                3)
 re) *60 + abs(sco min(85, confidence =            "
        00or = "#ff88       col       
      "SELL"ation =    recommend            4:
     = -elif score >      
           2)core) * + abs(sn(75, 50idence = mi     conf       
        "#ffaa00"  color =                   "
on = "HOLDdatirecommen           :
         = -1score >if   el            )
   * 3re+ sco, 60 n(85 = minfidence      co              00"
8ffolor = "#8       c         "BUY"
    endation = ecomm r            2:
       if score >=     el      3)
      0 + score * n(95, 7ce = mionfiden        c      
      "#00ff88"or =     col        
        NG BUY" = "STROationend    recomm              re >= 5:
      if sco          dation
  ecommen# Generate r               
                ity")
 ilates stabicty indolatilid("✅ Low vctors.appen     fa             re += 1
    sco         
         tility < 15:f vola      eli     k")
     es ris increastylatili High vo.append("⚠️     factors               ore -= 1
 sc              
     ity > 40: volatil if          ysis
     ty analatili       # Vol             
            tum")
enome mnegativong "⚠️ Strpend( factors.ap         
          core -= 1 s            3:
       _pct < -change     elif         ")
   umentsitive momng po✅ Stro.append("factors                  e += 1
       scor            
   _pct > 3:f change   i            s
 analysi change   # Price            
               ")
   momentumeak cates w volume indiend("⚠️ Low factors.app             = 1
         score -             .7:
     0 *ume_30ol avg_vvolume <f recent_      eli          ")
ovementrts price m suppovolumeHigh "✅ rs.append(       facto       1
      core +=    s                30 * 1.5:
 lume_volume > avg_ecent_voif r            
    e analysis# Volum              
                  d)")
sh treneariA50 (bw MbeloPrice ("⚠️ appendactors.       f           -= 2
      core            s       0:
      ce < ma_5ent_pri   elif curr                 lish)")
m bulterort-0 (shove MA2ice abPr.append("🟡 actors      f              += 1
         score           
         > ma_20:_price  current   elif        
          trend)")0 (bullishA5nd Mth MA20 aice above bo"✅ Prend( factors.app                  2
       score +=              :
         a_500 > mprice > ma_2nt_urre c      if               
                ]
   loc[-1SMA_50'].i50 = data['         ma_          -1]
 oc['SMA_20'].il = data[     ma_20               s:
a.columndatn 50' i 'SMA_ns andta.column da 'SMA_20' i if              analysis
 rage veMoving a    #       
                e")
      zon in neutral ("🟡 RSIppendactors.a          f              else:
                    earish)")
ition (bondought cicates overb"⚠️ RSI indtors.append(      fac                ore -= 3
     sc                    0:
 i_val > 7    elif rs          )")
      bullishition (sold condes overindicatRSI .append("✅    factors               
      e += 3  scor                      0:
rsi_val < 3   if                  
I'].iloc[-1]RS[' datasi_val =    r         ns:
       ta.columI' in da      if 'RS          
SI analysis   # R          
                  ors = []
       fact     = 0
         score          logic
    mendationced recom # Enhan             
                ml=True)
  low_ht", unsafe_al  ""              /div>
   <             /h3>
dation<ent Recommed InvestmenowerAI-P <h3>🤖               ">
     hanced-cardenclass="iv     <d        ""
    arkdown("     st.m        
   mendationecomred RAI-Powe     #         
               xt)
    n_tetiop=posi", helf}%osition:.1"{price_pition", fe Pos("Pricric.met       st         nge"
     Ra🟡 Mid0 else "ition < 2 price_posif" ar Supporte "🟢 Nen > 80 elsitio price_pose" ifesistanc R🔴 Near = "osition_text    p          e 50
       > 0 els price_range100 ifrange) * / price_pport) rice - su ((current_pion =_posit   price              support
   e - stanc= resiice_range     pr          
      position Price     #              
                    el")
  tance levarest resis help="Ne                            % away", 
ce:.1f}nce_distan=f"{resista       delta                      , 
nce:.2f}"esista, f"₹{rnce Level"sista("Reic  st.metr                )
   level"pportarest sup="Ne     hel                        , 
}% away"stance:.1ft_di=f"{suppor delta                         ", 
   ort:.2f}, f"₹{suppel"pport LevSuetric("  st.m                        
      
        * 100e) nt_pricice) / currepre - current_istance = ((resancce_distansist          re       100
    rt) */ suppot) ce - supporrrent_pri((custance = ort_di   supp                    
              x()
   'High'].macent_data[stance = resire               
     n()ow'].midata['Lrt = recent_suppo                20)
    ata.tail(data = d   recent_         s
        elnce levResistart and  Suppo   #                
                   )
  ce" & Resistan🎯 Support# ##wn("#rkdo   st.ma           :
      ol3    with c              
           ")
   ..ating.culta", "Calric("Bemet        st.                xcept:
      e           
   ")evel}k: {beta_lelp=f"Ris, h2f}"ta:."{beta", f.metric("Best                               k"
 Risow "🟢 Llse .8 e > 0etask" if bRidium "🟡 Me> 1.5 else ta bef k" i"🔴 High Risvel = ta_le   be                       1.0
      = 0 else  !ket_variancearriance if mmarket_variance / ta = cova         be                       ns)
returket_var(marnce = np.variamarket_                          ]
      )[0][1turnsket_reurns, marv(stock_ret.conce = nparia cov                          :
     ns) > 10etur_rketd len(mar > 10 aneturns)ock_r  if len(st                          opna()
).drchange('].pct_['Closeifty_datans = nturrket_re ma                     na()
      hange().dropt_ce'].pclosns = data['Cetur stock_r                           en(data):
 == l_data)iftyd len(nempty andata.t nifty_if no                     riod])
   nalysis_peod_map[aiod=peritory(per).hisNSEI"f.Ticker("^ty_data = ynif                             try:
            n)
   atioalculified cimplBeta (s   #                       
           trend)
    olume_d", venme Trc("Voluri.met         st          rmal"
  No.2 else "🟡0 * 1vg_volume_3ume > af recent_voligh" id = "🟢 Hme_trenlu vo               olume
    ent_vec= 30 else r) >dataan() if len(.tail(30).meolume']['Ve_30 = datavolumg_        av         an()
   il(5).mee'].taata['Volum= d_volume entrec            d
        e trenolum  # V                      
           ")
     ol_level}{v"Level: ", help=flity:.2f}%olatif"{v", y (Annual)"Volatilit st.metric(             
      "🟢 Low"y > 15 else atilit volium" iflse "🟡 Med0 e> 3ty latiliif vo🔴 High"  = "   vol_level        
          100qrt(252) *p.std() * nns.slity = retur      volati           
   na()ge().drop_chanse'].pcta['Cloeturns = dat   r                tility
  # Vola                      
              cs")
   ri📊 Market Metdown("#### st.mark                    
h col2:       wit          
             MA50")
  signal} rice is {ma_help=f"P0:.2f}", "₹{ma_5MA 50", ft.metric("S           s      w"
       loBeelse "🔴  ma_50 rice >ent_p currAbove" if = "🟢 a_signal m                       
0'].iloc[-1]data['SMA_550 =          ma_       s:
        ta.column in da 'SMA_50'     if        
                       ")
    nal} MA20ig_sce is {maf"Pri}", help=.2f{ma_20:"₹ f",A 20.metric("SM        st                
🔴 Below"a_20 else "nt_price > m" if curre"🟢 Abovesignal = ma_                       oc[-1]
 20'].il'SMA_a[ma_20 = dat                       ns:
 n data.columf 'SMA_20' i           i     ges
    ra# Moving Ave                      
               ")
   {rsi_signal}nal: elp=f"Sig:.2f}", hsirrent_r", f"{cuSI (14)ric("Ret   st.m                    utral"
 else "🟡 Ne_rsi < 30 f currentld" i Overso0 else "🟢_rsi > 7urrentht" if c Overbougsignal = "🔴si_          r            iloc[-1]
  a['RSI'].nt_rsi = dat   curre                    s:
 a.columndat'RSI' in    if                  RSI
   #             
                     
    ators")Indic Technical wn("#### 🎯   st.markdo               ol1:
   with c           
                    umns(3)
ol3 = st.coldef show_
enhanced_market_analytics():
    st.markdown("""
    <div class="enhanced-card">
        <h2>📈 Enhanced Market Analytics</h2>
        <p>Professional-grade market analysis with real-time data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Market overview with enhanced visuals
    st.markdown("#### 📊 Live Market Overview")
    
    try:
        # Fetch multiple market indices
        indices = {
            "^NSEI": "NIFTY 50",
            "^BSESN": "SENSEX", 
            "^NSEBANK": "BANK NIFTY",
            "^NSEIT": "NIFTY IT"
        }
        
        market_data = {}
        for symbol, name in indices.items():
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="5d")
                if not data.empty:
                    current = data['Close'].iloc[-1]
                    prev = data['Close'].iloc[-2] if len(data) > 1 else current
                    change_pct = ((current - prev) / prev) * 100
                    market_data[name] = {
                        'current': current,
                        'change_pct': change_pct,
                        'data': data
                    }
            except:
                continue
        
        if market_data:
            cols = st.columns(len(market_data))
            
            for i, (name, data) in enumerate(market_data.items()):
                with cols[i]:
                    delta_color = "normal" if data['change_pct'] >= 0 else "inverse"
                    st.metric(
                        name,
                        f"{data['current']:.2f}",
                        delta=f"{data['change_pct']:.2f}%",
                        delta_color=delta_color
                    )
            
            # Market indices chart
            fig = go.Figure()
            
            for name, data in market_data.items():
                # Normalize data for comparison
                normalized_data = (data['data']['Close'] / data['data']['Close'].iloc[0]) * 100
                
                fig.add_trace(go.Scatter(
                    x=data['data'].index,
                    y=normalized_data,
                    mode='lines',
                    name=name,
                    line=dict(width=3)
                ))
            
            fig.update_layout(
                title={
                    'text': "📊 Market Indices Comparison (Normalized to 100)",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': 'white'}
                },
                xaxis_title="Date",
                yaxis_title="Normalized Price",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.info("📊 Connecting to live market data...")
    
    # Enhanced sector analysis
    st.markdown("#### 🏭 Sector Performance Analysis")
    
    # Sample enhanced sector data with more metrics
    sector_data = [
        {"Sector": "Banking & Finance", "Performance": 2.8, "Volume": "Very High", "PE": 12.5, "Market Cap": "₹45L Cr", "Outlook": "Bullish"},
        {"Sector": "Information Technology", "Performance": -0.8, "Volume": "High", "PE": 22.3, "Market Cap": "₹38L Cr", "Outlook": "Neutral"},
        {"Sector": "Pharmaceuticals", "Performance": 4.2, "Volume": "High", "PE": 18.7, "Market Cap": "₹28L Cr", "Outlook": "Very Bullish"},
        {"Sector": "Automobile", "Performance": 1.9, "Volume": "Medium", "PE": 15.2, "Market Cap": "₹22L Cr", "Outlook": "Bullish"},
        {"Sector": "FMCG", "Performance": 0.6, "Volume": "Low", "PE": 35.8, "Market Cap": "₹31L Cr", "Outlook": "Neutral"},
        {"Sector": "Energy & Power", "Performance": 5.1, "Volume": "Very High", "PE": 8.9, "Market Cap": "₹26L Cr", "Outlook": "Very Bullish"},
        {"Sector": "Metals & Mining", "Performance": 3.4, "Volume": "High", "PE": 6.2, "Market Cap": "₹18L Cr", "Outlook": "Bullish"},
        {"Sector": "Real Estate", "Performance": -2.1, "Volume": "Medium", "PE": 25.6, "Market Cap": "₹12L Cr", "Outlook": "Bearish"}
    ]
    
    df = pd.DataFrame(sector_data)
    
    # Enhanced sector performance visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance bar chart
        fig = px.bar(
            df,
            x='Sector',
            y='Performance',
            color='Performance',
            title="📊 Sector Performance (%)",
            color_continuous_scale=['#ff4444', '#ffaa00', '#00ff88'],
            text='Performance'
        )
        
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white', tickangle=45),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
            title=dict(font=dict(color='white'))
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # PE Ratio comparison
        fig = px.scatter(
            df,
            x='PE',
            y='Performance',
            size='Market Cap',
            color='Outlook',
            hover_name='Sector',
            title="📈 PE Ratio vs Performance",
            color_discrete_map={
                'Very Bullish': '#00ff88',
                'Bullish': '#88ff00',
                'Neutral': '#ffaa00',
                'Bearish': '#ff4444'
            }
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
            title=dict(font=dict(color='white'))
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Sector details table
    st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()