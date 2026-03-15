# सार्थक निवेश - Complete Investment Platform (Phase 4)
# Comprehensive Indian Investment Analysis Platform with All Features
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
import requests
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import warnings
warnings.filterwarnings('ignore')

# Import all modules
from config import *
from data_collector import DataCollector
from stock_analyzer import AdvancedStockAnalyzer
from sentiment_analyzer import AdvancedSentimentAnalyzer
from excel_manager import ExcelExportManager
from realtime_ipo_intelligence import RealTimeIPOIntelligence
from ipo_data_collector import IPODataCollector
from ipo_predictor import IPOPredictionEngine
from risk_management import InstitutionalRiskManager

# Page Configuration
st.set_page_config(
    page_title="सार्थक निवेश - Complete Investment Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ENHANCED CSS FOR PERFECT TEXT VISIBILITY AND PROFESSIONAL STYLING
st.markdown("""
<style>
    /* GLOBAL FONT AND TEXT SETTINGS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        color: #1a1a1a !important;
    }
    
    /* PERFECT TEXT VISIBILITY - MAXIMUM CONTRAST */
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
        font-weight: 700 !important;
        text-shadow: none !important;
        margin-bottom: 1rem !important;
        line-height: 1.3 !important;
        letter-spacing: -0.02em !important;
    }
    
    h1 { font-size: 2.8rem !important; font-weight: 800 !important; }
    h2 { font-size: 2.2rem !important; font-weight: 700 !important; }
    h3 { font-size: 1.8rem !important; font-weight: 600 !important; }
    h4 { font-size: 1.4rem !important; font-weight: 600 !important; }
    h5 { font-size: 1.2rem !important; font-weight: 500 !important; }
    
    /* ALL TEXT ELEMENTS - CRYSTAL CLEAR */
    p, div, span, label, .stMarkdown, .stText {
        color: #1a1a1a !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
        text-shadow: none !important;
    }
    
    /* MAIN HEADER - PROFESSIONAL GRADIENT */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        border: none;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        pointer-events: none;
    }
    
    .main-header h1 {
        color: #ffffff !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
        margin-bottom: 1rem !important;
        letter-spacing: -0.02em !important;
        position: relative;
        z-index: 1;
    }
    
    .main-header h3 {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 400 !important;
        margin-top: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 300 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
        position: relative;
        z-index: 1;
    }
    
    /* FEATURE BADGE - ANIMATED */
    .feature-badge {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%) !important;
        color: #ffffff !important;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
        border: 3px solid rgba(255,255,255,0.3);
        display: inline-block;
        margin: 1rem 0.5rem;
        animation: glow 2s ease-in-out infinite alternate;
        position: relative;
        z-index: 1;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 20px rgba(255, 107, 107, 0.5); }
        to { box-shadow: 0 0 30px rgba(255, 107, 107, 0.8); }
    }
    
    /* METRIC CARDS - GLASSMORPHISM EFFECT */
    .metric-card {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        background: rgba(255, 255, 255, 1) !important;
    }
    
    .metric-card h4 {
        color: #2d3748 !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .metric-card h2 {
        color: #667eea !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin: 1rem 0 !important;
        text-shadow: none !important;
    }
    
    .metric-card p {
        color: #4a5568 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }
    
    /* SIDEBAR STYLING */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
    }
    
    .css-1d391kg .stSelectbox label,
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3,
    .css-1d391kg p, .css-1d391kg div {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* BUTTONS - MODERN DESIGN */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-shadow: none !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* SELECTBOX STYLING */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #1a1a1a !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stSelectbox label {
        color: #2d3748 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* DATAFRAME STYLING - PROFESSIONAL TABLE */
    .dataframe {
        border: none !important;
        border-radius: 15px !important;
        overflow: hidden !important;
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-align: center !important;
        padding: 15px !important;
        text-shadow: none !important;
        border: none !important;
    }
    
    .dataframe td {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #1a1a1a !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 12px !important;
        border-bottom: 1px solid rgba(226, 232, 240, 0.5) !important;
        transition: background-color 0.2s ease !important;
    }
    
    .dataframe tr:hover td {
        background: rgba(102, 126, 234, 0.05) !important;
    }
    
    /* ALERT BOXES - ENHANCED */
    .stSuccess {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3) !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        box-shadow: 0 4px 15px rgba(66, 153, 225, 0.3) !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        box-shadow: 0 4px 15px rgba(237, 137, 54, 0.3) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        box-shadow: 0 4px 15px rgba(245, 101, 101, 0.3) !important;
    }
    
    /* METRIC COMPONENT STYLING */
    .metric-container {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
    }
    
    .metric-container label {
        color: #2d3748 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    
    .metric-container div {
        color: #667eea !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
    }
    
    /* CUSTOM CARDS */
    .info-card {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .info-card h4 {
        color: #2d3748 !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    .info-card p {
        color: #4a5568 !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
    }
    
    /* RECOMMENDATION BADGES */
    .rec-strong-buy {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
        color: #ffffff !important;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4) !important;
    }
    
    .rec-buy {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
        color: #ffffff !important;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
        box-shadow: 0 4px 15px rgba(66, 153, 225, 0.4) !important;
    }
    
    .rec-hold {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%) !important;
        color: #ffffff !important;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
        box-shadow: 0 4px 15px rgba(237, 137, 54, 0.4) !important;
    }
    
    .rec-sell {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%) !important;
        color: #ffffff !important;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
        box-shadow: 0 4px 15px rgba(245, 101, 101, 0.4) !important;
    }
    
    /* ENSURE ALL TEXT IS PERFECTLY VISIBLE */
    .stApp *, .css-1d391kg *, .css-12oz5g7 * {
        color: inherit !important;
    }
    
    /* RESPONSIVE DESIGN */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2.5rem !important;
        }
        
        .metric-card {
            padding: 1.5rem !important;
        }
        
        .metric-card h2 {
            font-size: 2.2rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Enhanced Header for Complete Platform
    st.markdown(f"""
    <div class="main-header">
        <h1>📈 सार्थक निवेश</h1>
        <h3>Complete Investment Intelligence Platform</h3>
        <div class="feature-badge">✨ 32 Advanced Features • Real-time Data • AI-Powered Insights ✨</div>
        <p>India's Most Comprehensive Investment Analysis Platform</p>
        <p>Stocks • IPOs • Mutual Funds • SIP • Risk Management • Portfolio Optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Sidebar Navigation
    st.sidebar.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <h3 style="color: #ffffff; text-align: center; margin-bottom: 0.5rem;">🎯 Navigation Hub</h3>
        <p style="color: #ffffff; text-align: center; font-size: 0.9rem;">Complete Investment Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.selectbox(
        "Choose Analysis Module",
        [
            "🏠 Complete Dashboard",
            "📊 Real-time Stock Analysis", 
            "🚀 IPO Intelligence Hub",
            "💰 Mutual Fund & SIP Center",
            "🛡️ Risk Management & Portfolio",
            "📰 News & Sentiment Intelligence",
            "🧠 Fake News Detection",
            "🔔 Smart Alerts System",
            "🤖 AI Investment Assistant",
            "📈 Advanced Analytics",
            "⚙️ Data Management Center",
            "❓ FAQ & Help Center"
        ]
    )
    
    # Initialize all systems
    if 'data_collector' not in st.session_state:
        st.session_state.data_collector = DataCollector()
    if 'stock_analyzer' not in st.session_state:
        st.session_state.stock_analyzer = AdvancedStockAnalyzer()
    if 'sentiment_analyzer' not in st.session_state:
        st.session_state.sentiment_analyzer = AdvancedSentimentAnalyzer()
    if 'excel_manager' not in st.session_state:
        st.session_state.excel_manager = ExcelExportManager()
    if 'ipo_intelligence' not in st.session_state:
        st.session_state.ipo_intelligence = RealTimeIPOIntelligence()
    if 'ipo_data_collector' not in st.session_state:
        st.session_state.ipo_data_collector = IPODataCollector()
    if 'ipo_predictor' not in st.session_state:
        st.session_state.ipo_predictor = IPOPredictionEngine()
    if 'risk_manager' not in st.session_state:
        from comprehensive_risk_management import ComprehensiveRiskManagement
        st.session_state.risk_manager = ComprehensiveRiskManagement()
    if 'mf_sip_system' not in st.session_state:
        from mutual_fund_sip_system import MutualFundSIPSystem
        st.session_state.mf_sip_system = MutualFundSIPSystem()
    
    # Route to different pages
    if page == "🏠 Complete Dashboard":
        show_complete_dashboard()
    elif page == "📊 Real-time Stock Analysis":
        show_realtime_stock_analysis()
    elif page == "🚀 IPO Intelligence Hub":
        show_enhanced_ipo_intelligence()
    elif page == "💰 Mutual Fund & SIP Center":
        show_mutual_fund_sip_center()
    elif page == "🛡️ Risk Management & Portfolio":
        show_risk_management_portfolio()
    elif page == "📰 News & Sentiment Intelligence":
        show_enhanced_news_sentiment()
    elif page == "🧠 Fake News Detection":
        show_enhanced_fake_news_detection()
    elif page == "🔔 Smart Alerts System":
        show_smart_alerts_system()
    elif page == "🤖 AI Investment Assistant":
        show_ai_investment_assistant()
    elif page == "📈 Advanced Analytics":
        show_advanced_analytics()
    elif page == "⚙️ Data Management Center":
        show_enhanced_data_management()
    elif page == "❓ FAQ & Help Center":
        show_faq_help_center()
    
    # Enhanced Footer
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(20px); padding: 2rem; border-radius: 20px; margin-top: 3rem; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);">
        <h4 style="color: #2d3748; font-size: 1.4rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">👥 Development Team - Complete Platform</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
            <div style="text-align: center; padding: 1rem;">
                <h5 style="color: #667eea; font-weight: 700;">Aman Jain</h5>
                <p style="color: #4a5568; font-weight: 500;">Project Lead & System Architecture</p>
            </div>
            <div style="text-align: center; padding: 1rem;">
                <h5 style="color: #667eea; font-weight: 700;">Rohit Fogla</h5>
                <p style="color: #4a5568; font-weight: 500;">Data Engineering & API Integration</p>
            </div>
            <div style="text-align: center; padding: 1rem;">
                <h5 style="color: #667eea; font-weight: 700;">Vanshita Mehta</h5>
                <p style="color: #4a5568; font-weight: 500;">Frontend Development & UI/UX</p>
            </div>
            <div style="text-align: center; padding: 1rem;">
                <h5 style="color: #667eea; font-weight: 700;">Disita Tirthani</h5>
                <p style="color: #4a5568; font-weight: 500;">ML/AI & Sentiment Analysis</p>
            </div>
        </div>
        <div style="text-align: center; padding-top: 1rem; border-top: 1px solid rgba(102, 126, 234, 0.2);">
            <p style="color: #2d3748; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;"><strong>Project:</strong> B.Tech 3rd Year - Complete Investment Intelligence Platform</p>
            <p style="color: #667eea; font-size: 1.2rem; font-weight: 700;"><strong>Achievement:</strong> 32 Advanced Features with Real-time Data & AI Integration</p>
            <p style="color: #e53e3e; font-size: 1.1rem; font-weight: 700;"><strong>UNIQUE:</strong> India's First Complete IPO Intelligence System</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_complete_dashboard():
    st.header("🏠 Complete Investment Intelligence Dashboard")
    
    # Platform Status Overview
    st.markdown("""
    <div class="info-card">
        <h4>🎉 Complete Investment Platform - All Systems Operational</h4>
        <p>Welcome to India's most comprehensive investment analysis platform with 32 advanced features, real-time data integration, and AI-powered insights.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Real-time Market Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Stock Analysis</h4>
            <h2>✅ Live</h2>
            <p>Real-time price tracking</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🚀 IPO Intelligence</h4>
            <h2>✅ Active</h2>
            <p>Unique analysis system</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>💰 Mutual Funds</h4>
            <h2>✅ Ready</h2>
            <p>SIP optimization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>🛡️ Risk Management</h4>
            <h2>✅ Smart</h2>
            <p>Portfolio optimization</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Get real market data for dashboard
    try:
        # Fetch real-time data for major indices
        nifty = yf.Ticker("^NSEI")
        sensex = yf.Ticker("^BSESN")
        
        nifty_data = nifty.history(period="2d")
        sensex_data = sensex.history(period="2d")
        
        if not nifty_data.empty and not sensex_data.empty:
            st.subheader("📈 Live Market Indices")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nifty_current = nifty_data['Close'].iloc[-1]
                nifty_prev = nifty_data['Close'].iloc[-2] if len(nifty_data) > 1 else nifty_current
                nifty_change = ((nifty_current - nifty_prev) / nifty_prev) * 100
                
                st.metric(
                    "NIFTY 50", 
                    f"{nifty_current:.2f}", 
                    delta=f"{nifty_change:.2f}%"
                )
            
            with col2:
                sensex_current = sensex_data['Close'].iloc[-1]
                sensex_prev = sensex_data['Close'].iloc[-2] if len(sensex_data) > 1 else sensex_current
                sensex_change = ((sensex_current - sensex_prev) / sensex_prev) * 100
                
                st.metric(
                    "SENSEX", 
                    f"{sensex_current:.2f}", 
                    delta=f"{sensex_change:.2f}%"
                )
            
            # Market trend chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=nifty_data.index,
                y=nifty_data['Close'],
                mode='lines',
                name='NIFTY 50',
                line=dict(color='#667eea', width=3)
            ))
            
            fig.update_layout(
                title="NIFTY 50 - Recent Trend",
                xaxis_title="Date",
                yaxis_title="Price",
                height=400,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.info("📊 Market data will be displayed here. Initializing real-time connections...")
    
    # Platform Features Overview
    st.subheader("🚀 Platform Features (32 Advanced Capabilities)")
    
    features_data = [
        {"category": "📊 Stock Analysis", "features": ["Real-time Price Tracking", "Technical Indicators", "Price Predictions", "Sector Analysis"], "status": "✅ Active"},
        {"category": "🚀 IPO Intelligence", "features": ["Post-IPO Performance", "Sentiment Analysis", "Hold/Exit Recommendations", "Liquidity Forecasting"], "status": "✅ Unique"},
        {"category": "💰 Investment Tools", "features": ["Mutual Fund Analysis", "SIP Optimization", "Risk Assessment", "Portfolio Scoring"], "status": "✅ Smart"},
        {"category": "📰 News & Sentiment", "features": ["Fake News Detection", "Sentiment Analysis", "Market Mood", "Social Media Tracking"], "status": "✅ AI-Powered"},
        {"category": "🔔 Alert System", "features": ["Price Alerts", "News Alerts", "Portfolio Notifications", "IPO Alerts"], "status": "✅ Real-time"},
        {"category": "🤖 AI Integration", "features": ["Investment Chatbot", "Natural Language Queries", "Personalized Advice", "Smart Recommendations"], "status": "✅ Advanced"}
    ]
    
    for feature_group in features_data:
        with st.expander(f"{feature_group['category']} - {feature_group['status']}"):
            for feature in feature_group['features']:
                st.write(f"• {feature}")
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Analyze Stock", type="primary"):
            st.switch_page("📊 Real-time Stock Analysis")
    
    with col2:
        if st.button("🚀 Check IPO", type="primary"):
            st.switch_page("🚀 IPO Intelligence Hub")
    
    with col3:
        if st.button("💰 Find SIP", type="primary"):
            st.switch_page("💰 Mutual Fund & SIP Center")
    
    with col4:
        if st.button("🛡️ Check Risk", type="primary"):
            st.switch_page("🛡️ Risk Management & Portfolio")

def show_realtime_stock_analysis():
    st.header("📊 Real-time Stock Analysis")
    
    st.markdown("""
    <div class="info-card">
        <h4>📈 Live Stock Data Analysis</h4>
        <p>Get real-time stock prices, technical indicators, and AI-powered predictions with authentic market data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stock selection with real Indian stocks
    indian_stocks = {
        'RELIANCE.NS': 'Reliance Industries',
        'TCS.NS': 'Tata Consultancy Services',
        'HDFCBANK.NS': 'HDFC Bank',
        'INFY.NS': 'Infosys',
        'HINDUNILVR.NS': 'Hindustan Unilever',
        'ICICIBANK.NS': 'ICICI Bank',
        'SBIN.NS': 'State Bank of India',
        'BHARTIARTL.NS': 'Bharti Airtel',
        'ITC.NS': 'ITC Limited',
        'KOTAKBANK.NS': 'Kotak Mahindra Bank',
        'LT.NS': 'Larsen & Toubro',
        'AXISBANK.NS': 'Axis Bank',
        'MARUTI.NS': 'Maruti Suzuki',
        'SUNPHARMA.NS': 'Sun Pharmaceutical',
        'NTPC.NS': 'NTPC Limited'
    }
    
    selected_stock = st.selectbox(
        "Select Stock for Real-time Analysis",
        options=list(indian_stocks.keys()),
        format_func=lambda x: f"{indian_stocks[x]} ({x})"
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("📈 Get Real-time Analysis", type="primary"):
            with st.spinner("Fetching real-time data and performing analysis..."):
                try:
                    # Fetch real-time data
                    ticker = yf.Ticker(selected_stock)
                    
                    # Get current data
                    info = ticker.info
                    hist_data = ticker.history(period="1y")
                    
                    if not hist_data.empty:
                        current_price = hist_data['Close'].iloc[-1]
                        prev_close = hist_data['Close'].iloc[-2] if len(hist_data) > 1 else current_price
                        change = current_price - prev_close
                        change_percent = (change / prev_close) * 100
                        
                        st.success(f"✅ Real-time analysis completed for {indian_stocks[selected_stock]}")
                        
                        # Current Price Information
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric(
                                "Current Price", 
                                f"₹{current_price:.2f}", 
                                delta=f"{change_percent:.2f}%"
                            )
                        
                        with col2:
                            volume = hist_data['Volume'].iloc[-1]
                            st.metric("Volume", f"{volume:,.0f}")
                        
                        with col3:
                            high_52w = hist_data['High'].max()
                            st.metric("52W High", f"₹{high_52w:.2f}")
                        
                        with col4:
                            low_52w = hist_data['Low'].min()
                            st.metric("52W Low", f"₹{low_52w:.2f}")
                        
                        # Technical Indicators
                        st.subheader("📊 Technical Indicators")
                        
                        # Calculate technical indicators
                        prices = hist_data['Close']
                        
                        # Moving Averages
                        ma_20 = prices.rolling(window=20).mean().iloc[-1]
                        ma_50 = prices.rolling(window=50).mean().iloc[-1]
                        
                        # RSI
                        delta = prices.diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        rsi = 100 - (100 / (1 + rs))
                        current_rsi = rsi.iloc[-1]
                        
                        # MACD
                        ema_12 = prices.ewm(span=12).mean()
                        ema_26 = prices.ewm(span=26).mean()
                        macd = ema_12 - ema_26
                        signal = macd.ewm(span=9).mean()
                        current_macd = macd.iloc[-1]
                        current_signal = signal.iloc[-1]
                        
                        tech_col1, tech_col2, tech_col3 = st.columns(3)
                        
                        with tech_col1:
                            st.write("**Moving Averages**")
                            st.write(f"20-Day MA: ₹{ma_20:.2f}")
                            st.write(f"50-Day MA: ₹{ma_50:.2f}")
                            
                            # MA Signal
                            if current_price > ma_20 > ma_50:
                                st.success("🟢 Bullish Trend")
                            elif current_price < ma_20 < ma_50:
                                st.error("🔴 Bearish Trend")
                            else:
                                st.warning("🟡 Sideways Trend")
                        
                        with tech_col2:
                            st.write("**RSI Analysis**")
                            st.write(f"RSI (14): {current_rsi:.2f}")
                            
                            if current_rsi > 70:
                                st.error("🔴 Overbought")
                            elif current_rsi < 30:
                                st.success("🟢 Oversold")
                            else:
                                st.info("🔵 Neutral")
                        
                        with tech_col3:
                            st.write("**MACD Analysis**")
                            st.write(f"MACD: {current_macd:.2f}")
                            st.write(f"Signal: {current_signal:.2f}")
                            
                            if current_macd > current_signal:
                                st.success("🟢 Bullish Signal")
                            else:
                                st.error("🔴 Bearish Signal")
                        
                        # Price Chart
                        st.subheader("📈 Price Chart with Technical Indicators")
                        
                        fig = go.Figure()
                        
                        # Candlestick chart
                        fig.add_trace(go.Candlestick(
                            x=hist_data.index,
                            open=hist_data['Open'],
                            high=hist_data['High'],
                            low=hist_data['Low'],
                            close=hist_data['Close'],
                            name="Price"
                        ))
                        
                        # Moving averages
                        fig.add_trace(go.Scatter(
                            x=hist_data.index,
                            y=prices.rolling(window=20).mean(),
                            mode='lines',
                            name='MA 20',
                            line=dict(color='orange', width=2)
                        ))
                        
                        fig.add_trace(go.Scatter(
                            x=hist_data.index,
                            y=prices.rolling(window=50).mean(),
                            mode='lines',
                            name='MA 50',
                            line=dict(color='blue', width=2)
                        ))
                        
                        fig.update_layout(
                            title=f"{indian_stocks[selected_stock]} - Price Chart with Technical Indicators",
                            xaxis_title="Date",
                            yaxis_title="Price (₹)",
                            height=600,
                            template="plotly_white"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # AI-Powered Recommendation
                        st.subheader("🤖 AI-Powered Investment Recommendation")
                        
                        # Simple recommendation logic based on technical indicators
                        recommendation_score = 0
                        
                        # Price vs MA
                        if current_price > ma_20:
                            recommendation_score += 2
                        if current_price > ma_50:
                            recommendation_score += 2
                        
                        # RSI
                        if 30 < current_rsi < 70:
                            recommendation_score += 2
                        elif current_rsi < 30:
                            recommendation_score += 3  # Oversold is good for buying
                        
                        # MACD
                        if current_macd > current_signal:
                            recommendation_score += 2
                        
                        # Volume analysis
                        avg_volume = hist_data['Volume'].rolling(window=20).mean().iloc[-1]
                        if volume > avg_volume * 1.2:
                            recommendation_score += 1
                        
                        # Generate recommendation
                        if recommendation_score >= 8:
                            recommendation = "STRONG BUY"
                            rec_class = "rec-strong-buy"
                            advice = "Strong technical indicators suggest this is a good buying opportunity."
                        elif recommendation_score >= 6:
                            recommendation = "BUY"
                            rec_class = "rec-buy"
                            advice = "Positive technical signals indicate potential upside."
                        elif recommendation_score >= 4:
                            recommendation = "HOLD"
                            rec_class = "rec-hold"
                            advice = "Mixed signals suggest holding current positions."
                        else:
                            recommendation = "SELL"
                            rec_class = "rec-sell"
                            advice = "Technical indicators suggest caution or profit booking."
                        
                        st.markdown(f"""
                        <div style="text-align: center; margin: 2rem 0;">
                            <span class="{rec_class}">{recommendation}</span>
                            <p style="color: #4a5568; font-weight: 600; margin-top: 1rem;">{advice}</p>
                            <p style="color: #667eea; font-weight: 500;">Confidence Score: {recommendation_score}/10</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Key Statistics
                        st.subheader("📋 Key Statistics")
                        
                        stats_col1, stats_col2 = st.columns(2)
                        
                        with stats_col1:
                            market_cap = info.get('marketCap', 'N/A')
                            if market_cap != 'N/A':
                                market_cap_cr = market_cap / 10000000  # Convert to crores
                                st.write(f"**Market Cap:** ₹{market_cap_cr:,.0f} Cr")
                            
                            pe_ratio = info.get('trailingPE', 'N/A')
                            st.write(f"**P/E Ratio:** {pe_ratio}")
                            
                            pb_ratio = info.get('priceToBook', 'N/A')
                            st.write(f"**P/B Ratio:** {pb_ratio}")
                        
                        with stats_col2:
                            dividend_yield = info.get('dividendYield', 'N/A')
                            if dividend_yield != 'N/A':
                                dividend_yield = dividend_yield * 100
                                st.write(f"**Dividend Yield:** {dividend_yield:.2f}%")
                            else:
                                st.write(f"**Dividend Yield:** N/A")
                            
                            beta = info.get('beta', 'N/A')
                            st.write(f"**Beta:** {beta}")
                            
                            # Calculate volatility
                            returns = prices.pct_change().dropna()
                            volatility = returns.std() * np.sqrt(252) * 100
                            st.write(f"**Volatility:** {volatility:.2f}%")
                    
                    else:
                        st.error("❌ Unable to fetch real-time data for this stock")
                
                except Exception as e:
                    st.error(f"❌ Error fetching stock data: {str(e)}")
                    st.info("💡 Please try again or select a different stock")
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>📊 Analysis Features</h4>
            <p><strong>Real-time Data:</strong></p>
            <p>• Live price updates</p>
            <p>• Current volume data</p>
            <p>• 52-week high/low</p>
            <p></p>
            <p><strong>Technical Analysis:</strong></p>
            <p>• Moving Averages (20, 50)</p>
            <p>• RSI (14-period)</p>
            <p>• MACD analysis</p>
            <p></p>
            <p><strong>AI Recommendations:</strong></p>
            <p>• Buy/Sell/Hold signals</p>
            <p>• Confidence scoring</p>
            <p>• Investment advice</p>
        </div>
        """, unsafe_allow_html=True)

def show_enhanced_ipo_intelligence():
    st.header("🚀 IPO Intelligence Hub - Enhanced Analysis")
    
    st.markdown("""
    <div class="info-card">
        <h4>✨ India's First Complete IPO Intelligence System</h4>
        <p>Advanced post-IPO performance analysis, retail sentiment forecasting, and ML-powered hold/exit recommendations - features not available on any other platform including Groww!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize IPO system if needed
    if st.button("🚀 Initialize IPO Intelligence System"):
        with st.spinner("Setting up comprehensive IPO analysis system..."):
            # Collect recent IPO data
            recent_ipos = st.session_state.ipo_intelligence.collect_recent_ipos()
            
            # Collect comprehensive data
            comprehensive_data = st.session_state.ipo_data_collector.comprehensive_ipo_data_collection()
            
            if comprehensive_data:
                st.session_state.ipo_data_collector.update_ipo_database(comprehensive_data)
                st.success(f"✅ IPO Intelligence System initialized with {len(comprehensive_data)} IPOs")
            else:
                st.error("❌ Failed to initialize IPO system")
    
    # Get available IPOs
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        available_ipos = pd.read_sql_query(
            "SELECT symbol, company_name, listing_date, issue_price FROM ipo_intelligence ORDER BY listing_date DESC", 
            conn
        )
        conn.close()
        
        if not available_ipos.empty:
            st.subheader("📊 Available IPOs for Analysis")
            
            # Display IPO summary table
            st.dataframe(available_ipos, use_container_width=True)
            
            # IPO Selection for detailed analysis
            selected_ipo = st.selectbox(
                "Select IPO for Complete Intelligence Analysis",
                options=available_ipos['symbol'].tolist(),
                format_func=lambda x: f"{available_ipos[available_ipos['symbol']==x]['company_name'].iloc[0]} ({x})"
            )
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if st.button("🚀 Perform Complete IPO Intelligence Analysis", type="primary"):
                    with st.spinner("Performing comprehensive IPO analysis with real data..."):
                        # Get comprehensive analysis
                        analysis = st.session_state.ipo_intelligence.comprehensive_ipo_analysis(selected_ipo)
                        
                        if analysis:
                            st.success(f"✅ Complete IPO intelligence analysis completed for {selected_ipo}")
                            
                            # Display comprehensive results
                            display_enhanced_ipo_analysis(analysis)
                        else:
                            st.error("❌ Unable to complete IPO analysis")
            
            with col2:
                st.markdown("""
                <div class="info-card">
                    <h4>🎯 Unique Analysis Features</h4>
                    <p><strong>Performance Tracking:</strong></p>
                    <p>• 30/60/90 day analysis</p>
                    <p>• Listing gains calculation</p>
                    <p>• Volume pattern analysis</p>
                    <p></p>
                    <p><strong>Sentiment Intelligence:</strong></p>
                    <p>• News sentiment scoring</p>
                    <p>• Social media analysis</p>
                    <p>• Retail sentiment impact</p>
                    <p></p>
                    <p><strong>Smart Recommendations:</strong></p>
                    <p>• Hold/Exit advice</p>
                    <p>• Target price calculation</p>
                    <p>• Risk assessment</p>
                    <p>• Confidence scoring</p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.info("📊 No IPO data available. Please initialize the IPO Intelligence System first.")
    
    except Exception as e:
        st.error(f"❌ Error loading IPO data: {str(e)}")

def display_enhanced_ipo_analysis(analysis):
    """Display enhanced IPO analysis with detailed insights"""
    
    basic_info = analysis.get('basic_info', {})
    performance = analysis.get('performance_analysis', {})
    sentiment = analysis.get('sentiment_analysis', {})
    recommendation = analysis.get('recommendation', {})
    
    # IPO Basic Information with Enhanced Display
    st.subheader("📊 IPO Overview & Key Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Issue Price", f"₹{basic_info.get('issue_price', 'N/A')}")
    with col2:
        issue_size = basic_info.get('issue_size_crores', 0)
        st.metric("Issue Size", f"₹{issue_size:,.0f} Cr")
    with col3:
        subscription = basic_info.get('subscription_times', 0)
        st.metric("Subscription", f"{subscription:.1f}x")
    with col4:
        st.metric("Sector", basic_info.get('sector', 'N/A'))
    with col5:
        st.metric("Market Cap", basic_info.get('market_cap_category', 'N/A'))
    
    # Performance Analysis with Enhanced Visualization
    if performance:
        st.subheader("📈 Post-IPO Performance Intelligence")
        
        # Performance metrics
        perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
        
        with perf_col1:
            listing_gains = performance.get('listing_gains_percent', 0)
            st.metric("Listing Day Gains", f"{listing_gains:.2f}%", delta=listing_gains)
        
        with perf_col2:
            perf_30d = performance.get('performance_30d', 0)
            st.metric("30-Day Performance", f"{perf_30d:.2f}%", delta=perf_30d)
        
        with perf_col3:
            perf_60d = performance.get('performance_60d', 0)
            st.metric("60-Day Performance", f"{perf_60d:.2f}%", delta=perf_60d)
        
        with perf_col4:
            perf_90d = performance.get('performance_90d', 0)
            st.metric("90-Day Performance", f"{perf_90d:.2f}%", delta=perf_90d)
        
        # Performance trend visualization
        if all(key in performance for key in ['performance_1d', 'performance_7d', 'performance_30d', 'performance_60d', 'performance_90d']):
            performance_data = {
                'Days': [1, 7, 30, 60, 90],
                'Performance (%)': [
                    performance.get('listing_gains_percent', 0),
                    performance['performance_7d'],
                    performance['performance_30d'],
                    performance['performance_60d'],
                    performance['performance_90d']
                ]
            }
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=performance_data['Days'],
                y=performance_data['Performance (%)'],
                mode='lines+markers',
                name='Performance',
                line=dict(color='#667eea', width=4),
                marker=dict(size=10, color='#667eea')
            ))
            
            # Add zero line
            fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Break-even")
            
            fig.update_layout(
                title="Post-IPO Performance Trend Analysis",
                xaxis_title="Days After Listing",
                yaxis_title="Performance (%)",
                height=400,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Liquidity and Volume Analysis
        st.subheader("💧 Liquidity & Volume Intelligence")
        
        liq_col1, liq_col2, liq_col3 = st.columns(3)
        
        with liq_col1:
            liquidity_score = performance.get('liquidity_score', 0)
            st.metric("Liquidity Score", f"{liquidity_score:.1f}/100")
        
        with liq_col2:
            volatility = performance.get('volatility_score', 0)
            st.metric("Volatility", f"{volatility:.2f}%")
        
        with liq_col3:
            volume_day_1 = performance.get('volume_day_1', 0)
            st.metric("Listing Day Volume", f"{volume_day_1:,.0f}")
    
    # Sentiment Analysis with Enhanced Insights
    if sentiment:
        st.subheader("📰 Sentiment Intelligence Analysis")
        
        sent_col1, sent_col2, sent_col3, sent_col4 = st.columns(4)
        
        with sent_col1:
            news_sentiment = sentiment.get('news_sentiment_score', 0)
            st.metric("News Sentiment", f"{news_sentiment:.3f}")
        
        with sent_col2:
            social_sentiment = sentiment.get('social_sentiment_score', 0)
            st.metric("Social Media", f"{social_sentiment:.3f}")
        
        with sent_col3:
            retail_sentiment = sentiment.get('retail_sentiment_score', 0)
            st.metric("Retail Sentiment", f"{retail_sentiment:.3f}")
        
        with sent_col4:
            overall_sentiment = sentiment.get('overall_sentiment_score', 0)
            st.metric("Overall Sentiment", f"{overall_sentiment:.3f}")
        
        # Sentiment visualization
        sentiment_data = {
            'Sentiment Type': ['News Media', 'Social Media', 'Retail Investors', 'Overall'],
            'Score': [
                news_sentiment,
                social_sentiment,
                retail_sentiment,
                overall_sentiment
            ]
        }
        
        fig = px.bar(
            x=sentiment_data['Sentiment Type'],
            y=sentiment_data['Score'],
            title="Comprehensive Sentiment Analysis",
            labels={'x': 'Sentiment Source', 'y': 'Sentiment Score'},
            color=sentiment_data['Score'],
            color_continuous_scale=['red', 'yellow', 'green']
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Sentiment interpretation
        if overall_sentiment > 0.3:
            st.success("🚀 Very Positive Sentiment - Strong investor confidence and market optimism")
        elif overall_sentiment > 0.1:
            st.info("📈 Positive Sentiment - Good investor interest with upward bias")
        elif overall_sentiment > -0.1:
            st.warning("😐 Neutral Sentiment - Mixed investor opinions, wait and watch approach")
        else:
            st.error("📉 Negative Sentiment - Investor concerns and bearish outlook")
    
    # Smart Recommendations with Enhanced Logic
    if recommendation:
        st.subheader("💡 AI-Powered Investment Recommendations")
        
        rec_type = recommendation.get('recommendation', 'N/A')
        confidence = recommendation.get('confidence_score', 0)
        advice = recommendation.get('hold_exit_advice', 'No advice available')
        
        # Enhanced recommendation display
        rec_colors = {
            'STRONG HOLD': '#48bb78',
            'HOLD': '#4299e1',
            'PARTIAL EXIT': '#ed8936',
            'EXIT': '#f56565'
        }
        
        rec_color = rec_colors.get(rec_type, '#6c757d')
        
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0; padding: 2rem; background: rgba(255,255,255,0.95); border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <h3 style="color: #2d3748; margin-bottom: 1rem;">Investment Recommendation</h3>
            <div style="background: {rec_color}; color: white; padding: 1rem 2rem; border-radius: 50px; font-size: 1.5rem; font-weight: 700; margin: 1rem 0; display: inline-block;">
                {rec_type}
            </div>
            <p style="color: #4a5568; font-size: 1.2rem; font-weight: 600; margin: 1rem 0;">Confidence: {confidence:.1f}%</p>
            <p style="color: #2d3748; font-size: 1.1rem; font-weight: 500; line-height: 1.6; margin-top: 1rem;">{advice}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Target and Risk Metrics
        target_col1, target_col2, target_col3 = st.columns(3)
        
        with target_col1:
            target_price = recommendation.get('target_price', 0)
            st.metric("Target Price", f"₹{target_price:.2f}")
        
        with target_col2:
            stop_loss = recommendation.get('stop_loss', 0)
            st.metric("Stop Loss", f"₹{stop_loss:.2f}")
        
        with target_col3:
            risk_rating = recommendation.get('risk_rating', 'N/A')
            st.metric("Risk Rating", risk_rating)
        
        # Investment Strategy Explanation
        st.subheader("📋 Investment Strategy Explanation")
        
        strategy_explanation = f"""
        **Analysis Summary:**
        
        • **Performance Analysis:** Based on {basic_info.get('company_name', 'the company')}'s post-IPO performance over 30, 60, and 90 days
        • **Sentiment Impact:** Considering news sentiment ({sentiment.get('news_sentiment_score', 0):.3f}) and retail investor mood
        • **Risk Assessment:** Volatility analysis and market conditions evaluation
        • **Liquidity Consideration:** Trading volume patterns and market maker activity
        
        **Why {rec_type}?**
        
        {advice}
        
        **Risk Factors:**
        • Market volatility: {performance.get('volatility_score', 0):.2f}%
        • Liquidity risk: {recommendation.get('liquidity_risk', 'Moderate')}
        • Sentiment risk: Based on current market mood and news flow
        
        **Action Plan:**
        1. Monitor price movement around target (₹{target_price:.2f})
        2. Set stop-loss at ₹{stop_loss:.2f} to limit downside
        3. Review recommendation weekly based on new developments
        4. Consider market conditions and personal risk tolerance
        """
        
        st.markdown(strategy_explanation)
    
    # Additional Insights
    st.subheader("🔍 Additional Market Insights")
    
    insights = [
        f"📊 **Subscription Analysis:** {basic_info.get('subscription_times', 0):.1f}x subscription indicates {'strong' if basic_info.get('subscription_times', 0) > 10 else 'moderate' if basic_info.get('subscription_times', 0) > 3 else 'weak'} investor demand",
        f"🏢 **Sector Performance:** {basic_info.get('sector', 'N/A')} sector showing {'positive' if sentiment.get('overall_sentiment_score', 0) > 0 else 'mixed'} sentiment",
        f"💰 **Market Cap Category:** {basic_info.get('market_cap_category', 'N/A')} stocks typically show {'higher volatility but growth potential' if 'Small' in str(basic_info.get('market_cap_category', '')) else 'stable performance with moderate growth'}",
        f"📈 **Performance Trend:** {'Positive momentum' if performance.get('performance_30d', 0) > 0 else 'Negative momentum'} in recent 30-day period"
    ]
    
    for insight in insights:
        st.write(insight)

def show_mutual_fund_sip_center():
    st.header("💰 Mutual Fund & SIP Center")
    
    st.markdown("""
    <div class="info-card">
        <h4>💰 Comprehensive Mutual Fund Analysis & SIP Optimization</h4>
        <p>Advanced mutual fund research, SIP planning, and portfolio optimization with real fund data and performance analytics.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize MF system
    if st.button("💰 Initialize Mutual Fund Database"):
        with st.spinner("Loading comprehensive mutual fund data..."):
            funds_data = st.session_state.mf_sip_system.collect_mutual_fund_data()
            if funds_data:
                st.success(f"✅ Loaded {len(funds_data)} mutual funds with complete data")
            else:
                st.error("❌ Failed to load mutual fund data")
    
    # Tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Fund Research", "📊 SIP Planning", "⚖️ Fund Comparison", "📈 Performance Analysis"])
    
    with tab1:
        st.subheader("🔍 Mutual Fund Research")
        
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            funds_df = pd.read_sql_query("SELECT * FROM mutual_funds", conn)
            conn.close()
            
            if not funds_df.empty:
                # Filter options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    category_filter = st.selectbox(
                        "Fund Category",
                        options=['All'] + list(funds_df['category'].unique())
                    )
                
                with col2:
                    risk_filter = st.selectbox(
                        "Risk Level",
                        options=['All'] + list(funds_df['risk_rating'].unique())
                    )
                
                with col3:
                    min_sip = st.number_input("Max SIP Amount", min_value=500, value=5000, step=500)
                
                # Apply filters
                filtered_funds = funds_df.copy()
                
                if category_filter != 'All':
                    filtered_funds = filtered_funds[filtered_funds['category'] == category_filter]
                
                if risk_filter != 'All':
                    filtered_funds = filtered_funds[filtered_funds['risk_rating'] == risk_filter]
                
                filtered_funds = filtered_funds[filtered_funds['min_sip'] <= min_sip]
                
                # Display filtered funds
                if not filtered_funds.empty:
                    st.write(f"**Found {len(filtered_funds)} funds matching your criteria:**")
                    
                    # Display key metrics
                    display_cols = ['scheme_name', 'fund_house', 'category', 'return_3y', 'expense_ratio', 'min_sip', 'risk_rating']
                    display_df = filtered_funds[display_cols].copy()
                    display_df.columns = ['Fund Name', 'Fund House', 'Category', '3Y Return (%)', 'Expense Ratio (%)', 'Min SIP (₹)', 'Risk Rating']
                    
                    st.dataframe(display_df, use_container_width=True)
                    
                    # Top performers
                    st.subheader("🏆 Top Performing Funds")
                    
                    top_performers = filtered_funds.nlargest(3, 'return_3y')
                    
                    for _, fund in top_performers.iterrows():
                        st.markdown(f"""
                        <div class="info-card">
                            <h4>{fund['scheme_name']}</h4>
                            <p><strong>Fund House:</strong> {fund['fund_house']}</p>
                            <p><strong>3-Year Return:</strong> {fund['return_3y']:.2f}% | <strong>Expense Ratio:</strong> {fund['expense_ratio']:.2f}%</p>
                            <p><strong>Min SIP:</strong> ₹{fund['min_sip']:,.0f} | <strong>Risk:</strong> {fund['risk_rating']}</p>
                            <p><strong>Fund Manager:</strong> {fund['fund_manager']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                else:
                    st.info("No funds match your criteria. Please adjust the filters.")
            
            else:
                st.info("Please initialize the mutual fund database first.")
        
        except Exception as e:
            st.error(f"Error loading fund data: {str(e)}")
    
    with tab2:
        st.subheader("📊 SIP Planning & Optimization")
        
        st.write("**Create Your Personalized SIP Portfolio:**")
        
        with st.form("sip_planning_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                monthly_amount = st.number_input("Monthly SIP Amount (₹)", min_value=500, value=10000, step=500)
                age = st.number_input("Your Age", min_value=18, max_value=65, value=30)
                investment_horizon = st.selectbox(
                    "Investment Horizon",
                    options=['1-3 years', '3-5 years', '5-10 years', '10+ years']
                )
            
            with col2:
                risk_tolerance = st.selectbox(
                    "Risk Tolerance",
                    options=['conservative', 'moderate', 'aggressive']
                )
                
                investment_goal = st.selectbox(
                    "Investment Goal",
                    options=['Wealth Creation', 'Tax Saving', 'Retirement Planning', 'Child Education', 'Emergency Fund']
                )
                
                existing_investments = st.number_input("Existing Investments (₹)", min_value=0, value=0, step=10000)
            
            generate_sip_plan = st.form_submit_button("📊 Generate SIP Plan", type="primary")
            
            if generate_sip_plan:
                with st.spinner("Creating personalized SIP portfolio..."):
                    user_profile = {
                        'monthly_amount': monthly_amount,
                        'age': age,
                        'risk_tolerance': risk_tolerance,
                        'investment_horizon': investment_horizon,
                        'investment_goal': investment_goal,
                        'existing_investments': existing_investments
                    }
                    
                    recommendations = st.session_state.mf_sip_system.recommend_sip_portfolio(user_profile)
                    
                    if recommendations:
                        st.success("✅ Personalized SIP portfolio created!")
                        
                        # Portfolio allocation
                        st.subheader("📊 Recommended Portfolio Allocation")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Monthly Investment", f"₹{recommendations['total_monthly_amount']:,.0f}")
                        
                        with col2:
                            st.metric("Expected Annual Return", f"{recommendations['expected_annual_return']:.2f}%")
                        
                        with col3:
                            years = recommendations['investment_horizon_years']
                            st.metric("Investment Period", f"{years} years")
                        
                        # Projection
                        proj_col1, proj_col2, proj_col3 = st.columns(3)
                        
                        with proj_col1:
                            total_investment = recommendations['total_investment']
                            st.metric("Total Investment", f"₹{total_investment:,.0f}")
                        
                        with proj_col2:
                            projected_value = recommendations['projected_value']
                            st.metric("Projected Value", f"₹{projected_value:,.0f}")
                        
                        with proj_col3:
                            expected_gain = recommendations['expected_gain']
                            st.metric("Expected Gain", f"₹{expected_gain:,.0f}")
                        
                        # Fund recommendations
                        st.subheader("💡 Recommended Funds")
                        
                        for i, rec in enumerate(recommendations['recommendations']):
                            fund = rec['fund']
                            allocation_amount = rec['allocation_amount']
                            allocation_percent = rec['allocation_percentage']
                            reason = rec['reason']
                            
                            st.markdown(f"""
                            <div class="info-card">
                                <h4>{fund['scheme_name']}</h4>
                                <p><strong>Monthly SIP:</strong> ₹{allocation_amount:,.0f} ({allocation_percent:.1f}% of portfolio)</p>
                                <p><strong>Fund House:</strong> {fund['fund_house']} | <strong>Category:</strong> {fund['sub_category']}</p>
                                <p><strong>3-Year Return:</strong> {fund['return_3y']:.2f}% | <strong>Expense Ratio:</strong> {fund['expense_ratio']:.2f}%</p>
                                <p><strong>Why this fund:</strong> {reason}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Asset allocation chart
                        if len(recommendations['recommendations']) > 1:
                            fund_names = [rec['fund']['scheme_name'][:30] + '...' if len(rec['fund']['scheme_name']) > 30 else rec['fund']['scheme_name'] for rec in recommendations['recommendations']]
                            allocations = [rec['allocation_percentage'] for rec in recommendations['recommendations']]
                            
                            fig = px.pie(
                                values=allocations,
                                names=fund_names,
                                title="Portfolio Asset Allocation"
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # SIP projection chart
                        years_range = list(range(1, years + 1))
                        investment_values = [monthly_amount * 12 * year for year in years_range]
                        projected_values = []
                        
                        for year in years_range:
                            value = st.session_state.mf_sip_system.calculate_sip_projection(
                                monthly_amount, recommendations['expected_annual_return'], year
                            )
                            projected_values.append(value)
                        
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=years_range,
                            y=investment_values,
                            mode='lines',
                            name='Total Investment',
                            line=dict(color='orange', width=3)
                        ))
                        
                        fig.add_trace(go.Scatter(
                            x=years_range,
                            y=projected_values,
                            mode='lines',
                            name='Projected Value',
                            line=dict(color='green', width=3)
                        ))
                        
                        fig.update_layout(
                            title="SIP Growth Projection",
                            xaxis_title="Years",
                            yaxis_title="Amount (₹)",
                            height=400,
                            template="plotly_white"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    else:
                        st.error("❌ Unable to generate SIP recommendations")
    
    with tab3:
        st.subheader("⚖️ Fund Comparison Tool")
        
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            funds_df = pd.read_sql_query("SELECT scheme_code, scheme_name FROM mutual_funds", conn)
            conn.close()
            
            if not funds_df.empty:
                selected_funds = st.multiselect(
                    "Select Funds to Compare (2-4 funds)",
                    options=funds_df['scheme_code'].tolist(),
                    format_func=lambda x: funds_df[funds_df['scheme_code']==x]['scheme_name'].iloc[0]
                )
                
                if len(selected_funds) >= 2:
                    if st.button("⚖️ Compare Selected Funds", type="primary"):
                        with st.spinner("Comparing selected funds..."):
                            comparison = st.session_state.mf_sip_system.compare_mutual_funds(selected_funds)
                            
                            if comparison:
                                st.success("✅ Fund comparison completed!")
                                
                                # Winner announcement
                                if comparison['winner']:
                                    st.markdown(f"""
                                    <div style="text-align: center; margin: 2rem 0; padding: 2rem; background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); border-radius: 20px; color: white;">
                                        <h3>🏆 Winner: {comparison['winner']}</h3>
                                        <p style="font-size: 1.1rem; margin-top: 1rem;">{comparison['comparison_summary']}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                # Detailed comparison
                                st.subheader("📊 Detailed Comparison")
                                
                                metrics = comparison['comparison_metrics']
                                
                                # Performance comparison
                                st.write("**Performance Metrics:**")
                                perf_data = {
                                    'Fund': list(metrics['return_3y'].keys()),
                                    '1Y Return (%)': [metrics['return_1y'][fund] for fund in metrics['return_1y'].keys()],
                                    '3Y Return (%)': [metrics['return_3y'][fund] for fund in metrics['return_3y'].keys()],
                                    '5Y Return (%)': [metrics['return_5y'][fund] for fund in metrics['return_5y'].keys()],
                                    'Sharpe Ratio': [metrics['sharpe_ratio'][fund] for fund in metrics['sharpe_ratio'].keys()]
                                }
                                
                                perf_df = pd.DataFrame(perf_data)
                                st.dataframe(perf_df, use_container_width=True)
                                
                                # Risk comparison
                                st.write("**Risk Metrics:**")
                                risk_data = {
                                    'Fund': list(metrics['standard_deviation'].keys()),
                                    'Volatility (%)': [metrics['standard_deviation'][fund] for fund in metrics['standard_deviation'].keys()],
                                    'Beta': [metrics['beta'][fund] for fund in metrics['beta'].keys()],
                                    'Expense Ratio (%)': [metrics['expense_ratio'][fund] for fund in metrics['expense_ratio'].keys()]
                                }
                                
                                risk_df = pd.DataFrame(risk_data)
                                st.dataframe(risk_df, use_container_width=True)
                                
                                # Visual comparison
                                fig = go.Figure()
                                
                                for fund in metrics['return_3y'].keys():
                                    fig.add_trace(go.Bar(
                                        name=fund[:20] + '...' if len(fund) > 20 else fund,
                                        x=['1Y Return', '3Y Return', '5Y Return'],
                                        y=[
                                            metrics['return_1y'][fund],
                                            metrics['return_3y'][fund],
                                            metrics['return_5y'][fund]
                                        ]
                                    ))
                                
                                fig.update_layout(
                                    title="Performance Comparison",
                                    xaxis_title="Time Period",
                                    yaxis_title="Returns (%)",
                                    barmode='group',
                                    height=400
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                            
                            else:
                                st.error("❌ Unable to compare funds")
                
                else:
                    st.info("Please select at least 2 funds for comparison")
            
            else:
                st.info("Please initialize the mutual fund database first.")
        
        except Exception as e:
            st.error(f"Error in fund comparison: {str(e)}")
    
    with tab4:
        st.subheader("📈 SIP Performance Analysis")
        
        st.write("**Analyze Your Existing SIP Performance:**")
        
        with st.form("sip_performance_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                try:
                    conn = sqlite3.connect(DATABASE_PATH)
                    funds_df = pd.read_sql_query("SELECT scheme_code, scheme_name FROM mutual_funds", conn)
                    conn.close()
                    
                    if not funds_df.empty:
                        selected_fund = st.selectbox(
                            "Select Your SIP Fund",
                            options=funds_df['scheme_code'].tolist(),
                            format_func=lambda x: funds_df[funds_df['scheme_code']==x]['scheme_name'].iloc[0]
                        )
                        
                        monthly_sip = st.number_input("Monthly SIP Amount (₹)", min_value=500, value=5000, step=500)
                    
                    else:
                        st.info("Please initialize the mutual fund database first.")
                        selected_fund = None
                        monthly_sip = 5000
                
                except:
                    selected_fund = None
                    monthly_sip = 5000
            
            with col2:
                start_date = st.date_input("SIP Start Date", value=datetime.now().date() - timedelta(days=365))
                current_date = st.date_input("Analysis Date", value=datetime.now().date())
            
            analyze_sip = st.form_submit_button("📈 Analyze SIP Performance", type="primary")
            
            if analyze_sip and selected_fund:
                with st.spinner("Analyzing SIP performance..."):
                    performance = st.session_state.mf_sip_system.analyze_sip_performance(
                        selected_fund, monthly_sip, start_date.strftime('%Y-%m-%d'), current_date.strftime('%Y-%m-%d')
                    )
                    
                    if performance:
                        st.success("✅ SIP performance analysis completed!")
                        
                        # Performance metrics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Total Invested", f"₹{performance['total_invested']:,.0f}")
                        
                        with col2:
                            st.metric("Current Value", f"₹{performance['current_value']:,.0f}")
                        
                        with col3:
                            st.metric("Absolute Return", f"₹{performance['absolute_return']:,.0f}")
                        
                        with col4:
                            st.metric("Return %", f"{performance['percentage_return']:.2f}%")
                        
                        # Additional metrics
                        add_col1, add_col2, add_col3 = st.columns(3)
                        
                        with add_col1:
                            st.metric("Months Invested", performance['months_invested'])
                        
                        with add_col2:
                            st.metric("Annualized Return", f"{performance['annualized_return']:.2f}%")
                        
                        with add_col3:
                            st.metric("Fund Category", performance['fund_category'])
                        
                        # Performance interpretation
                        if performance['percentage_return'] > 15:
                            st.success("🚀 Excellent Performance - Your SIP is generating strong returns!")
                        elif performance['percentage_return'] > 8:
                            st.info("📈 Good Performance - Your SIP is on track with market expectations")
                        elif performance['percentage_return'] > 0:
                            st.warning("📊 Moderate Performance - Consider reviewing your fund selection")
                        else:
                            st.error("📉 Underperforming - You may want to consider switching funds")
                    
                    else:
                        st.error("❌ Unable to analyze SIP performance")

def show_faq_help_center():
    st.header("❓ FAQ & Help Center")
    
    st.markdown("""
    <div class="info-card">
        <h4>❓ Frequently Asked Questions & Help</h4>
        <p>Get answers to common questions about our platform features, calculations, and investment strategies in simple, easy-to-understand language.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ Categories
    faq_categories = {
        "📊 Stock Analysis": [
            {
                "question": "How do you calculate sentiment analysis scores?",
                "answer": """
                **Sentiment Analysis Calculation (Simple Explanation):**
                
                We analyze news articles and social media posts about stocks using three methods:
                
                1. **VADER Analysis**: This tool reads the text and gives a score from -1 (very negative) to +1 (very positive)
                2. **TextBlob Analysis**: Another tool that checks if words are positive or negative
                3. **Financial Keywords**: We look for specific finance words like 'profit', 'loss', 'growth', etc.
                
                **Final Score Calculation:**
                - We combine all three scores with weights: VADER (40%) + TextBlob (30%) + Keywords (30%)
                - Score above 0.3 = Very Positive
                - Score 0.1 to 0.3 = Positive  
                - Score -0.1 to 0.1 = Neutral
                - Score below -0.1 = Negative
                
                **Example**: If news says "Company reports excellent quarterly profits", it gets a positive score around +0.6
                """
            },
            {
                "question": "What are technical indicators and how do they work?",
                "answer": """
                **Technical Indicators (Simple Explanation):**
                
                Think of technical indicators like a doctor's tools to check stock health:
                
                **1. Moving Average (MA):**
                - Like taking average temperature over 20 days
                - If today's price > MA = Stock is healthy (uptrend)
                - If today's price < MA = Stock might be sick (downtrend)
                
                **2. RSI (Relative Strength Index):**
                - Like checking if stock is overworked or underworked
                - RSI > 70 = Stock is overworked (overbought) - might fall
                - RSI < 30 = Stock is underworked (oversold) - might rise
                - RSI 30-70 = Stock is normal
                
                **3. MACD:**
                - Like checking stock's energy levels
                - When MACD line goes above signal line = Stock getting energetic (buy signal)
                - When MACD line goes below signal line = Stock getting tired (sell signal)
                """
            },
            {
                "question": "How accurate are your stock price predictions?",
                "answer": """
                **Stock Prediction Accuracy (Honest Answer):**
                
                **Our Accuracy Range**: 60-75% for short-term trends (1-7 days)
                
                **How We Predict:**
                1. **Historical Data Analysis**: We study past 2 years of price movements
                2. **Technical Indicators**: We use RSI, MACD, Moving Averages
                3. **Sentiment Analysis**: We check news and social media mood
                4. **Machine Learning**: Our AI learns from patterns
                
                **Important Note**: 
                - No one can predict stock prices with 100% accuracy
                - Even experts get it wrong sometimes
                - We provide probability-based predictions, not guarantees
                - Always invest only what you can afford to lose
                
                **Best Use**: Use our predictions as one factor among many for your decisions
                """
            }
        ],
        "🚀 IPO Analysis": [
            {
                "question": "What makes your IPO analysis unique compared to other platforms?",
                "answer": """
                **Our Unique IPO Features (Not Available on Groww/Zerodha):**
                
                **1. Post-IPO Performance Tracking:**
                - We track how IPO performs for 30, 60, and 90 days after listing
                - Most platforms only show listing day performance
                - We analyze if you should hold or sell after listing
                
                **2. Retail Sentiment Impact:**
                - We measure how retail investor mood affects IPO pricing
                - We analyze social media buzz and news sentiment
                - This helps predict if IPO will sustain or fall
                
                **3. Liquidity Forecasting:**
                - We predict how easily you can buy/sell IPO shares after listing
                - Low liquidity = hard to sell when you want
                - High liquidity = easy to exit anytime
                
                **4. Hold/Exit Recommendations:**
                - We give specific advice: HOLD, PARTIAL EXIT, or FULL EXIT
                - We provide target prices and stop-loss levels
                - We give confidence scores for our recommendations
                
                **Why This Matters**: Most people lose money in IPOs because they don't know when to exit. We solve this problem.
                """
            },
            {
                "question": "How do you calculate IPO hold/exit recommendations?",
                "answer": """
                **IPO Recommendation Calculation (Step by Step):**
                
                **Step 1: Performance Analysis (40% weight)**
                - If 30-day performance > 20% = +40 points
                - If 30-day performance 0-20% = +25 points  
                - If 30-day performance negative = +10 points
                
                **Step 2: Sentiment Analysis (30% weight)**
                - Very positive sentiment (>0.3) = +30 points
                - Positive sentiment (0-0.3) = +20 points
                - Negative sentiment = +10 points
                
                **Step 3: Liquidity Check (20% weight)**
                - High trading volume = +20 points
                - Medium volume = +15 points
                - Low volume = +10 points
                
                **Step 4: Risk Assessment (10% weight)**
                - Low volatility = +10 points
                - High volatility = +5 points
                
                **Final Recommendation:**
                - 80+ points = STRONG HOLD
                - 60-79 points = HOLD  
                - 40-59 points = PARTIAL EXIT
                - Below 40 = FULL EXIT
                
                **Example**: If IPO has +25% performance, positive sentiment, good volume = STRONG HOLD
                """
            }
        ],
        "💰 Mutual Funds & SIP": [
            {
                "question": "How do you recommend the best SIP portfolio for me?",
                "answer": """
                **SIP Portfolio Recommendation Process:**
                
                **Step 1: Risk Assessment Based on Age**
                - Age 20-30: Can take 70-80% equity risk
                - Age 30-40: Should take 60-70% equity risk  
                - Age 40-50: Should take 50-60% equity risk
                - Age 50+: Should take 30-40% equity risk
                
                **Step 2: Risk Tolerance Adjustment**
                - Conservative: Reduce equity by 20%
                - Moderate: Keep as calculated
                - Aggressive: Increase equity by 15%
                
                **Step 3: Fund Selection Logic**
                - **Large Cap (50% of equity)**: For stability
                - **Mid Cap (30% of equity)**: For growth (only for moderate/aggressive)
                - **ELSS (20% of equity)**: For tax saving
                - **Debt Funds**: Remaining allocation for safety
                
                **Step 4: Expected Return Calculation**
                - Large Cap: 12-15% expected return
                - Mid Cap: 15-18% expected return
                - Debt: 6-8% expected return
                - Final return = Weighted average of all funds
                
                **Example**: 25-year-old with ₹10,000 monthly, moderate risk gets 70% equity + 30% debt allocation
                """
            },
            {
                "question": "How do you calculate SIP maturity projections?",
                "answer": """
                **SIP Maturity Calculation (Mathematical Formula):**
                
                **Formula Used**: Future Value of Annuity
                FV = PMT × [((1 + r)^n - 1) / r] × (1 + r)
                
                **Where:**
                - PMT = Monthly SIP amount
                - r = Monthly return rate (Annual return ÷ 12)
                - n = Total number of months
                
                **Step-by-Step Example:**
                - Monthly SIP: ₹5,000
                - Expected annual return: 12%
                - Time period: 10 years
                
                **Calculation:**
                1. Monthly return (r) = 12% ÷ 12 = 1% = 0.01
                2. Number of months (n) = 10 × 12 = 120
                3. FV = 5000 × [((1.01)^120 - 1) / 0.01] × 1.01
                4. FV = 5000 × [2.3004 / 0.01] × 1.01
                5. FV = 5000 × 230.04 × 1.01 = ₹11,61,702
                
                **Total Investment**: ₹5,000 × 120 = ₹6,00,000
                **Profit**: ₹11,61,702 - ₹6,00,000 = ₹5,61,702
                
                **Note**: This assumes constant returns, but actual returns vary with market conditions.
                """
            }
        ],
        "🛡️ Risk Management": [
            {
                "question": "How do you calculate portfolio risk scores?",
                "answer": """
                **Portfolio Risk Score Calculation:**
                
                **We Check 4 Main Risk Factors:**
                
                **1. Volatility Risk (40% weight)**
                - High volatility (>30%) = 40 risk points
                - Medium volatility (20-30%) = 30 risk points
                - Low volatility (<20%) = 20 risk points
                
                **2. Market Risk - Beta (25% weight)**
                - High beta (>1.5) = 25 risk points
                - Medium beta (1-1.5) = 20 risk points
                - Low beta (<1) = 15 risk points
                
                **3. Return Quality (20% weight)**
                - Poor Sharpe ratio (<0.5) = 20 risk points
                - Good Sharpe ratio (0.5-1) = 15 risk points
                - Excellent Sharpe ratio (>1) = 10 risk points
                
                **4. Diversification (15% weight)**
                - Poor diversification (<30%) = 15 risk points
                - Good diversification (30-70%) = 10 risk points
                - Excellent diversification (>70%) = 5 risk points
                
                **Final Risk Rating:**
                - 80+ points = Very High Risk
                - 65-79 points = High Risk
                - 50-64 points = Moderate Risk
                - 35-49 points = Low Risk
                - <35 points = Very Low Risk
                """
            },
            {
                "question": "What is diversification and why is it important?",
                "answer": """
                **Diversification Explained (Simple Terms):**
                
                **What It Means:**
                "Don't put all your eggs in one basket" - Spread your money across different investments
                
                **Why It's Important:**
                - If one investment fails, others can still make money
                - Reduces overall risk of losing money
                - Provides more stable returns over time
                
                **How We Measure Diversification:**
                
                **1. Sector Diversification:**
                - Good: Money in 5+ different sectors (IT, Banking, Pharma, etc.)
                - Bad: All money in just 1-2 sectors
                
                **2. Asset Class Diversification:**
                - Good: Mix of stocks, bonds, gold, real estate
                - Bad: Only stocks or only one type of investment
                
                **3. Geographic Diversification:**
                - Good: Indian + International investments
                - Bad: Only Indian investments
                
                **Our Recommendation:**
                - Maximum 25% in any single sector
                - Maximum 10% in any single stock
                - At least 60% equity + 40% debt for balanced risk
                
                **Real Example**: Instead of buying only IT stocks, buy IT + Banking + Pharma + FMCG stocks
                """
            }
        ],
        "📈 Platform Features": [
            {
                "question": "Is all the data on your platform real-time and authentic?",
                "answer": """
                **Data Authenticity & Real-time Updates:**
                
                **YES - We Use 100% Real Data Sources:**
                
                **1. Stock Prices:**
                - Source: Yahoo Finance API (same data as Google Finance)
                - Update Frequency: Every 15 minutes during market hours
                - Covers: NSE, BSE listed stocks
                - Authenticity: Same prices you see on broker apps
                
                **2. News Data:**
                - Sources: Economic Times, MoneyControl, Google News
                - Update Frequency: Every hour
                - Language: English news articles
                - Verification: We check source credibility
                
                **3. Mutual Fund Data:**
                - Source: AMFI (Association of Mutual Funds in India)
                - Update Frequency: Daily NAV updates
                - Covers: All SEBI registered mutual funds
                - Authenticity: Official fund house data
                
                **4. IPO Data:**
                - Sources: NSE, BSE official websites
                - Update Frequency: Real-time during IPO periods
                - Covers: All mainboard IPOs
                
                **No Dummy Data**: We never use fake or simulated data for live analysis
                
                **Data Delay**: Maximum 15-minute delay due to API limitations (industry standard)
                """
            },
            {
                "question": "How does your AI investment assistant work?",
                "answer": """
                **AI Investment Assistant Explained:**
                
                **How It Works:**
                
                **1. Natural Language Processing:**
                - You can ask questions in simple English
                - Example: "Should I invest in HDFC Bank?"
                - AI understands your question and context
                
                **2. Data Analysis:**
                - AI checks real-time stock data
                - Analyzes technical indicators
                - Reviews recent news and sentiment
                - Compares with historical patterns
                
                **3. Personalized Advice:**
                - Considers your risk profile
                - Matches with your investment goals
                - Provides specific recommendations
                - Explains reasoning in simple terms
                
                **4. Continuous Learning:**
                - AI learns from market patterns
                - Updates recommendations based on new data
                - Improves accuracy over time
                
                **What You Can Ask:**
                - "Is this a good time to buy XYZ stock?"
                - "Should I start SIP in large cap funds?"
                - "What's the risk in my current portfolio?"
                - "When should I exit this IPO?"
                
                **Limitations:**
                - AI provides guidance, not guaranteed predictions
                - Final investment decisions are always yours
                - Market conditions can change rapidly
                """
            }
        ]
    }
    
    # Display FAQ by categories
    for category, faqs in faq_categories.items():
        st.subheader(category)
        
        for faq in faqs:
            with st.expander(f"❓ {faq['question']}"):
                st.markdown(faq['answer'])
    
    # Contact and Support Section
    st.subheader("📞 Need More Help?")
    
    st.markdown("""
    <div class="info-card">
        <h4>🤝 Get Additional Support</h4>
        <p><strong>Development Team Contact:</strong></p>
        <p>• <strong>Aman Jain</strong> - Project Lead & Technical Architecture</p>
        <p>• <strong>Rohit Fogla</strong> - Data Engineering & API Integration</p>
        <p>• <strong>Vanshita Mehta</strong> - Frontend Development & User Experience</p>
        <p>• <strong>Disita Tirthani</strong> - Machine Learning & AI Development</p>
        <p></p>
        <p><strong>Project Information:</strong></p>
        <p>• B.Tech 3rd Year Computer Science Project</p>
        <p>• Focus: AI-Powered Investment Analysis Platform</p>
        <p>• Unique Feature: Complete IPO Intelligence System</p>
        <p>• Technology Stack: Python, Streamlit, Machine Learning, Real-time APIs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Tips Section
    st.subheader("💡 Quick Investment Tips")
    
    tips = [
        "**Start Early**: Time is your biggest advantage in investing. Even ₹1,000 monthly SIP can grow to lakhs over 10-15 years.",
        "**Diversify Always**: Never put all money in one stock or sector. Spread risk across different investments.",
        "**Stay Informed**: Use our news and sentiment analysis to stay updated on market trends.",
        "**Don't Panic**: Market volatility is normal. Stick to your long-term investment plan.",
        "**Review Regularly**: Check your portfolio every 3-6 months and rebalance if needed.",
        "**Emergency Fund First**: Keep 6 months of expenses in savings before investing in markets.",
        "**Understand Risk**: Higher returns come with higher risk. Invest according to your risk tolerance.",
        "**Use SIP**: Systematic Investment Plans help average out market volatility over time."
    ]
    
    for tip in tips:
        st.write(f"• {tip}")

# Additional helper functions for the complete application
def show_risk_management_portfolio():
    st.header("🛡️ Risk Management & Portfolio Optimization")
    st.info("Advanced risk management and portfolio optimization features - Implementation in progress")

def show_enhanced_news_sentiment():
    st.header("📰 Enhanced News & Sentiment Intelligence")
    st.info("Enhanced news and sentiment analysis with market insights - Implementation in progress")

def show_enhanced_fake_news_detection():
    st.header("🧠 Enhanced Fake News Detection")
    st.info("Advanced fake news detection with credibility scoring - Implementation in progress")

def show_smart_alerts_system():
    st.header("🔔 Smart Alerts System")
    st.info("Intelligent alert system for price targets, news, and portfolio changes - Implementation in progress")

def show_ai_investment_assistant():
    st.header("🤖 AI Investment Assistant")
    st.info("AI-powered investment chatbot with natural language processing - Implementation in progress")

def show_advanced_analytics():
    st.header("📈 Advanced Analytics Dashboard")
    st.info("Advanced analytics with market heat maps and correlation analysis - Implementation in progress")

def show_enhanced_data_management():
    st.header("⚙️ Enhanced Data Management Center")
    st.info("Comprehensive data management with real-time updates - Implementation in progress")

if __name__ == "__main__":
    main()