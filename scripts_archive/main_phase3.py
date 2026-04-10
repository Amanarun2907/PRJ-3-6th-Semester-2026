# Sarthak Nivesh - Main Streamlit Application (Phase 3)
# Complete IPO Intelligence Implementation
# Team: Aman Jain, Rohit Fogla, Vanshita Mehta, Disita Tirthani

import os
import sqlite3
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from config import *
from data_collector import DataCollector
from excel_manager import ExcelExportManager
from ipo_data_collector import IPODataCollector
from realtime_ipo_intelligence import RealTimeIPOIntelligence
from ipo_predictor import IPOPredictionEngine
from sentiment_analyzer import AdvancedSentimentAnalyzer
from stock_analyzer import AdvancedStockAnalyzer
from risk_management import InstitutionalRiskManager
from professional_analyzer import ProfessionalFinancialAnalyzer


st.set_page_config(
    page_title=f"{PAGE_TITLE} - Phase 3",
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    * { font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important; }
    .stApp { background-color: #ffffff !important; color: #000000 !important; }
    h1, h2, h3, h4, h5, h6 { color: #000000 !important; font-weight: 700 !important; }
    p, div, span, label, .stMarkdown { color: #000000 !important; font-weight: 500 !important; }

    .phase3-header {
        background: linear-gradient(135deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border: 3px solid #FF9933;
    }
    .phase3-header h1 {
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-shadow: none !important;
        margin-bottom: 0.5rem !important;
    }
    .ipo-unique-badge {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%) !important;
        color: #ffffff !important;
        padding: 0.6rem 1.5rem;
        border-radius: 25px;
        font-size: 1rem !important;
        font-weight: 700 !important;
        border: 2px solid #ffffff;
        display: inline-block;
        margin: 0.5rem;
    }
    .ipo-card {
        background: #ffffff !important;
        padding: 1.2rem;
        border-radius: 12px;
        border: 3px solid #FF6B35;
        box-shadow: 0 4px 16px rgba(255, 107, 53, 0.2);
        margin-bottom: 1rem;
    }
    .success-alert {
        background: #ffffff !important;
        border: 3px solid #28a745 !important;
        color: #000000 !important;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.2);
    }
    /* FinTech-style section cards and metric styling for clear, formal UI */
    .phase3-section {
        background: #ffffff !important;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        padding: 1.5rem 1.75rem;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        margin-bottom: 1.5rem;
    }
    .phase3-section h3, .phase3-section h4 {
        margin-top: 0 !important;
        margin-bottom: 0.75rem !important;
    }
    .phase3-metric-row {
        margin-bottom: 1.25rem;
    }
    .phase3-metric-card {
        background: #ffffff !important;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        padding: 0.9rem 1.1rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
    }
    .phase3-metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #6B7280 !important;
        margin-bottom: 0.2rem;
    }
    .phase3-metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #111827 !important;
    }
    .phase3-metric-sub {
        font-size: 0.85rem;
        color: #6B7280 !important;
    }
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
    }
</style>
""",
    unsafe_allow_html=True,
)


def ensure_session_state():
    if "data_collector" not in st.session_state:
        st.session_state.data_collector = DataCollector()
    if "stock_analyzer" not in st.session_state:
        st.session_state.stock_analyzer = AdvancedStockAnalyzer()
    if "sentiment_analyzer" not in st.session_state:
        st.session_state.sentiment_analyzer = AdvancedSentimentAnalyzer()
    if "excel_manager" not in st.session_state:
        st.session_state.excel_manager = ExcelExportManager()
    if "ipo_intelligence" not in st.session_state:
        st.session_state.ipo_intelligence = RealTimeIPOIntelligence()
    if "ipo_data_collector" not in st.session_state:
        st.session_state.ipo_data_collector = IPODataCollector()
    if "ipo_predictor" not in st.session_state:
        st.session_state.ipo_predictor = IPOPredictionEngine()


def main():
    st.markdown(
        f"""
        <div class="phase3-header">
            <h1>{PROJECT_NAME} - Phase 3</h1>
            <h3>Complete IPO Intelligence Implementation</h3>
            <div class="ipo-unique-badge">UNIQUE FEATURE: Post-IPO Liquidity & Retail Sentiment Forecast</div>
            <p style="color: #000000; font-weight: 600; font-size: 1.1rem; margin-top: 1rem;">
                India's AI-Powered IPO Analysis Platform
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.title("Phase 3 Navigation")
    st.sidebar.markdown("Complete IPO Intelligence System")

    page = st.sidebar.selectbox(
        "Choose Analysis Type",
        [
            "Phase 3 Dashboard",
            "IPO Intelligence Hub (Unique)",
            "IPO Performance Analysis",
            "IPO Prediction Engine",
            "IPO Sentiment Analysis",
            "IPO Recommendations",
            "Advanced Stock Analysis",
            "News & Sentiment Analysis",
            "Fake News Detection",
            "Portfolio Tracker",
            "Sector Analysis",
            "Excel Reports Manager",
            "AI Assistant",
            "Data Management Center",
        ],
    )

    ensure_session_state()

    if page == "Phase 3 Dashboard":
        show_phase3_dashboard()
    elif page == "IPO Intelligence Hub (Unique)":
        show_ipo_intelligence_hub()
    elif page == "IPO Performance Analysis":
        show_ipo_performance_analysis()
    elif page == "IPO Prediction Engine":
        show_ipo_prediction_engine()
    elif page == "IPO Sentiment Analysis":
        show_ipo_sentiment_analysis()
    elif page == "IPO Recommendations":
        show_ipo_recommendations()
    elif page == "Advanced Stock Analysis":
        show_advanced_stock_analysis()
    elif page == "News & Sentiment Analysis":
        show_news_sentiment_analysis()
    elif page == "Fake News Detection":
        show_fake_news_detection()
    elif page == "Portfolio Tracker":
        show_portfolio_tracker()
    elif page == "Sector Analysis":
        show_sector_analysis()
    elif page == "Excel Reports Manager":
        show_excel_reports()
    elif page == "AI Assistant":
        show_ai_assistant()
    elif page == "Data Management Center":
        show_data_management()


def show_phase3_dashboard():
    st.header("Phase 3 Dashboard - IPO Intelligence")

    st.markdown(
        """
        <div class="success-alert">
            <h4>Phase 3: IPO Intelligence System</h4>
            <p>Real-time IPO tracking, post-listing performance, sentiment analysis, liquidity, and ML-based recommendations.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='ipo_intelligence'"
        )
        table_exists = cursor.fetchone() is not None
        conn.close()

        if not table_exists:
            st.warning("IPO Intelligence table not found. Collect IPO data first.")
            return

        conn = sqlite3.connect(DATABASE_PATH)
        summary_df = pd.read_sql_query(
            """
            SELECT
                COUNT(*) as total_ipos,
                AVG(performance_30d) as avg_30d,
                AVG(performance_90d) as avg_90d,
                COUNT(CASE WHEN recommendation = 'STRONG HOLD' THEN 1 END) as strong_holds,
                COUNT(CASE WHEN recommendation = 'HOLD' THEN 1 END) as holds,
                COUNT(CASE WHEN recommendation = 'PARTIAL EXIT' THEN 1 END) as partial_exits,
                COUNT(CASE WHEN recommendation = 'EXIT' THEN 1 END) as exits
            FROM ipo_intelligence
            """,
            conn,
        )
        conn.close()

        if summary_df.empty or summary_df.iloc[0]["total_ipos"] == 0:
            st.info("No IPO data found. Collect IPO data from Data Management Center.")
            return

        summary = summary_df.iloc[0]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total IPOs Tracked", int(summary["total_ipos"]))
        with col2:
            avg_30d = summary["avg_30d"] if summary["avg_30d"] else 0
            st.metric("Avg 30-Day Performance", f"{avg_30d:.2f}%")
        with col3:
            avg_90d = summary["avg_90d"] if summary["avg_90d"] else 0
            st.metric("Avg 90-Day Performance", f"{avg_90d:.2f}%")
        with col4:
            st.metric("Strong Hold Recommendations", int(summary["strong_holds"]))

        recommendations_data = {
            "Recommendation": ["Strong Hold", "Hold", "Partial Exit", "Exit"],
            "Count": [
                int(summary["strong_holds"]) if summary["strong_holds"] else 0,
                int(summary["holds"]) if summary["holds"] else 0,
                int(summary["partial_exits"]) if summary["partial_exits"] else 0,
                int(summary["exits"]) if summary["exits"] else 0,
            ],
        }

        if sum(recommendations_data["Count"]) > 0:
            fig = px.pie(
                values=recommendations_data["Count"],
                names=recommendations_data["Recommendation"],
                title="IPO Recommendation Distribution",
                color_discrete_sequence=["#28a745", "#17a2b8", "#ffc107", "#dc3545"],
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading IPO summary: {str(e)}")


def show_ipo_intelligence_hub():
    st.header("IPO Intelligence Hub (Unique Feature)")

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        ipo_list = pd.read_sql_query(
            "SELECT symbol, company_name FROM ipo_intelligence ORDER BY listing_date DESC",
            conn,
        )
        conn.close()

        if ipo_list.empty:
            st.info("No IPO data available. Collect IPO data first.")
            return

        selected_symbol = st.selectbox(
            "Select IPO",
            options=ipo_list["symbol"].tolist(),
            format_func=lambda x: f"{ipo_list[ipo_list['symbol'] == x]['company_name'].iloc[0]} ({x})",
        )

        if st.button("Run Comprehensive IPO Intelligence", type="primary"):
            with st.spinner("Running comprehensive IPO analysis..."):
                analysis = st.session_state.ipo_intelligence.comprehensive_ipo_analysis(
                    selected_symbol
                )

                if not analysis:
                    st.error("Unable to complete IPO analysis. Ensure price/news data is available.")
                    return

                st.success("IPO intelligence analysis completed.")

                perf = analysis.get("performance_analysis") or {}
                sent = analysis.get("sentiment_analysis") or {}
                rec = analysis.get("recommendation") or {}

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("30-Day Performance", f"{perf.get('performance_30d', 0):.2f}%")
                with col2:
                    st.metric("90-Day Performance", f"{perf.get('performance_90d', 0):.2f}%")
                with col3:
                    st.metric("Liquidity Score", f"{perf.get('liquidity_score', 0):.1f}")
                with col4:
                    st.metric("Overall Sentiment", f"{sent.get('overall_sentiment_score', 0):.3f}")

                st.subheader("Recommendation")
                if rec:
                    st.markdown(
                        f"""
                        <div class="ipo-card">
                            <h4>{rec.get('recommendation', 'N/A')}</h4>
                            <p>Confidence: {rec.get('confidence_score', 0):.1f}%</p>
                            <p>{rec.get('hold_exit_advice', '')}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.info("No recommendation available yet.")

    except Exception as e:
        st.error(f"Error loading IPO list: {str(e)}")


def show_ipo_performance_analysis():
    st.header("IPO Performance Analysis")

    st.markdown(
        """
        <div class="phase3-section">
            <h3>Real-Time Post-Listing Performance</h3>
            <p>
                This section analyzes IPO performance using <strong>live market data</strong> from Yahoo Finance.
                Use the refresh button below to pull the latest post-listing prices and volumes before reviewing
                performance across 1, 7, 30, 60, and 90 days.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Optional real-time refresh of performance metrics before loading from database
    if st.button("🔄 Refresh IPO performance from live market data"):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            ipo_symbols = pd.read_sql_query(
                "SELECT symbol FROM ipo_intelligence ORDER BY listing_date DESC", conn
            )
            conn.close()

            if ipo_symbols.empty:
                st.warning("No IPO records found in the database. Collect IPO data first from the Data Management Center.")
            else:
                with st.spinner("Updating post-listing performance for all IPOs using latest prices..."):
                    for symbol in ipo_symbols["symbol"]:
                        st.session_state.ipo_intelligence.analyze_post_ipo_performance(symbol)
                st.success("Post-IPO performance metrics refreshed using real-time market data.")
        except Exception as e:
            st.error(f"Error refreshing IPO performance data: {str(e)}")

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        ipo_df = pd.read_sql_query(
            """
            SELECT company_name, symbol, listing_date, issue_price,
                   performance_1d, performance_7d, performance_30d,
                   performance_60d, performance_90d
            FROM ipo_intelligence
            ORDER BY listing_date DESC
            """,
            conn,
        )
        conn.close()

        if ipo_df.empty:
            st.info("No IPO performance data available. Run IPO analysis first.")
            return

        st.dataframe(ipo_df, use_container_width=True)

        perf_cols = ["performance_1d", "performance_7d", "performance_30d", "performance_90d"]
        for col in perf_cols:
            ipo_df[col] = pd.to_numeric(ipo_df[col], errors="coerce")

        avg_perf = ipo_df[perf_cols].mean().dropna()
        if not avg_perf.empty:
            fig = px.bar(
                x=avg_perf.index,
                y=avg_perf.values,
                title="Average IPO Performance by Period",
                labels={"x": "Period", "y": "Average Performance (%)"},
                color=avg_perf.values,
                color_continuous_scale=["red", "yellow", "green"],
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading IPO performance data: {str(e)}")


def show_ipo_prediction_engine():
    st.header("IPO Prediction Engine")

    col1, col2 = st.columns([2, 1])

    with col1:
        if st.button("Train IPO Prediction Models", type="primary"):
            with st.spinner("Training models on real IPO data..."):
                metrics = st.session_state.ipo_predictor.train_prediction_models()
                if metrics:
                    st.success("Models trained successfully.")
                else:
                    st.error("Insufficient real IPO data to train models.")

    with col2:
        st.info(
            """
            Models:
            - 30-Day Performance
            - 90-Day Performance
            - Liquidity Score
            """
        )

    st.subheader("Predict IPO Performance")
    with st.form("ipo_prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            issue_price = st.number_input("Issue Price (INR)", min_value=1.0, value=500.0)
            issue_size = st.number_input("Issue Size (Crores)", min_value=1.0, value=2000.0)
        with col2:
            subscription_times = st.number_input("Subscription Times", min_value=0.1, value=10.0)
            sector = st.selectbox(
                "Sector",
                [
                    "Technology",
                    "Financial Services",
                    "Healthcare",
                    "Manufacturing",
                    "Real Estate",
                    "Energy",
                    "Other",
                ],
            )
            market_cap = st.selectbox("Market Cap Category", ["Large Cap", "Mid Cap", "Small Cap"])

        predict_button = st.form_submit_button("Predict IPO Performance")

    if predict_button:
        ipo_features = {
            "issue_price": issue_price,
            "issue_size_crores": issue_size,
            "subscription_times": subscription_times,
            "sector": sector,
            "market_cap_category": market_cap,
        }

        predictions = st.session_state.ipo_predictor.predict_ipo_performance(ipo_features)

        if not predictions:
            st.error("Models are not trained or insufficient real data available.")
            return

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("30-Day Prediction", f"{predictions.get('performance_30d', 0):.2f}%")
        with col2:
            st.metric("90-Day Prediction", f"{predictions.get('performance_90d', 0):.2f}%")
        with col3:
            st.metric("Liquidity Score", f"{predictions.get('liquidity', 0):.1f}")


def show_ipo_sentiment_analysis():
    st.header("IPO Sentiment Analysis")

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        available_ipos = pd.read_sql_query(
            "SELECT symbol, company_name FROM ipo_intelligence ORDER BY listing_date DESC",
            conn,
        )
        conn.close()

        if available_ipos.empty:
            st.info("No IPO data available for sentiment analysis.")
            return

        selected_ipo = st.selectbox(
            "Select IPO for Sentiment Analysis",
            options=available_ipos["symbol"].tolist(),
            format_func=lambda x: f"{available_ipos[available_ipos['symbol']==x]['company_name'].iloc[0]} ({x})",
        )

        if st.button("Analyze IPO Sentiment", type="primary"):
            with st.spinner("Analyzing real-time IPO sentiment..."):
                company_name = available_ipos[available_ipos["symbol"] == selected_ipo][
                    "company_name"
                ].iloc[0]
                sentiment_analysis = st.session_state.ipo_intelligence.analyze_ipo_sentiment(
                    selected_ipo, company_name
                )

                if not sentiment_analysis:
                    st.error("No real news data found for sentiment analysis.")
                    return

                st.success(f"Sentiment analysis completed for {company_name}")

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("News Sentiment", f"{sentiment_analysis['news_sentiment_score']:.3f}")
                with col2:
                    st.metric(
                        "Social Sentiment",
                        f"{sentiment_analysis.get('social_sentiment_score', 0):.3f}",
                    )
                with col3:
                    st.metric(
                        "Retail Sentiment",
                        f"{sentiment_analysis.get('retail_sentiment_score', 0):.3f}",
                    )
                with col4:
                    st.metric(
                        "Overall Sentiment",
                        f"{sentiment_analysis['overall_sentiment_score']:.3f}",
                    )

    except Exception as e:
        st.error(f"Error in sentiment analysis: {str(e)}")


def show_ipo_recommendations():
    st.header("IPO Recommendations")

    st.markdown(
        """
        <div class="phase3-section">
            <h3>Live Post-Listing Recommendations</h3>
            <p>
                Recommendations below are based on <strong>real-time post-listing performance, liquidity, and sentiment data</strong>.
                Click the refresh button to recalculate all recommendations using the latest prices and news before viewing them.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Allow user to refresh all IPO recommendations with up-to-date data
    if st.button("🔄 Refresh all IPO recommendations using live data"):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            ipo_symbols = pd.read_sql_query(
                "SELECT symbol FROM ipo_intelligence ORDER BY listing_date DESC", conn
            )
            conn.close()

            if ipo_symbols.empty:
                st.warning("No IPO records found in the database. Collect IPO data first from the Data Management Center.")
            else:
                with st.spinner("Running comprehensive IPO intelligence (performance + sentiment + recommendations) for all IPOs..."):
                    for symbol in ipo_symbols["symbol"]:
                        st.session_state.ipo_intelligence.comprehensive_ipo_analysis(symbol)
                st.success("All IPO recommendations updated using real-time market and news data.")
        except Exception as e:
            st.error(f"Error refreshing IPO recommendations: {str(e)}")

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        recommendations_df = pd.read_sql_query(
            """
            SELECT company_name, symbol, recommendation, confidence_score,
                   hold_exit_advice, target_price, stop_loss, risk_rating,
                   performance_30d, performance_90d, overall_sentiment_score
            FROM ipo_intelligence
            WHERE recommendation IS NOT NULL
            ORDER BY confidence_score DESC
            """,
            conn,
        )
        conn.close()

        if recommendations_df.empty:
            st.info("No recommendations available. Generate recommendations first.")
            if st.button("Generate IPO Recommendations"):
                with st.spinner("Generating recommendations..."):
                    conn = sqlite3.connect(DATABASE_PATH)
                    all_ipos = pd.read_sql_query("SELECT symbol FROM ipo_intelligence", conn)
                    conn.close()
                    for symbol in all_ipos["symbol"]:
                        st.session_state.ipo_intelligence.generate_ipo_recommendation(symbol)
                    st.success("Recommendations generated.")
            return

        for _, ipo in recommendations_df.iterrows():
            st.markdown(
                f"""
                <div class="ipo-card">
                    <h4>{ipo['company_name']} ({ipo['symbol']})</h4>
                    <p><strong>Recommendation:</strong> {ipo['recommendation']} (Confidence: {ipo['confidence_score']:.1f}%)</p>
                    <p><strong>Advice:</strong> {ipo['hold_exit_advice']}</p>
                    <p><strong>Target:</strong> INR {ipo['target_price']:.2f} |
                       <strong>Stop Loss:</strong> INR {ipo['stop_loss']:.2f} |
                       <strong>Risk:</strong> {ipo['risk_rating']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    except Exception as e:
        st.error(f"Error loading recommendations: {str(e)}")


def show_data_management():
    st.header("Data Management Center")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Collect IPO Data"):
            with st.spinner("Collecting IPO data from NSE/BSE sources..."):
                data = st.session_state.ipo_data_collector.comprehensive_ipo_data_collection()
                if data:
                    st.session_state.ipo_data_collector.update_ipo_database(data)
                    st.success(f"Collected data for {len(data)} IPOs.")
                else:
                    st.error("Unable to collect IPO data. Check connectivity or data sources.")

    with col2:
        if st.button("Run IPO Performance Analysis"):
            with st.spinner("Analyzing post-IPO performance for all IPOs..."):
                conn = sqlite3.connect(DATABASE_PATH)
                ipo_symbols = pd.read_sql_query("SELECT symbol FROM ipo_intelligence", conn)
                conn.close()
                for symbol in ipo_symbols["symbol"]:
                    st.session_state.ipo_intelligence.analyze_post_ipo_performance(symbol)
                st.success("Performance analysis completed.")

    with col3:
        if st.button("Train IPO Models"):
            with st.spinner("Training IPO prediction models..."):
                metrics = st.session_state.ipo_predictor.train_prediction_models()
                if metrics:
                    st.success("Models trained.")
                else:
                    st.error("Not enough real data to train models.")

    st.subheader("Database Status")
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        stock_count = pd.read_sql_query("SELECT COUNT(*) as count FROM stock_prices", conn).iloc[0][
            "count"
        ]
        news_count = pd.read_sql_query("SELECT COUNT(*) as count FROM news_articles", conn).iloc[0][
            "count"
        ]
        ipo_count = pd.read_sql_query("SELECT COUNT(*) as count FROM ipo_intelligence", conn).iloc[0][
            "count"
        ]
        conn.close()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Stock Records", f"{stock_count:,}")
        with col2:
            st.metric("News Articles", f"{news_count:,}")
        with col3:
            st.metric("IPO Records", f"{ipo_count:,}")

    except Exception as e:
        st.error(f"Database error: {str(e)}")


def show_advanced_stock_analysis():
    st.header("Advanced Stock Analysis")
    st.info("Available in Phase 2 application.")


def show_news_sentiment_analysis():
    st.header("News & Sentiment Analysis")
    st.info("Available in Phase 2 application.")


def show_fake_news_detection():
    st.header("Fake News Detection")
    st.info("Available in Phase 2 application.")


def show_portfolio_tracker():
    st.header("Portfolio Tracker")
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
            with st.form("add_holding_form_p3"):
                symbol = st.selectbox("Stock", options=list(STOCK_SYMBOLS.keys()), format_func=lambda x: f"{STOCK_SYMBOLS[x]} ({x})")
                quantity = st.number_input("Quantity", min_value=0.0, step=1.0, format="%.2f", key="qty_p3")
                buy_price = st.number_input("Buy Price (₹)", min_value=0.0, step=0.5, format="%.2f", key="price_p3")
                buy_date = st.date_input("Buy Date", key="date_p3")
                notes = st.text_input("Notes", value="", key="notes_p3")
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
                    if st.button("Remove Selected", key="remove_p3"):
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
        if st.button("Generate Stock Recommendations", key="recs_p3"):
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


def show_sector_analysis():
    st.header("Sector Analysis")
    st.info("Available in Phase 2 application.")


def show_excel_reports():
    st.header("Excel Reports Manager")
    st.info("Available in Phase 2 application.")


def show_ai_assistant():
    st.header("AI Assistant")
    st.info("Coming in Phase 5.")


if __name__ == "__main__":
    main()
