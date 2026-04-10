# सार्थक निवेश - Professional-Grade Financial Platform
# Institutional-quality platform for financial experts and retail investors
# Team: Aman Jain, Rohit Fogla, Vanshita Mehta, Disita Tirthani

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3
import os
import numpy as np

# Import professional-grade modules
from config import *
from data_collector import DataCollector
from professional_analyzer import ProfessionalFinancialAnalyzer
from risk_management import InstitutionalRiskManager
from market_intelligence import AdvancedMarketIntelligence
from sentiment_analyzer import AdvancedSentimentAnalyzer
from excel_manager import ExcelExportManager

# Page Configuration
st.set_page_config(
    page_title="सार्थक निवेश - Professional Platform",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MAXIMUM TEXT VISIBILITY + PROFESSIONAL STYLING
st.markdown("""
<style>
    /* GLOBAL TEXT VISIBILITY - HIGHEST PRIORITY */
    * {
        font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
    }
    
    /* STREAMLIT APP BACKGROUND */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* ALL TEXT ELEMENTS - MAXIMUM CONTRAST */
    h1, h2, h3, h4, h5, h6, p, div, span, label, .stMarkdown {
        color: #000000 !important;
        font-weight: 600 !important;
        line-height: 1.6 !important;
    }
    
    /* HEADING SIZES - CLEAR HIERARCHY */
    h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
    h2 { font-size: 2rem !important; font-weight: 700 !important; }
    h3 { font-size: 1.5rem !important; font-weight: 700 !important; }
    h4 { font-size: 1.25rem !important; font-weight: 700 !important; }
    h5 { font-size: 1.1rem !important; font-weight: 600 !important; }
    h6 { font-size: 1rem !important; font-weight: 600 !important; }
    
    /* PROFESSIONAL HEADER - CLEAR TEXT */
    .professional-header {
        background: #ffffff !important;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        border: 3px solid #1e40af;
    }
    
    .professional-header h1 {
        color: #1e40af !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 1px !important;
        text-shadow: none !important;
    }
    
    .professional-header h2 {
        color: #000000 !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        margin-top: 0.5rem !important;
        text-shadow: none !important;
    }
    
    .professional-header .badge {
        background: #fbbf24 !important;
        color: #000000 !important;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 1rem !important;
        font-weight: 700 !important;
        margin: 0.5rem;
        display: inline-block;
        border: 2px solid #000000;
    }
    
    /* SIDEBAR - CLEAR TEXT */
    .css-1d391kg {
        background-color: #f8f9fa !important;
    }
    
    .css-1d391kg * {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* BUTTONS - HIGH CONTRAST */
    .stButton > button {
        background: #1e40af !important;
        color: #ffffff !important;
        border: 2px solid #1e40af !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    .stButton > button:hover {
        background: #1e3a8a !important;
        border-color: #1e3a8a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3) !important;
    }
    
    /* SELECTBOX - CLEAR TEXT */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 2px solid #1e40af !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox label {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    /* METRICS - HIGH CONTRAST */
    .metric-container {
        background-color: #ffffff !important;
        border: 2px solid #1e40af !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    .metric-container label {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    
    .metric-container div {
        color: #1e40af !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
    }
    
    /* DATAFRAMES - CLEAR TABLES */
    .dataframe {
        border: 2px solid #1e40af !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        background-color: #ffffff !important;
    }
    
    .dataframe th {
        background-color: #1e40af !important;
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
    
    /* ALERT MESSAGES - HIGH CONTRAST */
    .stSuccess {
        background-color: #ffffff !important;
        border: 3px solid #16a34a !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stInfo {
        background-color: #ffffff !important;
        border: 3px solid #2563eb !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stWarning {
        background-color: #ffffff !important;
        border: 3px solid #d97706 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stError {
        background-color: #ffffff !important;
        border: 3px solid #dc2626 !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* SPINNER TEXT */
    .stSpinner > div {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
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
    
    /* PROFESSIONAL CARDS */
    .professional-card {
        background: #ffffff !important;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #1e40af;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .professional-card h4 {
        color: #1e40af !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .professional-card p {
        color: #000000 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        line-height: 1.6 !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Professional Header
    st.markdown(f"""
    <div class="professional-header">
        <h1>🏆 {PROJECT_NAME}</h1>
        <h2>Professional-Grade Financial Intelligence Platform</h2>
        <div class="badge">INSTITUTIONAL QUALITY</div>
        <div class="badge">REAL-TIME ANALYTICS</div>
        <div class="badge">RISK MANAGEMENT</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional Sidebar
    st.sidebar.title("🎯 Professional Dashboard")
    st.sidebar.markdown("**Institutional-Grade Features**")
    
    page = st.sidebar.selectbox(
        "Select Professional Module",
        [
            "🏆 Executive Dashboard",
            "📊 Professional Stock Analysis", 
            "🛡️ Risk Management Center",
            "🧠 Market Intelligence Hub",
            "📈 Advanced Portfolio Analytics",
            "🚀 IPO Intelligence (Unique)",
            "📰 Sentiment & News Intelligence",
            "📋 Professional Reports",
            "⚙️ Data Management"
        ]
    )
    
    # Initialize professional modules
    if 'professional_analyzer' not in st.session_state:
        st.session_state.professional_analyzer = ProfessionalFinancialAnalyzer()
    if 'risk_manager' not in st.session_state:
        st.session_state.risk_manager = InstitutionalRiskManager()
    if 'market_intelligence' not in st.session_state:
        st.session_state.market_intelligence = AdvancedMarketIntelligence()
    if 'sentiment_analyzer' not in st.session_state:
        st.session_state.sentiment_analyzer = AdvancedSentimentAnalyzer()
    if 'excel_manager' not in st.session_state:
        st.session_state.excel_manager = ExcelExportManager()
    
    # Route to professional modules
    if page == "🏆 Executive Dashboard":
        show_executive_dashboard()
    elif page == "📊 Professional Stock Analysis":
        show_professional_stock_analysis()
    elif page == "🛡️ Risk Management Center":
        show_risk_management_center()
    elif page == "🧠 Market Intelligence Hub":
        show_market_intelligence_hub()
    elif page == "📈 Advanced Portfolio Analytics":
        show_portfolio_analytics()
    elif page == "🚀 IPO Intelligence (Unique)":
        show_ipo_intelligence()
    elif page == "📰 Sentiment & News Intelligence":
        show_sentiment_intelligence()
    elif page == "📋 Professional Reports":
        show_professional_reports()
    elif page == "⚙️ Data Management":
        show_data_management()

def show_executive_dashboard():
    st.header("🏆 Executive Dashboard - Market Overview")
    
    # Professional metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Market Status", "ACTIVE", "Real-time")
    with col2:
        st.metric("Data Quality", "99.8%", "+0.2%")
    with col3:
        st.metric("Risk Level", "MODERATE", "Stable")
    with col4:
        st.metric("Opportunities", "12", "+3")
    
    # Market Intelligence Summary
    if st.button("🧠 Generate Market Intelligence Report", type="primary"):
        with st.spinner("Generating comprehensive market intelligence..."):
            intelligence = st.session_state.market_intelligence.comprehensive_market_analysis()
            
            if intelligence:
                st.success("✅ Market Intelligence Report Generated!")
                
                # Market Overview
                st.subheader("📊 Market Overview")
                market_overview = intelligence.get('market_overview', {})
                
                if 'overall_sentiment' in market_overview:
                    sentiment = market_overview['overall_sentiment']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Market Direction", sentiment.get('market_direction', 'N/A'))
                    with col2:
                        st.metric("Market Volatility", sentiment.get('market_volatility', 'N/A'))
                    with col3:
                        st.metric("Market Strength", sentiment.get('market_strength', 'N/A'))
                
                # Professional Insights
                insights = intelligence.get('professional_insights', [])
                if insights:
                    st.subheader("💡 Professional Insights")
                    for insight in insights[:5]:
                        st.info(f"• {insight}")
                
                # Action Recommendations
                recommendations = intelligence.get('action_recommendations', {})
                if recommendations:
                    st.subheader("🎯 Action Recommendations")
                    
                    immediate = recommendations.get('immediate_actions', [])
                    if immediate:
                        st.write("**Immediate Actions:**")
                        for action in immediate:
                            st.warning(f"⚡ {action}")

def show_professional_stock_analysis():
    st.header("📊 Professional Stock Analysis")
    
    # Stock selection with professional interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_stock = st.selectbox(
            "Select Stock for Professional Analysis",
            options=list(STOCK_SYMBOLS.keys()),
            format_func=lambda x: f"{STOCK_SYMBOLS[x]} ({x})"
        )
    
    with col2:
        analysis_depth = st.selectbox(
            "Analysis Depth",
            ["Standard", "Comprehensive", "Institutional"],
            index=2
        )
    
    if st.button("🔬 Conduct Professional Analysis", type="primary"):
        with st.spinner("Conducting institutional-grade analysis..."):
            metrics = st.session_state.professional_analyzer.calculate_advanced_metrics(selected_stock)
            
            if metrics:
                st.success(f"✅ Professional analysis completed for {STOCK_SYMBOLS[selected_stock]}")
                
                # Investment Grade Display
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Investment Grade", metrics['investment_grade'])
                with col2:
                    st.metric("Recommendation", metrics['recommendation'])
                with col3:
                    st.metric("Confidence Score", f"{metrics['confidence_score']}%")
                with col4:
                    st.metric("Risk Rating", metrics['risk_rating'])
                
                # Professional Metrics
                st.subheader("📈 Professional Financial Metrics")
                
                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                
                with metrics_col1:
                    st.write("**Risk-Adjusted Returns**")
                    st.write(f"Sharpe Ratio: {metrics['sharpe_ratio']}")
                    st.write(f"Sortino Ratio: {metrics['sortino_ratio']}")
                    st.write(f"Treynor Ratio: {metrics['treynor_ratio']}")
                    st.write(f"Information Ratio: {metrics['information_ratio']}")
                
                with metrics_col2:
                    st.write("**Risk Metrics**")
                    st.write(f"Beta: {metrics['beta']}")
                    st.write(f"Alpha: {metrics['alpha']}%")
                    st.write(f"Volatility: {metrics['volatility_annualized']:.2f}%")
                    st.write(f"Max Drawdown: {metrics['max_drawdown']:.2f}%")
                
                with metrics_col3:
                    st.write("**Value at Risk**")
                    st.write(f"VaR (95%): {metrics['var_95']:.2f}%")
                    st.write(f"VaR (99%): {metrics['var_99']:.2f}%")
                    st.write(f"CVaR (95%): {metrics['cvar_95']:.2f}%")
                    st.write(f"CVaR (99%): {metrics['cvar_99']:.2f}%")

if __name__ == "__main__":
    main()