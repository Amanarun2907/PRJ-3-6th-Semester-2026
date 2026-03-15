# सार्थक निवेश - Main Streamlit Application
# Indian Stock Market Analysis & IPO Prediction Platform - Phase 2

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3
import os
import json

# Import our Phase 2 modules
from config import *
from data_collector import DataCollector
from stock_analyzer import AdvancedStockAnalyzer
from sentiment_analyzer import AdvancedSentimentAnalyzer
from excel_manager import ExcelExportManager
from excel_exporter import ExcelExporter
from sentiment_analyzer import SentimentAnalyzer
from risk_management import InstitutionalRiskManager
from professional_analyzer import ProfessionalFinancialAnalyzer

# Page Configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# ENHANCED CSS FOR MAXIMUM TEXT VISIBILITY - EVERY TEXT CRYSTAL CLEAR
st.markdown("""
<style>
    /* GLOBAL TEXT VISIBILITY SETTINGS - HIGHEST PRIORITY */
    * {
        font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
    }
    
    /* STREAMLIT GLOBAL TEXT OVERRIDES */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    /* Prevent text overlap and ensure wrapping */
    .stApp, .stApp * { line-height: 1.6 !important; }
    .stMarkdown, p, div, span, label { word-wrap: break-word !important; overflow-wrap: anywhere !important; }
    .element-container { box-sizing: border-box !important; }
    
    /* ALL HEADINGS - MAXIMUM CONTRAST */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-weight: 700 !important;
        text-shadow: none !important;
        margin-bottom: 1rem !important;
        line-height: 1.4 !important;
    }
    
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }
    h4 { font-size: 1.25rem !important; }
    h5 { font-size: 1.1rem !important; }
    h6 { font-size: 1rem !important; }
    
    /* ALL PARAGRAPH TEXT - MAXIMUM READABILITY */
    p, div, span, label, .stMarkdown {
        color: #000000 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
        text-shadow: none !important;
    }
    
    /* SIDEBAR TEXT VISIBILITY */
    .css-1d391kg, .css-1d391kg * {
        background-color: #f8f9fa !important;
        color: #000000 !important;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg h4 {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* MAIN HEADER - ENHANCED VISIBILITY */
    .main-header {
        background: linear-gradient(135deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border: 2px solid #FF9933;
    }
    
    .main-header h1 {
        color: #000000 !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-shadow: none !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 1px !important;
    }
    
    .main-header h3 {
        color: #000000 !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        margin-top: 0.5rem !important;
        text-shadow: none !important;
    }
    
    .main-header p {
        color: #000000 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        text-shadow: none !important;
    }
    
    /* METRIC CARDS - PERFECT TEXT VISIBILITY */
    .metric-card {
        background: #ffffff !important;
        padding: 1.5rem;
        border-radius: 12px;
        border: 3px solid #FF9933;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        border-color: #138808;
    }
    
    .metric-card h4 {
        color: #000000 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .metric-card h2 {
        color: #FF9933 !important;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        margin: 0.5rem 0 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
    }
    
    .metric-card p {
        color: #000000 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }
    
    /* TEAM INFO - ENHANCED READABILITY */
    .team-info {
        background: #ffffff !important;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        border: 3px solid #138808;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    .team-info h4 {
        color: #000000 !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .team-info p {
        color: #000000 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        line-height: 1.8 !important;
        margin-bottom: 0.8rem !important;
    }
    
    .team-info strong {
        color: #FF9933 !important;
        font-weight: 700 !important;
    }
    
    /* STREAMLIT COMPONENTS - MAXIMUM VISIBILITY */
    .stSuccess {
        background-color: #d4edda !important;
        border: 2px solid #28a745 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stInfo {
        background-color: #d1ecf1 !important;
        border: 2px solid #17a2b8 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        border: 2px solid #ffc107 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stError {
        background-color: #f8d7da !important;
        border: 2px solid #dc3545 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* BUTTON STYLING - CLEAR TEXT */
    .stButton > button {
        background: linear-gradient(135deg, #FF9933 0%, #ff7849 100%) !important;
        color: #ffffff !important;
        border: 2px solid #FF9933 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #138808 0%, #0d5d0d 100%) !important;
        border-color: #138808 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(255, 153, 51, 0.4) !important;
    }
    
    /* SELECTBOX AND INPUT STYLING */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 2px solid #FF9933 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox label {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        border: 2px solid #FF9933 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stTextInput label {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    /* DATAFRAME STYLING - PERFECT READABILITY */
    .dataframe {
        border: 2px solid #FF9933 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        background-color: #ffffff !important;
    }
    
    .dataframe th {
        background-color: #FF9933 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-align: center !important;
        padding: 12px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    .dataframe td {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 10px !important;
        border-bottom: 1px solid #e5e7eb !important;
    }
    
    /* METRIC COMPONENT STYLING */
    .metric-container {
        background-color: #ffffff !important;
        border: 2px solid #FF9933 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .metric-container label {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    
    .metric-container div {
        color: #FF9933 !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
    }
    
    /* EXCEL SECTION - ENHANCED VISIBILITY */
    .excel-section {
        background: #ffffff !important;
        padding: 1.5rem;
        border-radius: 12px;
        border: 3px solid #138808 !important;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    .excel-section h4 {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        margin-bottom: 1rem !important;
        text-transform: uppercase !important;
    }
    
    .excel-section p {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    /* SIDEBAR SPECIFIC OVERRIDES */
    .css-1d391kg .stSelectbox label,
    .css-1d391kg .stButton button,
    .css-1d391kg h1,
    .css-1d391kg h2,
    .css-1d391kg h3,
    .css-1d391kg h4,
    .css-1d391kg p,
    .css-1d391kg div {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* PLOTLY CHART STYLING */
    .js-plotly-plot {
        border: 2px solid #FF9933 !important;
        border-radius: 8px !important;
        background-color: #ffffff !important;
    }
    
    /* EXPANDER STYLING */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: 2px solid #FF9933 !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #e5e7eb !important;
        border-top: none !important;
    }
    
    /* SPINNER TEXT */
    .stSpinner > div {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    /* CODE BLOCKS */
    .stCode {
        background-color: #f8f9fa !important;
        border: 2px solid #FF9933 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    /* Tables readability */
    .stDataFrame table { width: 100% !important; }
    .stDataFrame table th, .stDataFrame table td { white-space: normal !important; word-break: break-word !important; }
    
    /* ENSURE ALL TEXT IS VISIBLE */
    .stApp * {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    /* OVERRIDE ANY LIGHT TEXT */
    .css-1v0mbdj, .css-1v0mbdj *, 
    .css-1d391kg, .css-1d391kg *,
    .css-12oz5g7, .css-12oz5g7 * {
        color: #000000 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>📈 {PROJECT_NAME}</h1>
        <h3>AI-Powered Indian Stock Market Analysis & IPO Prediction Platform</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.selectbox(
        "Choose Analysis Type",
        [
            "🏠 Dashboard",
            "📊 Stock Analysis", 
            "🚀 IPO Analysis (Unique)",
            "📰 News & Sentiment",
            "💰 Portfolio Tracker",
            "🔔 Alerts",
            "💰 Investment Tools",
            "📈 Analytics",
            "📋 Excel Reports",
            "❓ FAQs",
            "🤖 AI Assistant",
            "⚙️ Data Collection"
        ]
    )
    
    # Initialize data collector and other modules
    if 'data_collector' not in st.session_state:
        st.session_state.data_collector = DataCollector()
    
    if 'excel_exporter' not in st.session_state:
        st.session_state.excel_exporter = ExcelExporter()
    
    if 'sentiment_analyzer' not in st.session_state:
        st.session_state.sentiment_analyzer = SentimentAnalyzer()
    
    if 'stock_analyzer' not in st.session_state:
        st.session_state.stock_analyzer = AdvancedStockAnalyzer()
    
    # Route to different pages
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📊 Stock Analysis":
        show_stock_analysis()
    elif page == "🚀 IPO Analysis (Unique)":
        show_ipo_analysis()
    elif page == "📰 News & Sentiment":
        show_news_sentiment()
    elif page == "💰 Portfolio Tracker":
        show_portfolio()
    elif page == "🔔 Alerts":
        show_alerts()
    elif page == "💰 Investment Tools":
        show_investment_tools()
    elif page == "📈 Analytics":
        show_analytics()
    elif page == "📋 Excel Reports":
        show_excel_reports()
    elif page == "🤖 AI Assistant":
        show_ai_assistant()
    elif page == "❓ FAQs":
        show_faqs()
    elif page == "⚙️ Data Collection":
        show_data_collection()
    
    # Team Information Footer
    st.markdown("""
    <div class="team-info">
        <h4>👥 Development Team</h4>
        <p><strong>Project:</strong> B.Tech 3rd Year - Indian Stock Market Analysis</p>
        <p><strong>Team Members:</strong> Aman Jain, Rohit Fogla, Vanshita Mehta, Disita Tirthani</p>
        <p><strong>Unique Feature:</strong> Post-IPO Liquidity & Retail Sentiment Forecast</p>
    </div>
    """, unsafe_allow_html=True)

def show_dashboard():
    st.header("📊 Market Overview Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📈 Stocks Tracked</h4>
            <h2>20</h2>
            <p>Multi-sector coverage</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🚀 IPO Analysis</h4>
            <h2>Active</h2>
            <p>Unique feature</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>📰 News Sources</h4>
            <h2>6</h2>
            <p>Real-time sentiment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>🤖 AI Features</h4>
            <h2>7</h2>
            <p>ML predictions</p>
        </div>
        """, unsafe_allow_html=True)
    
    # High-level information (all detailed real-time dashboards are in Phase 2 app)
    st.subheader("📈 Live Market Analytics")
    st.info(
        "For full real-time sector performance, advanced analytics, and Excel reports, "
        "please use the Phase 2 advanced application (`main_phase2.py`). "
        "This Phase 1 interface provides a basic overview without any sample or dummy charts."
    )

