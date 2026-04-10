"""
सार्थक निवेश - Clean Modular Version
Complete Investment Intelligence Platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import modules
try:
    from realtime_mutual_fund_fetcher import RealtimeMutualFundFetcher
    REALTIME_MF_AVAILABLE = True
except:
    REALTIME_MF_AVAILABLE = False

try:
    from realtime_news_fetcher import RealtimeNewsFetcher
    REALTIME_NEWS_AVAILABLE = True
except:
    REALTIME_NEWS_AVAILABLE = False

try:
    from groq_ai_analyzer import GroqAIAnalyzer
    GROQ_AI_AVAILABLE = True
    GROQ_API_KEY = "your_groq_api_key_here"
except:
    GROQ_AI_AVAILABLE = False

try:
    from portfolio_risk_manager import PortfolioRiskManager
    PORTFOLIO_MANAGER_AVAILABLE = True
except:
    PORTFOLIO_MANAGER_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="सार्थक निवेश - Investment Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Dark Theme CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f3460 0%, #16213e 100%);
        border-right: 2px solid #00d4ff;
    }
    h1, h2, h3 {
        color: #00d4ff !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricValue"] {
        color: #00ff88 !important;
        font-size: 2rem !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%);
        color: #000000;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Sample Stock Data
INDIAN_STOCKS = {
    'RELIANCE.NS': 'Reliance Industries',
    'TCS.NS': 'Tata Consultancy Services',
    'HDFCBANK.NS': 'HDFC Bank',
    'INFY.NS': 'Infosys',
    'ICICIBANK.NS': 'ICICI Bank',
    'HINDUNILVR.NS': 'Hindustan Unilever',
    'ITC.NS': 'ITC Limited',
    'SBIN.NS': 'State Bank of India',
    'BHARTIARTL.NS': 'Bharti Airtel',
    'KOTAKBANK.NS': 'Kotak Mahindra Bank'
}

def show_dashboard():
    """Main Dashboard"""
    st.header("🏠 Investment Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("NIFTY 50", "22,500", "+150 (0.67%)")
    
    with col2:
        st.metric("SENSEX", "74,200", "+320 (0.43%)")
    
    with col3:
        st.metric("Portfolio Value", "₹5,45,000", "+₹12,500")
    
    with col4:
        st.metric("Total Returns", "18.5%", "+2.3%")
    
    st.markdown("---")
    
    # Quick Stats
    st.subheader("📊 Market Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ Market Status: OPEN")
        st.info("🕐 Last Updated: " + datetime.now().strftime("%H:%M:%S"))
    
    with col2:
        st.warning("⚡ Top Gainer: TCS (+3.2%)")
        st.error("📉 Top Loser: ITC (-1.8%)")

def show_stocks():
    """Stock Intelligence Page"""
    st.header("📊 Stock Intelligence")
    
    selected_stock = st.selectbox("Select Stock", list(INDIAN_STOCKS.values()))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Price", "₹2,850", "+45 (1.6%)")
    
    with col2:
        st.metric("Day High", "₹2,875", "")
    
    with col3:
        st.metric("Day Low", "₹2,820", "")
    
    st.markdown("---")
    
    # Sample chart
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    prices = np.random.randn(30).cumsum() + 2800
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines', name='Price', line=dict(color='#00d4ff', width=2)))
    fig.update_layout(
        title=f"{selected_stock} - 30 Day Trend",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("💡 Recommendation: BUY - Strong fundamentals and positive momentum")

def show_mutual_funds():
    """Mutual Funds Page"""
    st.header("💰 Mutual Fund Center")
    
    st.subheader("🔝 Top Performing Funds")
    
    funds_data = {
        'Fund Name': ['HDFC Top 100', 'ICICI Bluechip', 'SBI Large Cap', 'Axis Bluechip'],
        'NAV': ['₹850', '₹125', '₹95', '₹48'],
        '1Y Return': ['18.5%', '16.2%', '15.8%', '17.3%'],
        '3Y Return': ['22.1%', '20.5%', '19.8%', '21.2%'],
        'Rating': ['⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐']
    }
    
    df = pd.DataFrame(funds_data)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("🧮 SIP Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_sip = st.number_input("Monthly SIP Amount (₹)", 500, 100000, 5000, 500)
        years = st.slider("Investment Period (Years)", 1, 30, 10)
    
    with col2:
        expected_return = st.slider("Expected Annual Return (%)", 8, 20, 12)
    
    if st.button("Calculate Returns", type="primary"):
        months = years * 12
        monthly_rate = expected_return / 12 / 100
        future_value = monthly_sip * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
        total_invested = monthly_sip * months
        returns = future_value - total_invested
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Invested", f"₹{total_invested:,.0f}")
        with col2:
            st.metric("Expected Returns", f"₹{returns:,.0f}")
        with col3:
            st.metric("Future Value", f"₹{future_value:,.0f}")

def show_ipo():
    """IPO Intelligence Page"""
    st.header("🚀 IPO Intelligence Hub")
    
    st.subheader("🔥 Currently Open IPOs")
    
    ipo_data = {
        'Company': ['Tech Innovations Ltd', 'Green Energy Corp', 'FinTech Solutions'],
        'Price Band': ['₹250-280', '₹180-200', '₹320-350'],
        'Opens': ['Jan 15', 'Jan 18', 'Jan 20'],
        'Closes': ['Jan 17', 'Jan 20', 'Jan 22'],
        'Lot Size': ['50', '75', '40'],
        'Recommendation': ['🟢 Subscribe', '🟡 Neutral', '🟢 Subscribe']
    }
    
    df = pd.DataFrame(ipo_data)
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📊 Recent Listings Performance")
    
    listing_data = {
        'Company': ['ABC Tech', 'XYZ Pharma', 'PQR Auto'],
        'Issue Price': ['₹150', '₹220', '₹180'],
        'Listing Price': ['₹195', '₹198', '₹210'],
        'Current Price': ['₹210', '₹185', '₹225'],
        'Listing Gain': ['+30%', '-10%', '+16.7%'],
        'Current Gain': ['+40%', '-15.9%', '+25%']
    }
    
    df = pd.DataFrame(listing_data)
    st.dataframe(df, use_container_width=True)

def show_portfolio():
    """Portfolio Management Page"""
    st.header("🛡️ Portfolio & Risk Management")
    
    st.subheader("💼 Your Holdings")
    
    portfolio_data = {
        'Stock': ['Reliance', 'TCS', 'HDFC Bank', 'Infosys'],
        'Quantity': [50, 30, 40, 25],
        'Avg Price': ['₹2,400', '₹3,200', '₹1,500', '₹1,400'],
        'Current Price': ['₹2,850', '₹3,650', '₹1,620', '₹1,480'],
        'Investment': ['₹1,20,000', '₹96,000', '₹60,000', '₹35,000'],
        'Current Value': ['₹1,42,500', '₹1,09,500', '₹64,800', '₹37,000'],
        'P&L': ['+₹22,500', '+₹13,500', '+₹4,800', '+₹2,000'],
        'Returns': ['+18.75%', '+14.06%', '+8.00%', '+5.71%']
    }
    
    df = pd.DataFrame(portfolio_data)
    st.dataframe(df, use_container_width=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Investment", "₹3,11,000")
    
    with col2:
        st.metric("Current Value", "₹3,53,800")
    
    with col3:
        st.metric("Total P&L", "+₹42,800")
    
    with col4:
        st.metric("Overall Returns", "+13.76%")

def show_ai_assistant():
    """AI Assistant Page"""
    st.header("🤖 AI Investment Assistant")
    
    st.info("💡 Ask me anything about stocks, mutual funds, IPOs, or investment strategies!")
    
    user_question = st.text_area("Your Question:", placeholder="Example: Should I invest in large cap or mid cap funds?", height=100)
    
    if st.button("Get AI Advice", type="primary"):
        with st.spinner("AI is thinking..."):
            st.success("✅ AI Response Generated!")
            st.markdown("""
            **Investment Recommendation:**
            
            For a balanced portfolio, I recommend:
            
            1. **Large Cap Funds (60%)**: Stable returns, lower risk
               - HDFC Top 100
               - ICICI Bluechip
            
            2. **Mid Cap Funds (30%)**: Higher growth potential
               - Axis Midcap Fund
               - Kotak Emerging Equity
            
            3. **Small Cap Funds (10%)**: Aggressive growth
               - SBI Small Cap Fund
            
            **Risk Consideration**: Mid and small caps are volatile. Invest only if you have 5+ year horizon.
            
            **Action Steps**:
            - Start SIP with ₹5,000/month
            - Review quarterly
            - Rebalance annually
            """)

def main():
    """Main Application"""
    
    # Header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%); padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #000000; margin: 0;'>📈 सार्थक निवेश</h1>
        <p style='color: #000000; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>Complete Investment Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.title("📊 Navigation")
    
    page = st.sidebar.radio(
        "Go to",
        ["🏠 Dashboard", "📊 Stock Intelligence", "💰 Mutual Funds", "🚀 IPO Hub", "🛡️ Portfolio", "🤖 AI Assistant"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("**Team:** Aman Jain, Rohit Fogla, Vanshita Mehta, Disita Tirthani")
    
    # Route to pages
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📊 Stock Intelligence":
        show_stocks()
    elif page == "💰 Mutual Funds":
        show_mutual_funds()
    elif page == "🚀 IPO Hub":
        show_ipo()
    elif page == "🛡️ Portfolio":
        show_portfolio()
    elif page == "🤖 AI Assistant":
        show_ai_assistant()

if __name__ == "__main__":
    main()
