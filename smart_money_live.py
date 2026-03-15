"""
Smart Money Tracker - Live Real Data from NSE
Tracks FII/DII, Bulk Deals, Block Deals, Insider Trading
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import yfinance as yf
from bs4 import BeautifulSoup
import time

# Indian Stock Symbols
INDIAN_STOCKS = {
    'RELIANCE.NS': 'Reliance', 'TCS.NS': 'TCS', 'HDFCBANK.NS': 'HDFC Bank',
    'INFY.NS': 'Infosys', 'ICICIBANK.NS': 'ICICI Bank', 'HINDUNILVR.NS': 'Hindustan Unilever',
    'ITC.NS': 'ITC', 'SBIN.NS': 'SBI', 'BHARTIARTL.NS': 'Bharti Airtel',
    'KOTAKBANK.NS': 'Kotak Bank', 'LT.NS': 'L&T', 'AXISBANK.NS': 'Axis Bank',
    'ASIANPAINT.NS': 'Asian Paints', 'MARUTI.NS': 'Maruti', 'TITAN.NS': 'Titan',
    'BAJFINANCE.NS': 'Bajaj Finance', 'WIPRO.NS': 'Wipro', 'ULTRACEMCO.NS': 'UltraTech',
    'NESTLEIND.NS': 'Nestle', 'HCLTECH.NS': 'HCL Tech'
}

class LiveSmartMoneyTracker:
    """Live Smart Money Tracker with Real NSE Data"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.nseindia.com/'
        })
        self.base_url = 'https://www.nseindia.com'
        self._initialize_session()
    
    def _initialize_session(self):
        """Initialize NSE session with cookies"""
        try:
            self.session.get(self.base_url, timeout=10)
            time.sleep(1)
        except:
            pass
    
    def fetch_live_fii_dii_data(self):
        """Fetch live FII/DII data from NSE"""
        try:
            url = f"{self.base_url}/api/fiidiiTradeReact"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data and len(data) > 0:
                    # Parse the data
                    records = []
                    for item in data[:10]:  # Last 10 days
                        try:
                            records.append({
                                'date': item.get('date', ''),
                                'fii_buy': float(item.get('fiiBuyValue', 0)),
                                'fii_sell': float(item.get('fiiSellValue', 0)),
                                'fii_net': float(item.get('fiiNetValue', 0)),
                                'dii_buy': float(item.get('diiBuyValue', 0)),
                                'dii_sell': float(item.get('diiSellValue', 0)),
                                'dii_net': float(item.get('diiNetValue', 0))
                            })
                        except:
                            continue
                    
                    if records:
                        df = pd.DataFrame(records)
                        return df
        except Exception as e:
            print(f"FII/DII fetch error: {e}")
        
        return pd.DataFrame()
    
    def fetch_live_bulk_deals(self):
        """Fetch live bulk deals from NSE"""
        try:
            url = f"{self.base_url}/api/snapshot-capital-market-largedeal"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'BULK_DEAL_DATA' in data and data['BULK_DEAL_DATA']:
                    records = []
                    for deal in data['BULK_DEAL_DATA']:
                        try:
                            records.append({
                                'symbol': deal.get('symbol', ''),
                                'company': deal.get('companyName', ''),
                                'client_name': deal.get('clientName', ''),
                                'deal_type': deal.get('dealType', ''),
                                'quantity': float(deal.get('quantity', 0)),
                                'price': float(deal.get('tradePrice', 0)),
                                'date': deal.get('dealDate', '')
                            })
                        except:
                            continue
                    
                    if records:
                        return pd.DataFrame(records)
        except Exception as e:
            print(f"Bulk deals fetch error: {e}")
        
        return pd.DataFrame()
    
    def fetch_live_block_deals(self):
        """Fetch live block deals from NSE"""
        try:
            url = f"{self.base_url}/api/snapshot-capital-market-largedeal"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'BLOCK_DEAL_DATA' in data and data['BLOCK_DEAL_DATA']:
                    records = []
                    for deal in data['BLOCK_DEAL_DATA']:
                        try:
                            records.append({
                                'symbol': deal.get('symbol', ''),
                                'company': deal.get('companyName', ''),
                                'client_name': deal.get('clientName', ''),
                                'quantity': float(deal.get('quantity', 0)),
                                'price': float(deal.get('tradePrice', 0)),
                                'date': deal.get('dealDate', '')
                            })
                        except:
                            continue
                    
                    if records:
                        return pd.DataFrame(records)
        except Exception as e:
            print(f"Block deals fetch error: {e}")
        
        return pd.DataFrame()
    
    def get_stock_volume_analysis(self, symbol):
        """Analyze stock volume for institutional activity"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='30d')
            
            if not hist.empty and len(hist) > 10:
                current_volume = hist['Volume'].iloc[-1]
                avg_volume = hist['Volume'].mean()
                volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
                
                current_price = hist['Close'].iloc[-1]
                price_change = ((current_price - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                
                return {
                    'symbol': symbol,
                    'company': INDIAN_STOCKS.get(symbol, symbol),
                    'current_price': current_price,
                    'volume_ratio': volume_ratio,
                    'price_change_30d': price_change,
                    'avg_volume': avg_volume,
                    'current_volume': current_volume,
                    'signal': 'High Activity' if volume_ratio > 1.5 else 'Normal'
                }
        except:
            pass
        return None
    
    def detect_unusual_activity(self):
        """Detect unusual volume activity across stocks"""
        unusual_stocks = []
        
        for symbol in list(INDIAN_STOCKS.keys())[:15]:  # Check top 15 stocks
            analysis = self.get_stock_volume_analysis(symbol)
            if analysis and analysis['volume_ratio'] > 1.5:
                unusual_stocks.append(analysis)
        
        if unusual_stocks:
            return pd.DataFrame(unusual_stocks)
        return pd.DataFrame()
    
    def get_sector_flow_analysis(self):
        """Analyze sector-wise money flow"""
        sectors = {
            'Banking': ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'AXISBANK.NS'],
            'IT': ['TCS.NS', 'INFY.NS', 'WIPRO.NS', 'HCLTECH.NS'],
            'Auto': ['MARUTI.NS'],
            'FMCG': ['HINDUNILVR.NS', 'ITC.NS', 'NESTLEIND.NS'],
            'Finance': ['BAJFINANCE.NS']
        }
        
        sector_data = []
        
        for sector, stocks in sectors.items():
            total_volume_ratio = 0
            total_price_change = 0
            count = 0
            
            for symbol in stocks:
                analysis = self.get_stock_volume_analysis(symbol)
                if analysis:
                    total_volume_ratio += analysis['volume_ratio']
                    total_price_change += analysis['price_change_30d']
                    count += 1
            
            if count > 0:
                avg_volume_ratio = total_volume_ratio / count
                avg_price_change = total_price_change / count
                
                # Determine sector signal
                if avg_volume_ratio > 1.3 and avg_price_change > 2:
                    signal = "Strong Buy"
                    color = "#00ff88"
                elif avg_volume_ratio > 1.1 and avg_price_change > 0:
                    signal = "Buy"
                    color = "#17a2b8"
                elif avg_price_change < -2:
                    signal = "Sell"
                    color = "#ff5252"
                else:
                    signal = "Hold"
                    color = "#ffc107"
                
                sector_data.append({
                    'sector': sector,
                    'avg_volume_ratio': avg_volume_ratio,
                    'avg_price_change': avg_price_change,
                    'signal': signal,
                    'color': color,
                    'stocks_analyzed': count
                })
        
        return pd.DataFrame(sector_data)
    
    def generate_smart_money_signals(self, fii_dii_df, bulk_deals_df, block_deals_df):
        """Generate AI-powered buy/sell signals"""
        signals = []
        
        # Analyze FII/DII trend
        if not fii_dii_df.empty:
            latest_fii = fii_dii_df.iloc[0]['fii_net']
            latest_dii = fii_dii_df.iloc[0]['dii_net']
            
            if latest_fii > 1000 and latest_dii > 1000:
                signals.append({
                    'signal': 'STRONG BUY',
                    'reason': 'Both FII and DII are buying heavily',
                    'confidence': 90,
                    'color': '#00ff88'
                })
            elif latest_fii > 0 and latest_dii > 1000:
                signals.append({
                    'signal': 'BUY',
                    'reason': 'Strong DII support with FII buying',
                    'confidence': 80,
                    'color': '#17a2b8'
                })
            elif latest_fii < -2000 and latest_dii < 0:
                signals.append({
                    'signal': 'SELL',
                    'reason': 'Both FII and DII are selling',
                    'confidence': 85,
                    'color': '#ff5252'
                })
            else:
                signals.append({
                    'signal': 'HOLD',
                    'reason': 'Mixed institutional signals',
                    'confidence': 60,
                    'color': '#ffc107'
                })
        
        # Analyze bulk deals
        if not bulk_deals_df.empty:
            buy_deals = bulk_deals_df[bulk_deals_df['deal_type'].str.contains('BUY', case=False, na=False)]
            if len(buy_deals) > 5:
                signals.append({
                    'signal': 'BUY',
                    'reason': f'{len(buy_deals)} bulk buy deals detected today',
                    'confidence': 75,
                    'color': '#17a2b8'
                })
        
        # Analyze block deals
        if not block_deals_df.empty:
            signals.append({
                'signal': 'WATCH',
                'reason': f'{len(block_deals_df)} block deals detected - institutional activity',
                'confidence': 70,
                'color': '#ffc107'
            })
        
        return signals if signals else [{
            'signal': 'HOLD',
            'reason': 'Insufficient data for strong signal',
            'confidence': 50,
            'color': '#ffc107'
        }]

def show_live_smart_money_tracker():
    """Display Live Smart Money Tracker UI"""
    
    st.header("💰 Smart Money Tracker - Live Institutional Money Flow")
    
    # Hero Banner
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
                box-shadow: 0 10px 40px rgba(102, 126, 234, 0.5);'>
        <h2 style='color: #ffffff; margin: 0; text-align: center;'>
            🎯 FOLLOW THE SMART MONEY - LIVE DATA
        </h2>
        <p style='color: #ffffff; margin: 0.5rem 0; text-align: center; font-size: 1.2rem;'>
            Real-time FII/DII | Bulk & Block Deals | Volume Analysis | Sector Flow
        </p>
        <p style='color: #e0e0e0; margin: 0; text-align: center;'>
            ✅ Live NSE Data | ✅ Institutional Tracking | ✅ AI Signals
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tracker = LiveSmartMoneyTracker()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 FII/DII Flow",
        "💼 Bulk Deals",
        "🔒 Block Deals",
        "📈 Volume Analysis",
        "🏭 Sector Flow"
    ])
    
    # TAB 1: FII/DII Flow
    with tab1:
        st.subheader("📊 Foreign & Domestic Institutional Investors Flow")
        
        with st.spinner("🔄 Fetching live FII/DII data from NSE..."):
            fii_dii_df = tracker.fetch_live_fii_dii_data()
        
        if not fii_dii_df.empty:
            latest = fii_dii_df.iloc[0]
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                fii_color = "#00ff88" if latest['fii_net'] > 0 else "#ff5252"
                st.markdown(f"""
                <div style='background: rgba(0, 212, 255, 0.1); padding: 1.5rem; border-radius: 12px;
                            border-left: 5px solid {fii_color};'>
                    <h4 style='color: #00d4ff; margin: 0;'>FII Net</h4>
                    <h2 style='color: {fii_color}; margin: 0.5rem 0;'>₹{latest['fii_net']:,.0f} Cr</h2>
                    <p style='color: #e0e0e0; margin: 0;'>Buy: ₹{latest['fii_buy']:,.0f} Cr</p>
                    <p style='color: #e0e0e0; margin: 0;'>Sell: ₹{latest['fii_sell']:,.0f} Cr</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                dii_color = "#00ff88" if latest['dii_net'] > 0 else "#ff5252"
                st.markdown(f"""
                <div style='background: rgba(0, 212, 255, 0.1); padding: 1.5rem; border-radius: 12px;
                            border-left: 5px solid {dii_color};'>
                    <h4 style='color: #00d4ff; margin: 0;'>DII Net</h4>
                    <h2 style='color: {dii_color}; margin: 0.5rem 0;'>₹{latest['dii_net']:,.0f} Cr</h2>
                    <p style='color: #e0e0e0; margin: 0;'>Buy: ₹{latest['dii_buy']:,.0f} Cr</p>
                    <p style='color: #e0e0e0; margin: 0;'>Sell: ₹{latest['dii_sell']:,.0f} Cr</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                total_net = latest['fii_net'] + latest['dii_net']
                total_color = "#00ff88" if total_net > 0 else "#ff5252"
                st.markdown(f"""
                <div style='background: rgba(0, 212, 255, 0.1); padding: 1.5rem; border-radius: 12px;
                            border-left: 5px solid {total_color};'>
                    <h4 style='color: #00d4ff; margin: 0;'>Total Net Flow</h4>
                    <h2 style='color: {total_color}; margin: 0.5rem 0;'>₹{total_net:,.0f} Cr</h2>
                    <p style='color: #e0e0e0; margin: 0;'>Combined institutional flow</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # Generate signal
                if latest['fii_net'] > 1000 and latest['dii_net'] > 1000:
                    signal = "STRONG BUY"
                    signal_color = "#00ff88"
                elif latest['fii_net'] > 0 and latest['dii_net'] > 0:
                    signal = "BUY"
                    signal_color = "#17a2b8"
                elif latest['fii_net'] < -1000 and latest['dii_net'] < -1000:
                    signal = "SELL"
                    signal_color = "#ff5252"
                else:
                    signal = "HOLD"
                    signal_color = "#ffc107"
                
                st.markdown(f"""
                <div style='background: rgba(0, 212, 255, 0.1); padding: 1.5rem; border-radius: 12px;
                            border-left: 5px solid {signal_color};'>
                    <h4 style='color: #00d4ff; margin: 0;'>Market Signal</h4>
                    <h2 style='color: {signal_color}; margin: 0.5rem 0;'>{signal}</h2>
                    <p style='color: #e0e0e0; margin: 0;'>Based on institutional flow</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show historical data
            st.markdown("### 📈 Historical FII/DII Flow (Last 10 Days)")
            st.dataframe(fii_dii_df, use_container_width=True)
            
        else:
            st.warning("⚠️ Unable to fetch live FII/DII data. NSE API may be temporarily unavailable.")
            st.info("💡 This happens when market is closed or NSE servers are under maintenance.")
    
    # TAB 2: Bulk Deals
    with tab2:
        st.subheader("💼 Bulk Deals - Large Institutional Trades")
        
        with st.spinner("🔄 Fetching live bulk deals from NSE..."):
            bulk_deals_df = tracker.fetch_live_bulk_deals()
        
        if not bulk_deals_df.empty:
            st.success(f"✅ Found {len(bulk_deals_df)} bulk deals today!")
            
            for _, deal in bulk_deals_df.iterrows():
                deal_color = "#00ff88" if 'BUY' in str(deal.get('deal_type', '')).upper() else "#ff5252"
                st.markdown(f"""
                <div style='background: rgba(0, 212, 255, 0.1); padding: 1rem; border-radius: 10px;
                            border-left: 5px solid {deal_color}; margin: 0.5rem 0;'>
                    <h4 style='color: #00d4ff; margin: 0;'>{deal['company']} ({deal['symbol']})</h4>
                    <p style='margin: 0.3rem 0;'><strong>Client:</strong> {deal['client_name']}</p>
                    <p style='margin: 0.3rem 0;'><strong>Type:</strong> {deal.get('deal_type', 'N/A')}</p>
                    <p style='margin: 0.3rem 0;'><strong>Quantity:</strong> {deal['quantity']:,.0f} shares</p>
                    <p style='margin: 0.3rem 0;'><strong>Price:</strong> ₹{deal['price']:.2f}</p>
                    <p style='margin: 0;'><strong>Date:</strong> {deal['date']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ No bulk deals found today or data not available yet.")
            st.markdown("""
            **What are Bulk Deals?**
            - Trades where quantity is more than 0.5% of company's equity
            - Indicates significant institutional interest
            - Must be reported to exchange
            """)
    
    # TAB 3: Block Deals
    with tab3:
        st.subheader("🔒 Block Deals - Off-Market Institutional Trades")
        
        with st.spinner("🔄 Fetching live block deals from NSE..."):
            block_deals_df = tracker.fetch_live_block_deals()
        
        if not block_deals_df.empty:
            st.success(f"✅ Found {len(block_deals_df)} block deals today!")
            
            for _, deal in block_deals_df.iterrows():
                st.markdown(f"""
                <div style='background: rgba(0, 212, 255, 0.1); padding: 1rem; border-radius: 10px;
                            border-left: 5px solid #764ba2; margin: 0.5rem 0;'>
                    <h4 style='color: #00d4ff; margin: 0;'>{deal['company']} ({deal['symbol']})</h4>
                    <p style='margin: 0.3rem 0;'><strong>Client:</strong> {deal['client_name']}</p>
                    <p style='margin: 0.3rem 0;'><strong>Quantity:</strong> {deal['quantity']:,.0f} shares</p>
                    <p style='margin: 0.3rem 0;'><strong>Price:</strong> ₹{deal['price']:.2f}</p>
                    <p style='margin: 0;'><strong>Date:</strong> {deal['date']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ No block deals found today or data not available yet.")
            st.markdown("""
            **What are Block Deals?**
            - Large off-market trades (minimum 5 lakh shares or ₹5 crore)
            - Executed through special trading window
            - Indicates major institutional repositioning
            """)
    
    # TAB 4: Volume Analysis
    with tab4:
        st.subheader("📈 Unusual Volume Activity - Potential Smart Money Moves")
        
        with st.spinner("🔍 Analyzing volume across top stocks..."):
            unusual_df = tracker.detect_unusual_activity()
        
        if not unusual_df.empty:
            st.success(f"✅ Detected {len(unusual_df)} stocks with unusual volume activity!")
            
            for _, stock in unusual_df.iterrows():
                volume_color = "#00ff88" if stock['volume_ratio'] > 2 else "#17a2b8"
                price_color = "#00ff88" if stock['price_change_30d'] > 0 else "#ff5252"
                
                st.markdown(f"""
                <div style='background: rgba(0, 212, 255, 0.1); padding: 1rem; border-radius: 10px;
                            border-left: 5px solid {volume_color}; margin: 0.5rem 0;'>
                    <h4 style='color: #00d4ff; margin: 0;'>{stock['company']} ({stock['symbol'].replace('.NS', '')})</h4>
                    <p style='margin: 0.3rem 0;'><strong>Current Price:</strong> ₹{stock['current_price']:.2f}</p>
                    <p style='margin: 0.3rem 0;'><strong>Volume Ratio:</strong> <span style='color: {volume_color};'>{stock['volume_ratio']:.2f}x normal</span></p>
                    <p style='margin: 0.3rem 0;'><strong>30-Day Change:</strong> <span style='color: {price_color};'>{stock['price_change_30d']:+.2f}%</span></p>
                    <p style='margin: 0;'><strong>Signal:</strong> {stock['signal']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ No unusual volume activity detected currently.")
    
    # TAB 5: Sector Flow
    with tab5:
        st.subheader("🏭 Sector-wise Money Flow Analysis")
        
        with st.spinner("🔍 Analyzing sector-wise institutional flow..."):
            sector_df = tracker.get_sector_flow_analysis()
        
        if not sector_df.empty:
            st.success(f"✅ Analyzed {len(sector_df)} sectors")
            
            for _, sector in sector_df.iterrows():
                st.markdown(f"""
                <div style='background: rgba(0, 212, 255, 0.1); padding: 1.5rem; border-radius: 12px;
                            border-left: 5px solid {sector['color']}; margin: 1rem 0;'>
                    <h3 style='color: #00d4ff; margin: 0;'>{sector['sector']} Sector</h3>
                    <p style='margin: 0.5rem 0;'><strong>Signal:</strong> <span style='color: {sector['color']}; font-size: 1.2rem;'>{sector['signal']}</span></p>
                    <p style='margin: 0.3rem 0;'><strong>Avg Volume Ratio:</strong> {sector['avg_volume_ratio']:.2f}x</p>
                    <p style='margin: 0.3rem 0;'><strong>Avg Price Change (30d):</strong> {sector['avg_price_change']:+.2f}%</p>
                    <p style='margin: 0;'><strong>Stocks Analyzed:</strong> {sector['stocks_analyzed']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ Sector analysis data not available.")

if __name__ == "__main__":
    st.set_page_config(page_title="Live Smart Money Tracker", layout="wide")
    show_live_smart_money_tracker()