def show_stock_analysis():
    st.header("📊 Advanced Stock Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Stock selector with enhanced display
        selected_stock = st.selectbox(
            "Select Stock for Analysis",
            options=list(STOCK_SYMBOLS.keys()),
            format_func=lambda x: f"{STOCK_SYMBOLS[x]} ({x})"
        )
    
    with col2:
        # Analysis period selector
        analysis_period = st.selectbox(
            "Analysis Period",
            options=[30, 60, 90, 180, 365],
            format_func=lambda x: f"{x} days",
            index=2  # Default to 90 days
        )
    
    if st.button("📈 Analyze Stock", key="analyze_stock_btn"):
        with st.spinner("Analyzing stock data and sentiment..."):
            # Get stock data
            data = st.session_state.data_collector.get_stock_data(selected_stock, days=analysis_period)
            
            # Get stock-specific sentiment
            sentiment_data = st.session_state.sentiment_analyzer.get_stock_specific_sentiment(selected_stock)
            
            if not data.empty:
                st.success(f"✅ Analysis completed for {STOCK_SYMBOLS[selected_stock]}")
                
                # Enhanced metrics display
                col_a, col_b, col_c, col_d, col_e = st.columns(5)
                
                latest_price = data.iloc[0]['close']
                prev_price = data.iloc[1]['close'] if len(data) > 1 else latest_price
                change = latest_price - prev_price
                change_pct = (change / prev_price) * 100 if prev_price != 0 else 0
                
                with col_a:
                    st.metric("Latest Price", f"₹{latest_price:.2f}", 
                             f"{change:+.2f} ({change_pct:+.2f}%)")
                
                with col_b:
                    st.metric("Volume", f"{data.iloc[0]['volume']:,}")
                
                with col_c:
                    high_52w = data['high'].max()
                    low_52w = data['low'].min()
                    st.metric("52W High", f"₹{high_52w:.2f}")
                    st.metric("52W Low", f"₹{low_52w:.2f}")
                
                with col_d:
                    if sentiment_data:
                        sentiment_color = "normal"
                        if sentiment_data['sentiment_score'] > 0.1:
                            sentiment_color = "normal"
                        elif sentiment_data['sentiment_score'] < -0.1:
                            sentiment_color = "inverse"
                        
                        st.metric("Sentiment", sentiment_data['sentiment_label'], 
                                f"{sentiment_data['sentiment_score']:.3f}")
                        st.metric("News Articles", sentiment_data['articles_count'])
                
                with col_e:
                    try:
                        import yfinance as yf
                        ticker = yf.Ticker(selected_stock)
                        live_hist = ticker.history(period="1d", interval="1m")
                        if not live_hist.empty:
                            live_price = float(live_hist['Close'].iloc[-1])
                            st.metric("Live Price (1m)", f"₹{live_price:.2f}")
                            if st.button("🔄 Refresh Live Price", key="refresh_live"):
                                st.experimental_rerun()
                    except Exception as e:
                        st.info("Live 1m price unavailable right now.")
                
                # Option: use live internet data for chart
                use_live = st.checkbox("Use live internet data for chart (yfinance)", value=True)
                chart_df = data.copy()
                if use_live:
                    try:
                        import yfinance as yf
                        ticker = yf.Ticker(selected_stock)
                        live_daily = ticker.history(period="6mo", interval="1d")
                        if not live_daily.empty:
                            chart_df = pd.DataFrame({
                                'date': live_daily.index.tz_localize(None),
                                'close': live_daily['Close'].values,
                                'volume': live_daily['Volume'].values
                            }).sort_values('date')
                            chart_df.reset_index(drop=True, inplace=True)
                    except Exception:
                        pass

                # Enhanced price chart
                fig = go.Figure()
                
                # Add price line
                fig.add_trace(go.Scatter(
                    x=pd.to_datetime(chart_df['date']),
                    y=chart_df['close'],
                    mode='lines',
                    name='Close Price',
                    line=dict(color='#FF9933', width=3),
                    hovertemplate='<b>Date</b>: %{x}<br><b>Price</b>: ₹%{y:.2f}<extra></extra>'
                ))
                
                # Add volume as secondary y-axis
                fig.add_trace(go.Bar(
                    x=pd.to_datetime(chart_df['date']),
                    y=chart_df['volume'],
                    name='Volume',
                    yaxis='y2',
                    opacity=0.3,
                    marker_color='#138808'
                ))
                
                # Update layout for dual y-axis
                fig.update_layout(
                    title=f"{STOCK_SYMBOLS[selected_stock]} - Price & Volume Analysis",
                    xaxis_title="Date",
                    yaxis=dict(title="Price (₹)", side="left"),
                    yaxis2=dict(title="Volume", side="right", overlaying="y"),
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Technical indicators
                st.subheader("📊 Technical Indicators")
                
                # Calculate simple moving averages
                chart_df['SMA_20'] = chart_df['close'].rolling(window=20).mean()
                chart_df['SMA_50'] = chart_df['close'].rolling(window=50).mean()
                
                # Display technical analysis
                col_tech1, col_tech2 = st.columns(2)
                
                with col_tech1:
                    st.write("**Moving Averages:**")
                    if len(chart_df) >= 20:
                        sma_20 = chart_df['SMA_20'].iloc[-1]
                        st.write(f"• SMA 20: ₹{sma_20:.2f}")
                        
                        if latest_price > sma_20:
                            st.success("📈 Price above SMA 20 (Bullish)")
                        else:
                            st.error("📉 Price below SMA 20 (Bearish)")
                    
                    if len(chart_df) >= 50:
                        sma_50 = chart_df['SMA_50'].iloc[-1]
                        st.write(f"• SMA 50: ₹{sma_50:.2f}")
                        
                        if latest_price > sma_50:
                            st.success("📈 Price above SMA 50 (Bullish)")
                        else:
                            st.error("📉 Price below SMA 50 (Bearish)")
                
                with col_tech2:
                    st.write("**Price Analysis:**")
                    
                    # Support and resistance levels
                    support = data['low'].min()
                    resistance = data['high'].max()
                    
                    st.write(f"• Support Level: ₹{support:.2f}")
                    st.write(f"• Resistance Level: ₹{resistance:.2f}")
                    
                    # Price position
                    price_range = resistance - support
                    price_position = (latest_price - support) / price_range * 100
                    
                    st.write(f"• Price Position: {price_position:.1f}% of range")
                    
                    if price_position > 80:
                        st.warning("⚠️ Near resistance level")
                    elif price_position < 20:
                        st.info("💡 Near support level")
                    else:
                        st.success("✅ In middle range")
                
                with st.expander("🔮 Forecast (Educational Preview)"):
                    horizon = st.selectbox("Forecast Horizon", options=[7, 30, 90], format_func=lambda x: f"{x} days")
                    if st.button("Run Forecast", key="run_forecast"):
                        forecast = st.session_state.stock_analyzer.quick_price_forecast(selected_stock, horizon_days=horizon)
                        if forecast:
                            ffig = go.Figure()
                            ffig.add_trace(go.Scatter(x=forecast['history']['date'], y=forecast['history']['actual'], mode='lines', name='Actual', line=dict(color='#138808', width=2)))
                            ffig.add_trace(go.Scatter(x=forecast['forecast']['date'], y=forecast['forecast']['forecast'], mode='lines', name='Forecast', line=dict(color='#FF0000', width=2, dash='dash')))
                            ffig.update_layout(title=f"{STOCK_SYMBOLS[selected_stock]} - Price Forecast ({horizon} days)", xaxis_title="Date", yaxis_title="Price (₹)", height=500, hovermode='x unified')
                            st.plotly_chart(ffig, use_container_width=True)
                        else:
                            st.info("Not enough historical data to run the forecast.")
                
                # Sentiment analysis section
                if sentiment_data and sentiment_data['articles_count'] > 0:
                    st.subheader("📰 News Sentiment Analysis")
                    
                    col_sent1, col_sent2 = st.columns(2)
                    
                    with col_sent1:
                        sentiment_score = sentiment_data['sentiment_score']
                        
                        if sentiment_score > 0.1:
                            st.success(f"😊 Positive Sentiment: {sentiment_score:.3f}")
                            st.write("Recent news shows positive market sentiment for this stock.")
                        elif sentiment_score < -0.1:
                            st.error(f"😟 Negative Sentiment: {sentiment_score:.3f}")
                            st.write("Recent news shows negative market sentiment for this stock.")
                        else:
                            st.info(f"😐 Neutral Sentiment: {sentiment_score:.3f}")
                            st.write("Recent news shows neutral market sentiment for this stock.")
                    
                    with col_sent2:
                        st.metric("News Articles Found", sentiment_data['articles_count'])
                        
                        if sentiment_data['fake_news_count'] > 0:
                            st.warning(f"⚠️ {sentiment_data['fake_news_count']} potential fake news detected")
                        else:
                            st.success("✅ No fake news detected")
                
            else:
                st.warning("No data available. Please run data collection first.")
                
                # Show data collection button
                if st.button("🔄 Collect Data for This Stock"):
                    with st.spinner(f"Collecting data for {STOCK_SYMBOLS[selected_stock]}..."):
                        st.session_state.data_collector.collect_stock_data(selected_stock)
                        st.success("✅ Data collection completed! Click 'Analyze Stock' again.")

def show_ipo_analysis():
    st.header("🚀 IPO Analysis - Unique Feature")
    st.info("Unique: Real-time Post-IPO performance + liquidity + sentiment with rule-based exit guidance.")

    col = st.columns(2)
    with col[0]:
        symbol = st.text_input("IPO Symbol (e.g., NYKAA.NS, LIC.NS, TATATECH.NS)")
    with col[1]:
        show_latest = st.checkbox("Show Latest IPOs")

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        if show_latest:
            latest_df = pd.read_sql_query("""
                SELECT company_name, symbol, listing_date, issue_price, performance_30d, performance_60d, performance_90d
                FROM ipo_intelligence ORDER BY listing_date DESC LIMIT 10
            """, conn)
            if not latest_df.empty:
                st.subheader("Latest IPOs (Evidence)")
                st.dataframe(latest_df, use_container_width=True)

        if symbol:
            st.subheader("📈 Post‑IPO Performance (Evidence)")
            # Build price series since listing
            price_df = pd.read_sql_query("""
                SELECT date, close, volume FROM stock_prices
                WHERE symbol = ? ORDER BY date ASC
            """, conn, params=(symbol,))
            ipo_meta = pd.read_sql_query("""
                SELECT company_name, listing_date, issue_price, sentiment_score, liquidity_score, recommendation, confidence_score
                FROM ipo_intelligence WHERE symbol = ? ORDER BY analysis_date DESC LIMIT 1
            """, conn, params=(symbol,))
            conn.close()

            if price_df.empty or ipo_meta.empty:
                st.warning("No complete IPO intelligence found. Ensure IPO data was collected in Phase 3.")
                return

            listing_date = pd.to_datetime(ipo_meta.iloc[0]['listing_date'])
            plot_df = price_df[price_df['date'] >= str(listing_date)]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=pd.to_datetime(plot_df['date']), y=plot_df['close'], mode='lines', name='Close', line=dict(color='#FF9933', width=3)))
            fig.update_layout(title="Post‑IPO Price Since Listing", xaxis_title="Date", yaxis_title="Price (₹)", height=500, hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)

            # Evidence: returns and liquidity stats
            perf_30 = (plot_df.tail(30)['close'].iloc[-1] / plot_df.head(1)['close'].iloc[0] - 1) * 100 if len(plot_df) >= 30 else None
            perf_60 = (plot_df.tail(60)['close'].iloc[-1] / plot_df.head(1)['close'].iloc[0] - 1) * 100 if len(plot_df) >= 60 else None
            perf_90 = (plot_df.tail(90)['close'].iloc[-1] / plot_df.head(1)['close'].iloc[0] - 1) * 100 if len(plot_df) >= 90 else None
            vol_mean = plot_df['volume'].rolling(5).mean().iloc[-1] if 'volume' in plot_df.columns and len(plot_df) >= 5 else None

            c1, c2, c3, c4 = st.columns(4)
            with c1: st.metric("30‑Day Return", f"{perf_30:.2f}%" if perf_30 is not None else "N/A")
            with c2: st.metric("60‑Day Return", f"{perf_60:.2f}%" if perf_60 is not None else "N/A")
            with c3: st.metric("90‑Day Return", f"{perf_90:.2f}%" if perf_90 is not None else "N/A")
            with c4: st.metric("Avg Vol (5d)", f"{vol_mean:,.0f}" if vol_mean is not None else "N/A")

            # Exit window logic with statistics
            st.subheader("🎯 Exit Window Recommendation (With Proof)")
            series = plot_df['close'].values
            peak = series.max()
            last = series[-1]
            drawdown = (last - peak) / peak * 100
            mom_10 = (series[-1] / series[-10] - 1) * 100 if len(series) >= 10 else 0
            vol_20 = pd.Series(series).pct_change().rolling(20).std().iloc[-1] * 100 if len(series) >= 21 else None

            # Rule: if price falls more than 12% from recent peak after listing+10, or momentum turns negative for 2 weeks → consider exit
            rule_hit = (drawdown <= -12) or (mom_10 < 0)
            rec_text = "Consider Partial Exit" if rule_hit else "Hold with Trailing Stop"

            e1, e2, e3 = st.columns(3)
            with e1: st.metric("Max Drawdown from Peak", f"{drawdown:.2f}%")
            with e2: st.metric("10‑Day Momentum", f"{mom_10:.2f}%")
            with e3: st.metric("Volatility (20‑day)", f"{vol_20:.2f}%" if vol_20 is not None else "N/A")

            st.info(f"Recommendation: {rec_text}. Logic: Drawdown {drawdown:.1f}% and momentum {mom_10:.1f}%. Trailing stop at 10–15% below recent peak protects gains.")

            # Evidence panel: recent news headlines & sentiment
            st.subheader("📰 Sentiment Evidence")
            try:
                conn = sqlite3.connect(DATABASE_PATH)
                news = pd.read_sql_query("""
                    SELECT title, source, published_at, sentiment_score, is_fake_news
                    FROM news_articles
                    WHERE title LIKE ? OR description LIKE ?
                    ORDER BY published_at DESC LIMIT 8
                """, conn, params=(f"%{symbol.split('.')[0]}%", f"%{symbol.split('.')[0]}%"))
                conn.close()
                if not news.empty:
                    news['Fake?'] = news['is_fake_news'].map({1: 'Yes', 0: 'No'})
                    news = news[['title', 'source', 'published_at', 'sentiment_score', 'Fake?']]
                    st.dataframe(news, use_container_width=True)
            except Exception:
                pass

    except Exception as e:
        st.error(f"IPO analysis error: {str(e)}")

