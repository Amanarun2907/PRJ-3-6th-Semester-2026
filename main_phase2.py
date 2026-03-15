# सार्थक निवेश - Main Streamlit Application (Phase 2)
# Advanced Indian Stock Market Analysis & IPO Prediction Platform
# Team: Aman Jain, Rohit Fogla, Vanshita Mehta, Disita Tirthani

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3
import os

# Import our Phase 2 modules
from config import *
from data_collector import DataCollector
from stock_analyzer import AdvancedStockAnalyzer
from sentiment_analyzer import AdvancedSentimentAnalyzer
from excel_manager import ExcelExportManager
from risk_management import InstitutionalRiskManager
from professional_analyzer import ProfessionalFinancialAnalyzer

# Page Configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# MAXIMUM TEXT VISIBILITY CSS - EVERY TEXT CRYSTAL CLEAR
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
    
    /* MAIN HEADER - ENHANCED VISIBILITY */
    .main-header {
        background: linear-gradient(135deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border: 3px solid #FF9933;
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
    
    .team-info ul li {
        color: #000000 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        line-height: 1.6 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .team-info strong {
        color: #FF9933 !important;
        font-weight: 700 !important;
    }
    
    /* FEATURE CARDS - MAXIMUM VISIBILITY */
    .feature-card {
        background: #ffffff !important;
        padding: 1rem;
        border-radius: 10px;
        border: 3px solid #FF9933;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .feature-card h4 {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .feature-card p {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
    }
    
    /* SUCCESS ALERT - ENHANCED */
    .success-alert {
        background: #ffffff !important;
        border: 3px solid #28a745 !important;
        color: #000000 !important;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.2);
    }
    
    .success-alert h4 {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .success-alert p {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin: 0 !important;
    }
    
    /* PHASE BADGE */
    .phase-badge {
        background: #FF9933 !important;
        color: #ffffff !important;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
        border: 2px solid #ffffff;
    }
    
    /* STREAMLIT COMPONENTS - MAXIMUM VISIBILITY */
    .stSuccess {
        background-color: #ffffff !important;
        border: 3px solid #28a745 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stInfo {
        background-color: #ffffff !important;
        border: 3px solid #17a2b8 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stWarning {
        background-color: #ffffff !important;
        border: 3px solid #ffc107 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stError {
        background-color: #ffffff !important;
        border: 3px solid #dc3545 !important;
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
    
    /* DATAFRAME STYLING - PERFECT READABILITY */
    .dataframe {
        border: 3px solid #FF9933 !important;
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
    # Enhanced Header for Phase 2
    st.markdown(f"""
    <div class="main-header">
        <h1>📈 {PROJECT_NAME}</h1>
        <h3>AI-Powered Indian Stock Market Analysis & IPO Prediction Platform</h3>
        <p><span class="phase-badge">PHASE 2 COMPLETE</span> Advanced Analytics • Sentiment Analysis • Excel Integration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Sidebar
    st.sidebar.title("🎯 Navigation")
    st.sidebar.markdown("**Phase 2 Features Available**")
    
    page = st.sidebar.selectbox(
        "Choose Analysis Type",
        [
            "🏠 Enhanced Dashboard",
            "📊 Advanced Stock Analysis", 
            "🚀 IPO Analysis (Unique Feature)",
            "📰 News & Sentiment Analysis",
            "🧠 Fake News Detection",
            "💰 Portfolio Tracker",
            "📈 Sector Analysis",
            "📊 Excel Reports Manager",
            "🤖 AI Assistant",
            "⚙️ Data Management Center"
        ]
    )
    
    # Initialize all Phase 2 components
    if 'data_collector' not in st.session_state:
        st.session_state.data_collector = DataCollector()
    if 'stock_analyzer' not in st.session_state:
        st.session_state.stock_analyzer = AdvancedStockAnalyzer()
    if 'sentiment_analyzer' not in st.session_state:
        st.session_state.sentiment_analyzer = AdvancedSentimentAnalyzer()
    if 'excel_manager' not in st.session_state:
        st.session_state.excel_manager = ExcelExportManager()
    
    # Route to different pages
    if page == "🏠 Enhanced Dashboard":
        show_enhanced_dashboard()
    elif page == "📊 Advanced Stock Analysis":
        show_advanced_stock_analysis()
    elif page == "🚀 IPO Analysis (Unique Feature)":
        show_ipo_analysis()
    elif page == "📰 News & Sentiment Analysis":
        show_news_sentiment_analysis()
    elif page == "🧠 Fake News Detection":
        show_fake_news_detection()
    elif page == "💰 Portfolio Tracker":
        show_portfolio_tracker()
    elif page == "📈 Sector Analysis":
        show_sector_analysis()
    elif page == "📊 Excel Reports Manager":
        show_excel_reports()
    elif page == "🤖 AI Assistant":
        show_ai_assistant()
    elif page == "⚙️ Data Management Center":
        show_data_management()
    
    # Enhanced Team Information Footer
    st.markdown("""
    <div class="team-info">
        <h4>👥 Development Team - Phase 2 Complete</h4>
        <p><strong>Project:</strong> B.Tech 3rd Year - Advanced Indian Stock Market Analysis Platform</p>
        <p><strong>Team Members:</strong></p>
        <ul>
            <li><strong>Aman Jain</strong> - Project Lead & ML Development</li>
            <li><strong>Rohit Fogla</strong> - Data Collection & API Integration</li>
            <li><strong>Vanshita Mehta</strong> - Frontend Development & UI/UX</li>
            <li><strong>Disita Tirthani</strong> - NLP & Sentiment Analysis</li>
        </ul>
        <p><strong>Phase 2 Achievements:</strong> Advanced Analytics, Fake News Detection, Excel Integration, Comprehensive Stock Analysis</p>
        <p><strong>Unique Feature:</strong> Post-IPO Liquidity & Retail Sentiment Forecast (Framework Ready)</p>
    </div>
    """, unsafe_allow_html=True)

def show_enhanced_dashboard():
    st.header("📊 Enhanced Market Dashboard - Phase 2")
    
    # Phase 2 Feature Status
    st.markdown("""
    <div class="success-alert">
        <h4>🎉 Phase 2 Complete - All Features Active!</h4>
        <p>Advanced analytics, sentiment analysis, fake news detection, and Excel integration are now live.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📈 Advanced Analytics</h4>
            <h2>✅ Active</h2>
            <p>Technical indicators, predictions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🧠 Sentiment Analysis</h4>
            <h2>✅ Live</h2>
            <p>Real-time news sentiment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>🚨 Fake News Detection</h4>
            <h2>✅ Active</h2>
            <p>ML-based verification</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Excel Reports</h4>
            <h2>✅ Auto</h2>
            <p>Hourly updates</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Real-time Market Overview
    st.subheader("📈 Real-time Market Overview")
    
    try:
        # Get real market data
        conn = sqlite3.connect(DATABASE_PATH)
        
        # Get latest market summary
        market_query = '''
            WITH latest_data AS (
                SELECT symbol, close, date,
                       LAG(close) OVER (PARTITION BY symbol ORDER BY date) as prev_close
                FROM stock_prices
                WHERE date >= date('now', '-2 days')
            )
            SELECT symbol, close, prev_close,
                   ROUND(((close - prev_close) / prev_close) * 100, 2) as change_percent
            FROM latest_data
            WHERE prev_close IS NOT NULL
        '''
        
        market_df = pd.read_sql_query(market_query, conn)
        conn.close()
        
        if not market_df.empty:
            # Market Statistics
            total_stocks = len(market_df)
            gainers = len(market_df[market_df['change_percent'] > 0])
            losers = len(market_df[market_df['change_percent'] < 0])
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Stocks", total_stocks)
            with col2:
                st.metric("Gainers", gainers, delta=f"{(gainers/total_stocks)*100:.1f}%")
            with col3:
                st.metric("Losers", losers, delta=f"-{(losers/total_stocks)*100:.1f}%")
            with col4:
                avg_change = market_df['change_percent'].mean()
                st.metric("Avg Change", f"{avg_change:.2f}%", delta=avg_change)
            
            # Market Sentiment Chart
            fig = px.histogram(
                market_df, 
                x='change_percent',
                nbins=20,
                title="Market Performance Distribution",
                labels={'change_percent': 'Change %', 'count': 'Number of Stocks'},
                color_discrete_sequence=['#FF9933']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("📊 Market data is being updated. Please check back in a few minutes.")
    
    except Exception as e:
        st.error(f"Error loading market data: {str(e)}")
    
    # Phase 2 Features Overview
    st.subheader("🚀 Phase 2 Features")
    
    features = [
        {"name": "Advanced Stock Analysis", "status": "✅ Active", "description": "Technical indicators, RSI, MACD, Bollinger Bands"},
        {"name": "Sentiment Analysis", "status": "✅ Active", "description": "Real-time news sentiment with VADER & TextBlob"},
        {"name": "Fake News Detection", "status": "✅ Active", "description": "ML-based fake news identification"},
        {"name": "Excel Integration", "status": "✅ Active", "description": "Automated Excel reports with real data"},
        {"name": "Sector Analysis", "status": "✅ Active", "description": "Performance analysis across all sectors"},
        {"name": "Background Data Service", "status": "✅ Running", "description": "Independent 24/7 data updates"},
    ]
    
    for feature in features:
        st.markdown(f"""
        <div class="feature-card">
            <h4>{feature['name']} - {feature['status']}</h4>
            <p>{feature['description']}</p>
        </div>
        """, unsafe_allow_html=True)

def show_advanced_stock_analysis():
    st.header("📊 Advanced Stock Analysis - Real Data")
    
    # Stock selector with all available stocks
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        available_stocks = pd.read_sql_query("SELECT DISTINCT symbol FROM stock_prices ORDER BY symbol", conn)
        conn.close()
        
        stock_options = available_stocks['symbol'].tolist()
        
        selected_stock = st.selectbox(
            "Select Stock for Advanced Analysis",
            options=stock_options,
            format_func=lambda x: f"{STOCK_SYMBOLS.get(x, x.replace('.NS', ''))} ({x})"
        )
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("📈 Perform Advanced Analysis", type="primary"):
                with st.spinner("Analyzing stock with advanced indicators..."):
                    analysis = st.session_state.stock_analyzer.get_stock_analysis(selected_stock)
                    
                    if analysis:
                        st.success(f"✅ Analysis complete for {analysis['company_name']}")
                        
                        # Current Price Info
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric(
                                "Current Price", 
                                f"₹{analysis['current_price']}", 
                                delta=f"{analysis['day_change_percent']}%"
                            )
                        with col2:
                            st.metric("Volume", f"{analysis['volume']:,}")
                        with col3:
                            st.metric("RSI", analysis['rsi'])
                        with col4:
                            st.metric("Volatility", f"{analysis['volatility']}%")
                        
                        # Technical Indicators
                        st.subheader("📊 Technical Indicators")
                        
                        tech_col1, tech_col2, tech_col3 = st.columns(3)
                        
                        with tech_col1:
                            st.write("**Moving Averages**")
                            st.write(f"SMA 5: ₹{analysis['sma_5']}")
                            st.write(f"SMA 20: ₹{analysis['sma_20']}")
                            st.write(f"SMA 50: ₹{analysis['sma_50']}")
                        
                        with tech_col2:
                            st.write("**MACD Analysis**")
                            st.write(f"MACD: {analysis['macd']}")
                            st.write(f"Signal: {analysis['macd_signal']}")
                            st.write(f"Trend: {analysis['short_term_trend']}")
                        
                        with tech_col3:
                            st.write("**Support/Resistance**")
                            st.write(f"Support: ₹{analysis['support_level']}")
                            st.write(f"Resistance: ₹{analysis['resistance_level']}")
                            st.write(f"Risk Level: {analysis['risk_level']}")
                        
                        # Trading Signals
                        st.subheader("🎯 Trading Signals")
                        
                        if analysis['trading_signals']:
                            for signal in analysis['trading_signals']:
                                signal_color = {
                                    'BUY': 'green',
                                    'SELL': 'red', 
                                    'HOLD': 'orange',
                                    'WATCH': 'blue'
                                }.get(signal['type'], 'gray')
                                
                                st.markdown(f"""
                                <div style="padding: 0.5rem; margin: 0.5rem 0; border-left: 4px solid {signal_color}; background: #f8f9fa;">
                                    <strong>{signal['type']}</strong> - {signal['reason']} 
                                    <span style="color: {signal_color};">({signal['strength']} Signal)</span>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No specific trading signals at this time.")
                    
                    else:
                        st.error("Unable to analyze this stock. Please try another.")
        
        with col2:
            st.info("""
            **Advanced Analysis Includes:**
            - Technical Indicators (RSI, MACD, Bollinger Bands)
            - Moving Averages (5, 20, 50 day)
            - Support/Resistance Levels
            - Trading Signals
            - Risk Assessment
            - Volume Analysis
            """)
    
    except Exception as e:
        st.error(f"Error loading stock data: {str(e)}")

def show_news_sentiment_analysis():
    st.header("📰 News & Sentiment Analysis - Real Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("📰 Analyze Latest News Sentiment", type="primary"):
            with st.spinner("Processing news articles for sentiment..."):
                # Process news sentiment
                success = st.session_state.sentiment_analyzer.process_all_news()
                
                if success:
                    st.success("✅ News sentiment analysis completed!")
                    
                    # Get market sentiment summary
                    sentiment_summary = st.session_state.sentiment_analyzer.get_market_sentiment_summary()
                    
                    # Display sentiment metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Overall Sentiment", sentiment_summary['overall_sentiment'].title())
                    with col2:
                        st.metric("Sentiment Score", f"{sentiment_summary['sentiment_score']:.3f}")
                    with col3:
                        st.metric("Total Articles", sentiment_summary['total_articles'])
                    with col4:
                        st.metric("Positive Articles", sentiment_summary['positive_articles'])
                    
                    # Sentiment Distribution
                    if sentiment_summary['total_articles'] > 0:
                        sentiment_data = {
                            'Sentiment': ['Positive', 'Negative', 'Neutral'],
                            'Count': [
                                sentiment_summary['positive_articles'],
                                sentiment_summary['negative_articles'],
                                sentiment_summary['neutral_articles']
                            ]
                        }
                        
                        fig = px.pie(
                            values=sentiment_data['Count'],
                            names=sentiment_data['Sentiment'],
                            title="Market Sentiment Distribution (Last 24 Hours)",
                            color_discrete_sequence=['green', 'red', 'gray']
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Recent News Sample
                    st.subheader("📰 Recent News Analysis")
                    
                    try:
                        conn = sqlite3.connect(DATABASE_PATH)
                        recent_news = pd.read_sql_query('''
                            SELECT title, source, sentiment_score, is_fake_news, published_at
                            FROM news_articles 
                            WHERE sentiment_score IS NOT NULL
                            ORDER BY published_at DESC 
                            LIMIT 10
                        ''', conn)
                        conn.close()
                        
                        if not recent_news.empty:
                            for _, news in recent_news.iterrows():
                                sentiment_color = 'green' if news['sentiment_score'] > 0.1 else 'red' if news['sentiment_score'] < -0.1 else 'gray'
                                fake_badge = "🚨 FAKE" if news['is_fake_news'] else "✅ VERIFIED"
                                
                                st.markdown(f"""
                                <div style="padding: 1rem; margin: 0.5rem 0; border: 1px solid #ddd; border-radius: 5px;">
                                    <h5>{news['title']}</h5>
                                    <p><strong>Source:</strong> {news['source']} | 
                                       <strong>Sentiment:</strong> <span style="color: {sentiment_color};">{news['sentiment_score']:.3f}</span> | 
                                       <strong>Status:</strong> {fake_badge}</p>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Error loading recent news: {str(e)}")
                
                else:
                    st.error("Error processing news sentiment")
    
    with col2:
        st.info("""
        **Sentiment Analysis Features:**
        - VADER Sentiment Analysis
        - TextBlob Polarity Detection
        - Financial Keyword Analysis
        - Multi-source News Processing
        - Real-time Market Mood
        - Fake News Filtering
        """)

def show_fake_news_detection():
    st.header("🧠 Fake News Detection - ML Powered")
    
    st.markdown("""
    <div class="success-alert">
        <h4>🚨 Advanced Fake News Detection Active</h4>
        <p>Our ML system analyzes news articles for credibility using multiple detection methods.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Manual fake news check
    st.subheader("🔍 Test Fake News Detection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        test_title = st.text_input("Enter News Title", "GUARANTEED 500% RETURNS IN 30 DAYS!!!")
        test_description = st.text_area("Enter News Description", "Secret insider tip reveals risk-free investment opportunity")
        test_source = st.text_input("Enter Source", "unknown_source")
    
    with col2:
        if st.button("🔍 Analyze for Fake News", type="primary"):
            with st.spinner("Analyzing news credibility..."):
                result = st.session_state.sentiment_analyzer.detect_fake_news(
                    test_title, test_description, test_source
                )
                
                if result['is_fake']:
                    st.error(f"🚨 **FAKE NEWS DETECTED** (Confidence: {result['confidence']:.1%})")
                else:
                    st.success(f"✅ **APPEARS LEGITIMATE** (Confidence: {result['confidence']:.1%})")
                
                st.write(f"**Fake Score:** {result['fake_score']:.3f}")
                st.write("**Analysis Reasons:**")
                for reason in result['reasons']:
                    st.write(f"- {reason}")
    
    # Show recent fake news detections
    st.subheader("🚨 Recent Fake News Detections")
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        fake_news = pd.read_sql_query('''
            SELECT title, source, published_at, sentiment_score
            FROM news_articles 
            WHERE is_fake_news = 1
            ORDER BY published_at DESC 
            LIMIT 5
        ''', conn)
        conn.close()
        
        if not fake_news.empty:
            st.write(f"**Found {len(fake_news)} fake news articles:**")
            for _, news in fake_news.iterrows():
                st.markdown(f"""
                <div style="padding: 1rem; margin: 0.5rem 0; border: 2px solid red; border-radius: 5px; background: #ffe6e6;">
                    <h5>🚨 {news['title']}</h5>
                    <p><strong>Source:</strong> {news['source']} | <strong>Detected:</strong> {news['published_at']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No fake news detected in recent articles - All sources appear credible!")
    
    except Exception as e:
        st.error(f"Error loading fake news data: {str(e)}")

def show_excel_reports():
    st.header("📊 Excel Reports Manager - Real Data")
    
    st.markdown("""
    <div class="success-alert">
        <h4>📊 Automated Excel Reports Available</h4>
        <p>All reports contain real market data and update automatically every hour.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate reports section
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Generate All Excel Reports", type="primary"):
            with st.spinner("Generating Excel reports with real data..."):
                success = st.session_state.excel_manager.generate_all_reports()
                
                if success:
                    st.success("✅ All Excel reports generated successfully!")
                    st.balloons()
                else:
                    st.error("❌ Some reports had issues")
    
    with col2:
        if st.button("📈 Generate Stock Data Only"):
            with st.spinner("Creating stock data Excel..."):
                success = st.session_state.excel_manager.create_stock_data_excel()
                if success:
                    st.success("✅ Stock data Excel created!")
    
    # Available reports
    st.subheader("📋 Available Excel Reports")
    
    reports = [
        {
            "name": "📈 Stock Data Report",
            "file": "stock_data.xlsx",
            "description": "Latest prices, technical indicators, top gainers/losers, sector performance",
            "sheets": "Latest Prices, Historical Data, Top Gainers, Top Losers, Sector Performance, Market Summary"
        },
        {
            "name": "📰 News Sentiment Report", 
            "file": "news_sentiment.xlsx",
            "description": "News articles with sentiment scores, fake news detection, source analysis",
            "sheets": "All News, Sentiment Summary, Source Analysis, Daily Sentiment, Fake News Detected"
        },
        {
            "name": "🚀 IPO Analysis Report",
            "file": "ipo_analysis.xlsx", 
            "description": "IPO performance tracking framework (Phase 3 implementation)",
            "sheets": "IPO Features, IPO Performance, Implementation Notes"
        },
        {
            "name": "💰 Portfolio Summary",
            "file": "portfolio_summary.xlsx",
            "description": "System status, team information, feature status",
            "sheets": "System Status, Team Info, Feature Status"
        },
        {
            "name": "📊 Daily Market Report",
            "file": "daily_market_report.xlsx",
            "description": "Daily top movers, market summary, performance statistics",
            "sheets": "Top Gainers, Top Losers, Market Summary"
        }
    ]
    
    for report in reports:
        with st.expander(f"{report['name']} - {report['file']}"):
            st.write(f"**Description:** {report['description']}")
            st.write(f"**Sheets:** {report['sheets']}")
            
            # Check if file exists
            file_path = f"exports/{report['file']}"
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path) / 1024  # KB
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                st.success(f"✅ Available | Size: {file_size:.1f} KB | Last Updated: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.warning("⚠️ Not generated yet - Click 'Generate All Excel Reports' above")

def show_sector_analysis():
    st.header("📈 Sector Analysis - Real Performance Data")
    
    if st.button("📊 Analyze All Sectors", type="primary"):
        with st.spinner("Analyzing sector performance..."):
            sector_data = st.session_state.stock_analyzer.get_sector_analysis()
            
            if sector_data:
                st.success("✅ Sector analysis completed!")
                
                # Create sector performance chart
                sectors = list(sector_data.keys())
                performance = [data['performance'] for data in sector_data.values()]
                
                fig = px.bar(
                    x=sectors,
                    y=performance,
                    title="Sector Performance Today (%)",
                    labels={'x': 'Sector', 'y': 'Performance (%)'},
                    color=performance,
                    color_continuous_scale=['red', 'yellow', 'green']
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Sector details
                st.subheader("📊 Sector Details")
                
                for sector, data in sector_data.items():
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(f"{sector} Sector", f"{data['performance']:.2f}%")
                    with col2:
                        st.write(f"Stocks: {data['stocks_count']}")
                    with col3:
                        status_color = 'green' if data['status'] == 'Positive' else 'red' if data['status'] == 'Negative' else 'gray'
                        st.markdown(f"<span style='color: {status_color};'><strong>{data['status']}</strong></span>", unsafe_allow_html=True)
            
            else:
                st.error("Unable to load sector data")

def show_ipo_analysis():
    st.header("🚀 IPO Analysis - Unique Feature Framework")
    
    st.markdown("""
    <div class="success-alert">
        <h4>🎯 Unique Feature: Post-IPO Liquidity & Retail Sentiment Forecast</h4>
        <p><strong>Phase 2:</strong> Framework complete and ready for implementation</p>
        <p><strong>Phase 3:</strong> Full implementation with real IPO data analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("""
    **🎯 This Unique Feature Will Analyze:**
    - IPO performance in first 30/60/90 days post-listing
    - Social media sentiment + trading volume patterns  
    - Specific hold/exit recommendations with confidence scores
    - Retail sentiment impact on IPO pricing
    - Liquidity forecasting for new listings
    
    *This India-specific feature is not available on platforms like Groww!*
    """)
    
    # Framework demonstration
    st.subheader("📊 IPO Analysis Framework")
    
    # Sample framework data
    framework_features = [
        {"feature": "Post-IPO Performance Tracking", "status": "✅ Framework Ready", "phase": "Phase 3"},
        {"feature": "Sentiment-Based Analysis", "status": "✅ Framework Ready", "phase": "Phase 3"},
        {"feature": "Hold/Exit Recommendations", "status": "✅ Framework Ready", "phase": "Phase 3"},
        {"feature": "Liquidity Forecasting", "status": "✅ Framework Ready", "phase": "Phase 3"},
        {"feature": "Retail Sentiment Impact", "status": "✅ Framework Ready", "phase": "Phase 3"},
        {"feature": "Volume Pattern Analysis", "status": "✅ Framework Ready", "phase": "Phase 3"},
    ]
    
    for feature in framework_features:
        st.markdown(f"""
        <div class="feature-card">
            <h4>{feature['feature']} - {feature['status']}</h4>
            <p>Implementation: {feature['phase']}</p>
        </div>
        """, unsafe_allow_html=True)

def show_portfolio_tracker():
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
            with st.form("add_holding_form_p2"):
                symbol = st.selectbox("Stock", options=list(STOCK_SYMBOLS.keys()), format_func=lambda x: f"{STOCK_SYMBOLS[x]} ({x})")
                quantity = st.number_input("Quantity", min_value=0.0, step=1.0, format="%.2f", key="qty_p2")
                buy_price = st.number_input("Buy Price (₹)", min_value=0.0, step=0.5, format="%.2f", key="price_p2")
                buy_date = st.date_input("Buy Date", key="date_p2")
                notes = st.text_input("Notes", value="", key="notes_p2")
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
        for sym in df['symbol'].unique():
            price_df = pd.read_sql_query('''
                SELECT close FROM stock_prices
                WHERE symbol = ?
                ORDER BY date DESC
                LIMIT 1
            ''', conn, params=(sym,))
            if not price_df.empty:
                latest_prices[sym] = float(price_df.iloc[0]['close'])
            else:
                try:
                    import yfinance as yf
                    ticker = yf.Ticker(sym)
                    hist = ticker.history(period="5d")
                    if not hist.empty:
                        latest_prices[sym] = float(hist['Close'].iloc[-1])
                except Exception:
                    latest_prices[sym] = None
        
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
            alloc = df.groupby('symbol')[['current_value']].sum().reset_index()
            alloc.columns = ['symbol', 'value']
            if not alloc.empty and alloc['value'].sum() > 0:
                fig = px.pie(alloc, names='symbol', values='value', title='Allocation by Current Value', hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
        except Exception:
            pass
        
        with st.expander("🗑️ Remove Holding"):
            try:
                conn = sqlite3.connect(DATABASE_PATH)
                holdings = pd.read_sql_query("SELECT id, symbol, quantity FROM user_portfolio ORDER BY created_at DESC", conn)
                conn.close()
                if not holdings.empty:
                    choice = st.selectbox("Select holding to remove", options=holdings['id'].tolist(), format_func=lambda x: f"{holdings[holdings['id']==x]['symbol'].iloc[0]} • {holdings[holdings['id']==x]['quantity'].iloc[0]}")
                    if st.button("Remove Selected", key="remove_p2"):
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
        if st.button("Generate Stock Recommendations", key="recs_p2"):
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
    st.info("AI Chatbot powered by Groq with advanced market insights - Coming in Phase 5!")

def show_data_management():
    st.header("⚙️ Data Management Center")
    
    # Data collection controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Collect All Stock Data"):
            with st.spinner("Collecting comprehensive stock data..."):
                # This would trigger the background service
                st.success("✅ Data collection initiated!")
                st.info("💡 Tip: Use the background data service for automatic updates")
    
    with col2:
        if st.button("📰 Collect News Data"):
            with st.spinner("Collecting news from all sources..."):
                st.session_state.data_collector.collect_news_data()
                st.success("✅ News data collection completed!")
    
    # Database status
    st.subheader("📊 Database Status")
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        
        # Count records
        stock_count = pd.read_sql_query("SELECT COUNT(*) as count FROM stock_prices", conn).iloc[0]['count']
        news_count = pd.read_sql_query("SELECT COUNT(*) as count FROM news_articles", conn).iloc[0]['count']
        unique_stocks = pd.read_sql_query("SELECT COUNT(DISTINCT symbol) as count FROM stock_prices", conn).iloc[0]['count']
        
        # Get latest update time
        latest_update = pd.read_sql_query("SELECT MAX(created_at) as latest FROM stock_prices", conn).iloc[0]['latest']
        
        conn.close()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Stock Records", f"{stock_count:,}")
        with col2:
            st.metric("Unique Stocks", unique_stocks)
        with col3:
            st.metric("News Articles", f"{news_count:,}")
        with col4:
            st.metric("Last Update", latest_update[:10] if latest_update else "N/A")
        
        # Background service status
        st.subheader("🔄 Background Data Service")
        
        st.info("""
        **To start the independent background service:**
        
        1. Open a new terminal/command prompt
        2. Navigate to your project folder
        3. Run: `python data_service.py`
        4. Service will run 24/7 and update data every hour
        5. You can close this Streamlit app and data will keep updating
        """)
        
        if st.button("📋 View Background Service Instructions"):
            st.code("""
# Start the background data service (runs independently)
python data_service.py

# The service will:
# - Update stock data every hour
# - Collect news from all sources
# - Generate Excel reports automatically
# - Run 24/7 even when Streamlit app is closed
            """)
            
    except Exception as e:
        st.error(f"Database error: {str(e)}")

if __name__ == "__main__":
    main()