def show_excel_reports():
    st.header("📋 Excel Reports & Data Export")
    
    st.markdown("""
    <div class="excel-section">
        <h4>📊 Real-time Excel Data Export</h4>
        <p>Export all your market data to Excel files for presentations and detailed analysis. 
        Files are updated hourly and saved in the <code>exports/</code> folder.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Stock Data Export")
        if st.button("📊 Export Stock Data", key="export_stocks"):
            with st.spinner("Exporting stock data to Excel..."):
                file_path = st.session_state.excel_exporter.export_stock_data()
                if file_path:
                    st.success(f"✅ Stock data exported successfully!")
                    st.info(f"📁 File saved: `{file_path}`")
                else:
                    st.error("❌ Failed to export stock data")
        
        st.subheader("🚀 IPO Analysis Export")
        if st.button("📊 Export IPO Data", key="export_ipo"):
            with st.spinner("Exporting IPO analysis to Excel..."):
                file_path = st.session_state.excel_exporter.export_ipo_analysis()
                if file_path:
                    st.success(f"✅ IPO analysis exported successfully!")
                    st.info(f"📁 File saved: `{file_path}`")
                else:
                    st.error("❌ Failed to export IPO data")
    
    with col2:
        st.subheader("📰 News & Sentiment Export")
        if st.button("📊 Export News Analysis", key="export_news"):
            with st.spinner("Exporting news sentiment to Excel..."):
                # First analyze sentiment
                st.session_state.sentiment_analyzer.analyze_market_sentiment()
                # Then export
                file_path = st.session_state.excel_exporter.export_news_sentiment()
                if file_path:
                    st.success(f"✅ News analysis exported successfully!")
                    st.info(f"📁 File saved: `{file_path}`")
                else:
                    st.error("❌ Failed to export news data")
        
        st.subheader("📋 Daily Market Report")
        if st.button("📊 Generate Daily Report", key="export_report"):
            with st.spinner("Generating comprehensive daily report..."):
                file_path = st.session_state.excel_exporter.export_daily_report()
                if file_path:
                    st.success(f"✅ Daily report generated successfully!")
                    st.info(f"📁 File saved: `{file_path}`")
                else:
                    st.error("❌ Failed to generate daily report")
    
    # Export all data at once
    st.subheader("🚀 Export All Data")
    if st.button("📊 Export Everything to Excel", key="export_all"):
        with st.spinner("Exporting all data to Excel files..."):
            exported_files = st.session_state.excel_exporter.export_all_data()
            if exported_files:
                st.success(f"✅ All data exported successfully!")
                st.info(f"📁 {len(exported_files)} files created in `exports/` folder:")
                for file in exported_files:
                    st.write(f"   • `{file}`")
            else:
                st.error("❌ Failed to export data")
    
    # Show existing files
    st.subheader("📁 Existing Excel Files")
    try:
        import os
        exports_folder = "exports"
        if os.path.exists(exports_folder):
            files = [f for f in os.listdir(exports_folder) if f.endswith('.xlsx')]
            if files:
                files_df = pd.DataFrame({
                    'File Name': files,
                    'Size (KB)': [round(os.path.getsize(os.path.join(exports_folder, f)) / 1024, 2) for f in files],
                    'Modified': [datetime.fromtimestamp(os.path.getmtime(os.path.join(exports_folder, f))).strftime('%Y-%m-%d %H:%M') for f in files]
                })
                st.dataframe(files_df, use_container_width=True)
            else:
                st.info("No Excel files found. Export some data first!")
        else:
            st.info("Exports folder not found. Export some data first!")
    except Exception as e:
        st.error(f"Error reading exports folder: {str(e)}")

def show_faqs():
    st.header("❓ Frequently Asked Questions")
    st.subheader("How is the sentiment score calculated?")
    st.write("We scan real news from trusted sources. Each article’s text is scored using a language model that measures positivity and negativity. We average these scores, giving more weight to recent and reliable sources. The final number ranges from negative to positive.")
    st.subheader("How do you detect fake news?")
    st.write("We use patterns found in misleading content, cross-check sources, and apply a classifier trained to flag suspicious language. Items marked risky are excluded from sentiment to keep results clean.")
    st.subheader("How are risk metrics computed?")
    st.write("Volatility shows how much prices move. VaR and CVaR estimate possible worst-case losses. Sharpe Ratio compares returns to risk. Diversification checks how similar your stocks move; lower similarity means better risk spread.")
    st.subheader("How do recommendations work?")
    st.write("We combine technical signals, news sentiment, risk profile, and long‑term trends into one score. That score maps to a simple label like BUY, HOLD, or SELL with a confidence percentage.")
    st.subheader("How are IPO insights created?")
    st.write("We track price and volume after listing, study public mood from news and social coverage, and use a machine learning model trained on real IPO features to estimate performance and liquidity. This gives clear hold/exit suggestions.")
    st.subheader("How is my portfolio value updated?")
    st.write("Each holding’s latest market price multiplies by quantity. We read fresh prices from the database and, if missing, fetch the latest from the market. Totals and P&L update in real time.")
    st.subheader("Are predictions 100% accurate?")
    st.write("No. Markets change fast. Our analytics are decision aids, not guarantees. Always be cautious and consider multiple factors before investing.")
def show_news_sentiment():
    st.header("📰 News & Sentiment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📰 Collect Latest News"):
            with st.spinner("Collecting news from multiple sources..."):
                st.session_state.data_collector.collect_news_data()
                st.success("✅ News collection completed!")
    
    with col2:
        if st.button("🧠 Analyze Market Sentiment"):
            with st.spinner("Analyzing sentiment and detecting fake news..."):
                results = st.session_state.sentiment_analyzer.analyze_market_sentiment()
                if results:
                    st.success("✅ Sentiment analysis completed!")
                    
                    # Display results
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("Overall Sentiment", results['sentiment_label'], 
                                f"{results['overall_sentiment']:.3f}")
                    
                    with col_b:
                        st.metric("Articles Analyzed", results['total_articles'])
                    
                    with col_c:
                        st.metric("Fake News Detected", 
                                f"{results['fake_news_count']} ({results['fake_news_percentage']}%)")
                else:
                    st.error("❌ Failed to analyze sentiment")
    
    # Display news sources
    st.subheader("📡 News Sources")
    
    sources_df = pd.DataFrame({
        'Source': ['Google News (Finance)', 'Google News (IPO)', 'Economic Times (Market)', 
                  'Economic Times (Stocks)', 'MoneyControl (Market)', 'MoneyControl (Results)', 'NewsAPI'],
        'Type': ['RSS Feed', 'RSS Feed', 'RSS Feed', 'RSS Feed', 'RSS Feed', 'RSS Feed', 'API'],
        'Status': ['✅ Active'] * 7,
        'Cost': ['Free', 'Free', 'Free', 'Free', 'Free', 'Free', 'Free (1000/day)'],
        'Features': ['General Market News', 'IPO Specific News', 'Market Reports', 
                    'Stock Analysis', 'Market Reports', 'Earnings Results', 'Comprehensive News']
    })
    
    st.dataframe(sources_df, use_container_width=True)
    
    st.subheader("📊 Market Sentiment Dashboard")
    
    # Get actual sentiment data if available
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        sentiment_query = '''
            SELECT 
                CASE 
                    WHEN sentiment_score > 0.1 THEN 'Positive'
                    WHEN sentiment_score < -0.1 THEN 'Negative'
                    ELSE 'Neutral'
                END as sentiment,
                COUNT(*) as count
            FROM news_articles 
            WHERE sentiment_score IS NOT NULL
            GROUP BY sentiment
        '''
        sentiment_df = pd.read_sql_query(sentiment_query, conn)
        conn.close()
        
        if not sentiment_df.empty:
            fig = px.pie(
                sentiment_df,
                values='count',
                names='sentiment',
                title="Market Sentiment Distribution",
                color_discrete_map={'Positive': '#16a34a', 'Neutral': '#eab308', 'Negative': '#dc2626'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sentiment data available yet. Collect news and run sentiment analysis to see live market sentiment.")
            
    except Exception as e:
        st.error(f"Error loading sentiment data: {str(e)}")
    
    # Fake News Detection Results
    st.subheader("🔍 Fake News Detection")
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        fake_news_query = '''
            SELECT 
                COUNT(*) as total_articles,
                SUM(CASE WHEN is_fake_news = 1 THEN 1 ELSE 0 END) as fake_articles
            FROM news_articles
        '''
        fake_news_df = pd.read_sql_query(fake_news_query, conn)
        conn.close()
        
        if not fake_news_df.empty and fake_news_df.iloc[0]['total_articles'] > 0:
            total = fake_news_df.iloc[0]['total_articles']
            fake = fake_news_df.iloc[0]['fake_articles']
            genuine = total - fake
            
            col_x, col_y = st.columns(2)
            
            with col_x:
                st.metric("Total Articles", total)
                st.metric("Genuine News", genuine, f"{(genuine/total)*100:.1f}%")
            
            with col_y:
                st.metric("Fake News Detected", fake, f"{(fake/total)*100:.1f}%")
                
                if fake/total > 0.2:
                    st.warning("⚠️ High fake news percentage detected!")
                else:
                    st.success("✅ Low fake news percentage - good news quality!")
        else:
            st.info("💡 No news data available for fake news analysis. Collect news first!")
            
    except Exception as e:
        st.error(f"Error loading fake news data: {str(e)}")
    
    st.subheader("📰 Latest Articles (With Proofs)")
    colf1, colf2 = st.columns(2)
    with colf1:
        hours = st.selectbox("Recent window", options=[6, 12, 24, 72], index=2, format_func=lambda x: f"Last {x} hours")
    with colf2:
        only_fake = st.checkbox("Show only potential fake news", value=False)
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        base_q = """
            SELECT title, source, published_at, sentiment_score, is_fake_news, url
            FROM news_articles 
            WHERE published_at >= datetime('now', ?)
        """
        params = (f"-{hours} hour",)
        if only_fake:
            base_q += " AND is_fake_news = 1"
        base_q += " ORDER BY published_at DESC LIMIT 50"
        articles_df = pd.read_sql_query(base_q, conn, params=params)
        conn.close()
        if not articles_df.empty:
            articles_df['Fake?'] = articles_df['is_fake_news'].map({1: 'Yes', 0: 'No'})
            articles_df.rename(columns={
                'title': 'Title', 'source': 'Source', 'published_at': 'Published',
                'sentiment_score': 'Sentiment', 'url': 'URL'
            }, inplace=True)
            display_cols = ['Title', 'Source', 'Published', 'Sentiment', 'Fake?', 'URL']
            st.dataframe(articles_df[display_cols], use_container_width=True)
    except Exception as e:
        st.info("Could not load detailed articles table.")
    
    st.subheader("🧭 Market Advice (Simple Language)")
    try:
        # Compute quick overall sentiment
        conn = sqlite3.connect(DATABASE_PATH)
        srow = pd.read_sql_query("""
            SELECT AVG(sentiment_score) as avg_s, SUM(CASE WHEN is_fake_news=1 THEN 1 ELSE 0 END) as fake_c, COUNT(*) as total_c
            FROM news_articles WHERE published_at >= datetime('now','-3 day')
        """, conn).iloc[0]
        conn.close()
        avg_s = srow['avg_s'] if srow['avg_s'] is not None else 0.0
        fake_ratio = (srow['fake_c']/srow['total_c']*100) if srow['total_c'] else 0.0
        # Simple advice rules
        advice = []
        if avg_s > 0.1:
            advice.append("Overall news mood is positive. It may be a good time to continue SIPs and hold quality stocks.")
        elif avg_s < -0.1:
            advice.append("News mood is negative. Be cautious, prefer SIPs over lumpsum, and focus on diversified or index funds.")
        else:
            advice.append("News mood is mixed. Stick to your plan, keep SIPs steady, and avoid overreacting.")
        if fake_ratio > 10:
            advice.append("High fake news proportion detected. Double‑check headlines before acting.")
        advice.append("For IPOs: Use our IPO analysis to check post‑listing momentum before entering.")
        advice.append("For Mutual Funds & Index Funds: Favor diversified funds when volatility is high.")
        for a in advice:
            st.write(f"- {a}")
    except Exception:
        pass

def show_alerts():
    st.header("🔔 Alerts Center")
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                symbol TEXT,
                direction TEXT,
                target_price REAL,
                keyword TEXT,
                threshold REAL,
                enabled INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_id INTEGER,
                event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                message TEXT
            )
        ''')
        conn.commit()
        # Add flexible params column if missing
        try:
            cols = pd.read_sql_query("PRAGMA table_info(alerts)", conn)
            if 'params' not in cols['name'].tolist():
                conn.execute("ALTER TABLE alerts ADD COLUMN params TEXT")
                conn.commit()
        except Exception:
            pass
        
        with st.expander("➕ Create Price Target Alert", expanded=False):
            with st.form("price_alert_form"):
                symbol = st.selectbox("Stock", options=list(STOCK_SYMBOLS.keys()), format_func=lambda x: f"{STOCK_SYMBOLS[x]} ({x})")
                direction = st.selectbox("Direction", options=["above", "below"])
                target = st.number_input("Target Price (₹)", min_value=0.0, step=0.5, format="%.2f")
                submitted = st.form_submit_button("Create Price Alert")
                if submitted and symbol and target > 0:
                    cursor.execute('''
                        INSERT INTO alerts (type, symbol, direction, target_price, enabled)
                        VALUES ('PRICE', ?, ?, ?, 1)
                    ''', (symbol, direction, float(target)))
                    conn.commit()
                    st.success("✅ Price alert created")
        
        with st.expander("➕ Create News Keyword Alert", expanded=False):
            with st.form("news_alert_form"):
                keyword = st.text_input("Keyword")
                submitted = st.form_submit_button("Create News Alert")
                if submitted and keyword:
                    cursor.execute('''
                        INSERT INTO alerts (type, keyword, enabled)
                        VALUES ('NEWS', ?, 1)
                    ''', (keyword,))
                    conn.commit()
                    st.success("✅ News alert created")
        
        with st.expander("➕ Create Portfolio P&L Alert", expanded=False):
            with st.form("portfolio_alert_form"):
                direction = st.selectbox("Direction", options=["above", "below"], key="pdir")
                threshold = st.number_input("P&L % Threshold", step=0.5, format="%.2f")
                submitted = st.form_submit_button("Create Portfolio Alert")
                if submitted:
                    cursor.execute('''
                        INSERT INTO alerts (type, direction, threshold, enabled)
                        VALUES ('PORTFOLIO', ?, ?, 1)
                    ''', (direction, float(threshold)))
                    conn.commit()
                    st.success("✅ Portfolio alert created")
        
        with st.expander("➕ Create IPO Listing Alert", expanded=False):
            if st.button("Create Today's IPO Listing Alert"):
                cursor.execute('''
                    INSERT INTO alerts (type, enabled)
                    VALUES ('IPO_LISTING', 1)
                ''')
                conn.commit()
                st.success("✅ IPO listing alert created")
        
        with st.expander("➕ Create Trailing Stop Alert (Advanced)", expanded=False):
            with st.form("trail_alert_form"):
                symbol_t = st.selectbox("Stock", options=list(STOCK_SYMBOLS.keys()), key="trail_sym", format_func=lambda x: f"{STOCK_SYMBOLS[x]} ({x})")
                trail_pct = st.number_input("Trailing % below recent high", min_value=1.0, max_value=50.0, step=0.5, value=12.0, format="%.1f")
                submitted = st.form_submit_button("Create Trailing Stop Alert")
                if submitted and symbol_t:
                    params = json.dumps({"trailing_pct": float(trail_pct)})
                    cursor.execute('''
                        INSERT INTO alerts (type, symbol, params, enabled)
                        VALUES ('TRAIL', ?, ?, 1)
                    ''', (symbol_t, params))
                    conn.commit()
                    st.success("✅ Trailing stop alert created")
        
        st.subheader("Active Alerts")
        alerts_df = pd.read_sql_query("SELECT * FROM alerts ORDER BY created_at DESC", conn)
        if not alerts_df.empty:
            st.dataframe(alerts_df, use_container_width=True)
            delete_id = st.number_input("Delete alert by ID", min_value=0, step=1, value=0)
            if st.button("Delete Alert") and delete_id > 0:
                conn.execute("DELETE FROM alerts WHERE id = ?", (int(delete_id),))
                conn.commit()
                st.success("✅ Alert deleted")
        else:
            st.info("No alerts created yet.")
        
        if st.button("Check Alerts Now"):
            triggered = 0
            alerts = pd.read_sql_query("SELECT * FROM alerts WHERE enabled = 1", conn)
            for _, alert in alerts.iterrows():
                if alert['type'] == 'PRICE' and alert['symbol'] and alert['target_price']:
                    price_df = pd.read_sql_query('''
                        SELECT close FROM stock_prices WHERE symbol = ? ORDER BY date DESC LIMIT 1
                    ''', conn, params=(alert['symbol'],))
                    if not price_df.empty:
                        latest = float(price_df.iloc[0]['close'])
                        cond = (alert['direction']=='above' and latest >= alert['target_price']) or (alert['direction']=='below' and latest <= alert['target_price'])
                        if cond:
                            msg = f"{alert['symbol']} is {alert['direction']} ₹{alert['target_price']:.2f} (last ₹{latest:.2f})"
                            conn.execute("INSERT INTO alert_events (alert_id, message) VALUES (?, ?)", (int(alert['id']), msg))
                            triggered += 1
                elif alert['type'] == 'TRAIL' and alert['symbol']:
                    try:
                        params = json.loads(alert['params']) if alert['params'] else {}
                        tpct = float(params.get('trailing_pct', 12.0))
                        # Use 30‑day high as proxy for recent high
                        hist = pd.read_sql_query('''
                            SELECT close FROM stock_prices WHERE symbol = ? ORDER BY date DESC LIMIT 30
                        ''', conn, params=(alert['symbol'],))
                        if not hist.empty:
                            recent_high = float(hist['close'].max())
                            latest = float(hist['close'].iloc[0])
                            trigger = latest <= recent_high * (1 - tpct/100.0)
                            if trigger:
                                msg = f"{alert['symbol']} fell {tpct}% from recent high (₹{recent_high:.2f} → ₹{latest:.2f})"
                                conn.execute("INSERT INTO alert_events (alert_id, message) VALUES (?, ?)", (int(alert['id']), msg))
                                triggered += 1
                    except Exception:
                        pass
                elif alert['type'] == 'NEWS' and alert['keyword']:
                    news = pd.read_sql_query('''
                        SELECT title FROM news_articles 
                        WHERE (title LIKE ? OR description LIKE ?)
                        AND published_at >= datetime('now', '-1 day')
                        ORDER BY published_at DESC LIMIT 5
                    ''', conn, params=(f"%{alert['keyword']}%", f"%{alert['keyword']}%"))
                    if not news.empty:
                        msg = f"News matches keyword '{alert['keyword']}': {news.iloc[0]['title'][:80]}"
                        conn.execute("INSERT INTO alert_events (alert_id, message) VALUES (?, ?)", (int(alert['id']), msg))
                        triggered += 1
                elif alert['type'] == 'PORTFOLIO' and alert['threshold'] is not None:
                    holdings = pd.read_sql_query("SELECT symbol, quantity, buy_price FROM user_portfolio", conn)
                    if not holdings.empty:
                        total_inv = 0.0
                        total_val = 0.0
                        for _, h in holdings.iterrows():
                            price_df = pd.read_sql_query('''
                                SELECT close FROM stock_prices WHERE symbol = ? ORDER BY date DESC LIMIT 1
                            ''', conn, params=(h['symbol'],))
                            if price_df.empty:
                                continue
                            latest = float(price_df.iloc[0]['close'])
                            total_inv += float(h['quantity']) * float(h['buy_price'])
                            total_val += float(h['quantity']) * latest
                        if total_inv > 0:
                            pnl_pct = ((total_val - total_inv) / total_inv) * 100
                            cond = (alert['direction']=='above' and pnl_pct >= alert['threshold']) or (alert['direction']=='below' and pnl_pct <= alert['threshold'])
                            if cond:
                                msg = f"Portfolio P&L {alert['direction']} {alert['threshold']}% (current {pnl_pct:.2f}%)"
                                conn.execute("INSERT INTO alert_events (alert_id, message) VALUES (?, ?)", (int(alert['id']), msg))
                                triggered += 1
                elif alert['type'] == 'IPO_LISTING':
                    ipos = pd.read_sql_query('''
                        SELECT company_name, symbol FROM ipo_data WHERE listing_date = date('now')
                    ''', conn)
                    if not ipos.empty:
                        msg = f"IPO listed today: {ipos.iloc[0]['company_name']} ({ipos.iloc[0]['symbol']})"
                        conn.execute("INSERT INTO alert_events (alert_id, message) VALUES (?, ?)", (int(alert['id']), msg))
                        triggered += 1
            conn.commit()
            if triggered > 0:
                st.success(f"✅ {triggered} alert(s) triggered")
            else:
                st.info("No alerts triggered right now.")
        
        st.subheader("Recent Alert Events")
        events_df = pd.read_sql_query("SELECT * FROM alert_events ORDER BY event_time DESC LIMIT 20", conn)
        if not events_df.empty:
            st.dataframe(events_df, use_container_width=True)
        else:
            st.info("No alert events yet.")
        
        conn.close()
    except Exception as e:
        st.error(f"Alert center error: {str(e)}")

def show_portfolio():
    st.header("💰 Portfolio Tracker")
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                quantity REAL NOT NULL,
                buy_price REAL NOT NULL,
                buy_date DATE,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        
        with st.expander("➕ Add Holding", expanded=True):
            with st.form("add_holding_form"):
                symbol = st.selectbox("Stock", options=list(STOCK_SYMBOLS.keys()), format_func=lambda x: f"{STOCK_SYMBOLS[x]} ({x})")
                quantity = st.number_input("Quantity", min_value=0.0, step=1.0, format="%.2f")
                buy_price = st.number_input("Buy Price (₹)", min_value=0.0, step=0.5, format="%.2f")
                buy_date = st.date_input("Buy Date")
                notes = st.text_input("Notes", value="")
                submitted = st.form_submit_button("Add To Portfolio")
                if submitted and symbol and quantity > 0 and buy_price > 0:
                    cursor.execute('''
                        INSERT INTO user_portfolio (symbol, quantity, buy_price, buy_date, notes)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (symbol, float(quantity), float(buy_price), str(buy_date), notes))
                    conn.commit()
                    st.success("✅ Holding added")
        
        df = pd.read_sql_query('''
            SELECT id, symbol, quantity, buy_price, buy_date, notes, created_at
            FROM user_portfolio
            ORDER BY created_at DESC
        ''', conn)
        
        if df.empty:
            st.info("No holdings yet. Add your first holding to start tracking in real-time.")
            conn.close()
            return
        
        latest_prices = {}
        refresh_all = st.checkbox("Refresh latest prices from internet (yfinance)", value=True)
        for sym in df['symbol'].unique():
            price_df = pd.read_sql_query('''
                SELECT close FROM stock_prices
                WHERE symbol = ?
                ORDER BY date DESC
                LIMIT 1
            ''', conn, params=(sym,))
            if not price_df.empty and not refresh_all:
                latest_prices[sym] = float(price_df.iloc[0]['close'])
            else:
                try:
                    import yfinance as yf
                    ticker = yf.Ticker(sym)
                    hist = ticker.history(period="5d")
                    if not hist.empty:
                        latest_prices[sym] = float(hist['Close'].iloc[-1])
                except Exception:
                    latest_prices[sym] = float(price_df.iloc[0]['close']) if not price_df.empty else None
        
        conn.close()
        
        df['current_price'] = df['symbol'].map(lambda s: latest_prices.get(s))
        df = df.dropna(subset=['current_price'])
        
        df['invested'] = df['quantity'] * df['buy_price']
        df['current_value'] = df['quantity'] * df['current_price']
        df['pnl'] = df['current_value'] - df['invested']
        df['pnl_pct'] = (df['pnl'] / df['invested']) * 100
        
        total_invested = float(df['invested'].sum())
        total_value = float(df['current_value'].sum())
        total_pnl = float(df['pnl'].sum())
        total_pnl_pct = (total_pnl / total_invested) * 100 if total_invested > 0 else 0.0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Invested", f"₹{total_invested:,.2f}")
        with col2:
            st.metric("Current Value", f"₹{total_value:,.2f}")
        with col3:
            st.metric("P&L", f"₹{total_pnl:,.2f}", f"{total_pnl_pct:.2f}%")
        with col4:
            st.metric("Holdings", len(df))
        
        display_df = df[['symbol', 'quantity', 'buy_price', 'current_price', 'invested', 'current_value', 'pnl', 'pnl_pct', 'buy_date', 'notes']].copy()
        display_df.columns = ['Symbol', 'Qty', 'Buy Price', 'Current Price', 'Invested', 'Current Value', 'P&L', 'P&L %', 'Buy Date', 'Notes']
        st.dataframe(display_df, use_container_width=True)
        
        try:
            import plotly.express as px
            alloc = df.groupby('symbol')['current_value'].sum().reset_index()
            alloc.columns = ['symbol', 'value']
            if not alloc.empty and alloc['value'].sum() > 0:
                fig = px.pie(alloc, names='symbol', values='value', title='Allocation by Current Value', hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
        except Exception:
            pass
        
        # Diversification insights (not all eggs in one basket)
        try:
            sector_map = globals().get('STOCK_SECTORS', {})
            df['Sector'] = df['symbol'].map(lambda s: sector_map.get(s, "Other"))
            sector_alloc = df.groupby('Sector')['current_value'].sum()
            weights = sector_alloc / sector_alloc.sum() if sector_alloc.sum() > 0 else sector_alloc
            hhi = float((weights**2).sum()) if not weights.empty else None
            dscore = (1 - hhi) * 100 if hhi is not None else None
            st.subheader("🧺 Diversification")
            if dscore is not None:
                st.metric("Diversification Score", f"{dscore:.1f}/100")
            st.bar_chart(weights)
            if dscore is not None and dscore < 60:
                st.info("Diversification is low. Consider adding sectors that are under‑represented to reduce risk.")
        except Exception:
            pass
        
        with st.expander("🗑️ Remove Holding"):
            try:
                conn = sqlite3.connect(DATABASE_PATH)
                holdings = pd.read_sql_query("SELECT id, symbol, quantity FROM user_portfolio ORDER BY created_at DESC", conn)
                conn.close()
                if not holdings.empty:
                    choice = st.selectbox("Select holding to remove", options=holdings['id'].tolist(), format_func=lambda x: f"{holdings[holdings['id']==x]['symbol'].iloc[0]} • {holdings[holdings['id']==x]['quantity'].iloc[0]}")
                    if st.button("Remove Selected"):
                        conn = sqlite3.connect(DATABASE_PATH)
                        conn.execute("DELETE FROM user_portfolio WHERE id = ?", (int(choice),))
                        conn.commit()
                        conn.close()
                        st.success("✅ Holding removed")
                else:
                    st.info("No holdings to remove.")
            except Exception as e:
                st.error(f"Delete error: {str(e)}")
        
        st.subheader("🛡️ Portfolio Risk Assessment")
        symbols = df['symbol'].tolist()
        values = df['current_value'].tolist()
        weight_sum = sum(values)
        weights = [v/weight_sum for v in values] if weight_sum > 0 else [1/len(values)]*len(values)
        
        try:
            risk_manager = InstitutionalRiskManager()
            risk = risk_manager.comprehensive_risk_assessment(symbols, weights)
            if risk:
                r1, r2, r3, r4 = st.columns(4)
                with r1:
                    st.metric("Volatility (Annual)", f"{risk['portfolio_volatility_annual']:.2f}%")
                with r2:
                    st.metric("Return (Annual)", f"{risk['portfolio_return_annual']:.2f}%")
                with r3:
                    st.metric("Max Drawdown", f"{risk['max_drawdown']:.2f}%")
                with r4:
                    st.metric("Sharpe Ratio", f"{risk['sharpe_ratio']}")
                st.info(f"Overall Risk Rating: {risk['overall_risk_rating']}")
        except Exception as e:
            st.warning(f"Risk assessment unavailable: {str(e)}")
        
        st.subheader("🎯 Recommendations")
        if st.button("Generate Stock Recommendations"):
            try:
                analyzer = ProfessionalFinancialAnalyzer()
                recs = []
                for sym in df['symbol'].unique():
                    m = analyzer.calculate_advanced_metrics(sym)
                    if m:
                        recs.append({
                            'Symbol': sym,
                            'Company': STOCK_SYMBOLS.get(sym, sym),
                            'Recommendation': m.get('recommendation', 'NEUTRAL'),
                            'Investment Grade': m.get('investment_grade', 'Not Rated'),
                            'Risk Rating': m.get('risk_rating', 'Unknown'),
                            'Confidence': f"{m.get('confidence_score', 0)}%"
                        })
                if recs:
                    st.dataframe(pd.DataFrame(recs), use_container_width=True)
            except Exception as e:
                st.warning(f"Recommendations unavailable: {str(e)}")
        
    except Exception as e:
        st.error(f"Portfolio error: {str(e)}")

def show_ai_assistant():
    st.header("🤖 AI Investment Assistant")
    st.info("Groq-powered AI to answer investment questions in simple language.")
    if 'ai_chat' not in st.session_state:
        st.session_state.ai_chat = []
    model = st.selectbox("Model", options=["llama3-8b-8192", "mixtral-8x7b-32768"], index=0)
    mode = st.selectbox("Mode", options=["Explain", "Recommend", "Summarize Portfolio"], index=0)
    user_query = st.text_input("Ask about stocks, IPOs, mutual funds, or risk:")

    # Preflight checks for better errors
    groq_ready = True
    if not GROQ_API_KEY or str(GROQ_API_KEY).strip() == "":
        st.error("AI key is missing. Please set GROQ_API_KEY in config.py.")
        groq_ready = False
    try:
        from groq import Groq  # noqa: F401
    except Exception:
        st.error("Groq SDK not found. Install with: pip install groq")
        groq_ready = False

    # Connectivity quick test
    if st.button("Test Connection"):
        if not groq_ready:
            st.warning("Groq is not ready yet. Fix the issues above and try again.")
        else:
            try:
                from groq import Groq
                client = Groq(api_key=GROQ_API_KEY)
                ping = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "Reply with a single word: PONG."},
                        {"role": "user", "content": "PING"}
                    ],
                    temperature=0.0,
                    max_tokens=5
                )
                out = ping.choices[0].message.content if ping and ping.choices else "(no content)"
                st.success(f"Connection OK. Model replied: {out}")
            except Exception as e:
                st.error(f"Connection failed: {e}")

    if st.button("Ask") and user_query:
        st.session_state.ai_chat.append({"role": "user", "content": user_query})
        if not groq_ready:
            st.session_state.ai_chat.append({"role": "assistant", "content": "AI is not configured yet. Please install groq SDK and set GROQ_API_KEY."})
        else:
            try:
                from groq import Groq
                client = Groq(api_key=GROQ_API_KEY)
                # Optional portfolio snapshot for context
                portfolio_context = ""
                try:
                    conn = sqlite3.connect(DATABASE_PATH)
                    dfp = pd.read_sql_query("SELECT symbol, quantity, buy_price FROM user_portfolio ORDER BY created_at DESC LIMIT 20", conn)
                    conn.close()
                    if not dfp.empty and mode == "Summarize Portfolio":
                        portfolio_context = "User portfolio (symbol, qty, buy): " + "; ".join([f"{r.symbol} {r.quantity} @ {r.buy_price}" for _, r in dfp.iterrows()])
                except Exception:
                    pass
                sys_prompt = (
                    "You are an investment assistant for Indian markets. "
                    "Answer clearly in simple words. Avoid jargon. "
                    f"Task mode: {mode}. "
                    "Never promise returns. Always include a brief risk note. "
                    + (f"Context: {portfolio_context}" if portfolio_context else "")
                )
                messages = [{"role": "system", "content": sys_prompt}] + st.session_state.ai_chat
                resp = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=600
                )
                answer = resp.choices[0].message.content if resp and resp.choices else "No response."
                st.session_state.ai_chat.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.session_state.ai_chat.append({"role": "assistant", "content": f"AI call failed: {e}"})
    for msg in st.session_state.ai_chat[-10:]:
        role = "You" if msg['role']=="user" else "AI"
        st.markdown(f"**{role}:** {msg['content']}")

def show_data_collection():
    st.header("⚙️ Data Collection Center")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Collect All Stock Data"):
            with st.spinner("Collecting data for all 20 stocks..."):
                st.session_state.data_collector.collect_all_stocks()
                st.success("✅ Stock data collection completed!")
    
    with col2:
        if st.button("📰 Collect News Data"):
            with st.spinner("Collecting news from all sources..."):
                st.session_state.data_collector.collect_news_data()
                st.success("✅ News data collection completed!")
    
    # Data status
    st.subheader("📊 Data Status")
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        
        # Count records
        stock_count = pd.read_sql_query("SELECT COUNT(*) as count FROM stock_prices", conn).iloc[0]['count']
        news_count = pd.read_sql_query("SELECT COUNT(*) as count FROM news_articles", conn).iloc[0]['count']
        
        conn.close()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Stock Records", f"{stock_count:,}")
        with col2:
            st.metric("News Articles", f"{news_count:,}")
        with col3:
            st.metric("Database Size", "Ready")
            
    except Exception as e:
        st.error(f"Database not initialized: {str(e)}")

def show_investment_tools():
    st.header("💰 Investment Tools")
    tab1, tab2, tab3 = st.tabs(["SIP Optimizer", "Index Funds Guide", "Rule‑Based MF Ideas"])
    with tab1:
        st.subheader("SIP Goal Planner (Simple)")
        goal = st.number_input("Target Amount (₹)", min_value=0.0, step=1000.0, value=1000000.0, format="%.2f")
        years = st.number_input("Years", min_value=1, step=1, value=10)
        exp_return = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.5, value=12.0)
        r = exp_return / 100 / 12
        n = years * 12
        if r > 0:
            sip = goal * r / ((1 + r)**n - 1)
        else:
            sip = goal / n
        st.metric("Suggested Monthly SIP", f"₹{sip:,.0f}")
        st.info("Tip: Increase SIP by 5–10% every year to reach the goal comfortably.")
    with tab2:
        st.subheader("Index Funds (Simple Guidance)")
        st.write("- For stability, consider Nifty 50 index funds.")
        st.write("- For growth flavor, consider Nifty Next 50 (more volatile).")
        st.write("- Use SIP in index funds during high volatility periods.")
    with tab3:
        st.subheader("Rule‑Based Mutual Fund Ideas (From Market Mood)")
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            srow = pd.read_sql_query("""
                SELECT AVG(sentiment_score) as avg_s FROM news_articles 
                WHERE published_at >= datetime('now','-7 day')
            """, conn).iloc[0]
            conn.close()
            avg_s = srow['avg_s'] if srow['avg_s'] is not None else 0.0
            if avg_s > 0.1:
                st.write("- Positive mood: Consider flexicap/large & midcap funds.")
            elif avg_s < -0.1:
                st.write("- Negative mood: Prefer large‑cap index funds and short‑duration debt funds.")
            else:
                st.write("- Mixed mood: Stick to diversified flexicap or large‑cap funds.")
        except Exception:
            st.write("- When data is unavailable, prefer diversified index funds for core allocation.")

def show_analytics():
    st.header("📈 Analytics & Visualization")
    tab1, tab2, tab3 = st.tabs(["Market Heat Map", "Correlation Matrix", "Performance Comparison"])
    with tab1:
        st.subheader("Sector Heat Map (Last 30 Trading Days)")
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            prices = pd.read_sql_query("""
                SELECT symbol, date, close FROM stock_prices 
                WHERE date >= date('now','-45 day')
            """, conn)
            conn.close()
            if not prices.empty:
                last = prices.sort_values(['symbol', 'date']).groupby('symbol').tail(30)
                returns = last.groupby('symbol').apply(lambda df: df['close'].iloc[-1]/df['close'].iloc[0]-1).reset_index()
                returns.columns = ['symbol', 'ret']
                sector_map = globals().get('STOCK_SECTORS', {})
                returns['Sector'] = returns['symbol'].map(lambda s: sector_map.get(s, "Other"))
                fig = px.treemap(returns, path=['Sector', 'symbol'], values='ret', color='ret', color_continuous_scale='RdYlGn')
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough recent price data.")
        except Exception as e:
            st.info("Heat map unavailable.")
    with tab2:
        st.subheader("Correlation Matrix (60‑Day Returns)")
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            prices = pd.read_sql_query("""
                SELECT symbol, date, close FROM stock_prices 
                WHERE date >= date('now','-90 day')
            """, conn)
            conn.close()
            if not prices.empty:
                pivot = prices.pivot_table(index='date', columns='symbol', values='close').dropna(axis=1, how='any')
                rets = pivot.pct_change().dropna()
                corr = rets.corr()
                fig = px.imshow(corr, color_continuous_scale='RdBu', origin='lower')
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough data for correlation.")
        except Exception:
            st.info("Correlation unavailable.")
    with tab3:
        st.subheader("Compare Multiple Stocks")
        try:
            sel = st.multiselect("Select symbols", options=list(STOCK_SYMBOLS.keys()))
            if sel:
                conn = sqlite3.connect(DATABASE_PATH)
                prices = pd.read_sql_query(f"""
                    SELECT symbol, date, close FROM stock_prices 
                    WHERE symbol IN ({','.join(['?']*len(sel))}) AND date >= date('now','-180 day')
                """, conn, params=sel)
                conn.close()
                if not prices.empty:
                    base = prices.sort_values(['symbol','date']).groupby('symbol').first().reset_index()[['symbol','close']]
                    prices = prices.merge(base, on='symbol', suffixes=('','_base'))
                    prices['norm'] = prices['close']/prices['close_base']*100
                    fig = px.line(prices, x='date', y='norm', color='symbol', labels={'norm':'Normalized (100=Start)'})
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.info("Comparison unavailable.")
if __name__ == "__main__":
    main()
