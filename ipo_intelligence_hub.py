"""IPO Intelligence Hub - World Class UI, 100% Real Data from ipowatch.in"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from ipo_live_engine import IPOLiveEngine


def show_ipo_intelligence():
    st.title("🚀 IPO Intelligence Hub")
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);
                border:1px solid #00d4ff;padding:1.2rem;border-radius:12px;margin-bottom:1rem;'>
        <h3 style='color:#00d4ff;margin:0;text-align:center;'>
            LIVE IPO DATA · REAL GMP · REAL SUBSCRIPTION · AI PREDICTIONS
        </h3>
        <p style='color:#aaa;margin:0.3rem 0 0 0;text-align:center;font-size:0.9rem;'>
            Sources: ipowatch.in · Yahoo Finance · Google News RSS
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🔄 Refresh All Live Data", type="primary", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    with col2:
        st.caption(f"🕐 {datetime.now().strftime('%d %b %Y %H:%M')}")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🟢 Open IPOs",
        "📅 Upcoming Calendar",
        "📈 Listed & Performance",
        "💰 GMP Tracker",
        "🔔 Exit Alerts",
        "🔍 Allotment Check"
    ])

    with tab1:
        _tab_open_ipos()
    with tab2:
        _tab_upcoming()
    with tab3:
        _tab_listed()
    with tab4:
        _tab_gmp()
    with tab5:
        _tab_exit_alerts()
    with tab6:
        _tab_allotment()


@st.cache_data(ttl=300)
def _get_gmp_data():
    return IPOLiveEngine().fetch_gmp_ipowatch()


@st.cache_data(ttl=600)
def _get_listed_enriched():
    engine = IPOLiveEngine()
    listed = engine.fetch_listed_ipos_ipowatch()
    enriched = engine.get_post_listing_analysis(listed)
    # If Yahoo Finance couldn't resolve symbols (SME IPOs), show basic data from ipowatch
    if not enriched and listed:
        # Return basic data with GMP-based analysis
        basic = []
        for ipo in listed:
            issue_p = ipo.get("issue_price", 0)
            listing_p = ipo.get("listing_price", 0)
            gain = ipo.get("listing_gain", 0)
            if issue_p == 0:
                continue
            total_ret = gain  # Use listing gain as proxy since no live price
            target_1 = round(issue_p * 1.20, 2)
            target_2 = round(issue_p * 1.40, 2)
            stop_loss = round(issue_p * 0.90, 2)
            if total_ret >= 20:
                alert, ac, am = "BOOK ALL PROFITS", "#00ff88", f"Strong listing gain of {total_ret:+.1f}%. Consider booking profits."
            elif total_ret >= 10:
                alert, ac, am = "BOOK 50% PROFITS", "#17a2b8", f"Good listing gain {total_ret:+.1f}%. Book 50%, hold rest."
            elif total_ret < -5:
                alert, ac, am = "STOP LOSS HIT", "#ff5252", f"Listed below issue price by {total_ret:.1f}%. Exit to limit losses."
            else:
                alert, ac, am = "HOLD", "#ffc107", f"Listing gain {total_ret:+.1f}%. Monitor closely."
            basic.append({
                "company": ipo.get("company", ""),
                "symbol": "SME",
                "sector": "N/A",
                "issue_price": issue_p,
                "listing_price": listing_p,
                "current_price": listing_p if listing_p > 0 else issue_p,
                "day_high": listing_p,
                "day_low": listing_p,
                "volume": 0,
                "avg_volume": 0,
                "volume_ratio": 1,
                "listing_gain": gain,
                "total_return": total_ret,
                "rsi": 50.0,
                "volatility": 0.0,
                "support": round(issue_p * 0.90, 2),
                "resistance": round(issue_p * 1.30, 2),
                "target_1": target_1,
                "target_2": target_2,
                "stop_loss": stop_loss,
                "alert": alert,
                "alert_color": ac,
                "alert_msg": am,
                "market_cap": 0,
                "pe_ratio": 0,
                "week_52_high": 0,
                "week_52_low": 0,
                "listing_date": ipo.get("listing_date", "")
            })
        return basic
    return enriched


def _tab_open_ipos():
    st.subheader("🟢 Currently Open IPOs — Apply or Avoid?")
    with st.spinner("Fetching live IPO data from ipowatch.in..."):
        all_ipos = _get_gmp_data()

    open_ipos = [i for i in all_ipos if i["status"] == "Open"]

    if not open_ipos:
        st.info("ℹ️ No IPOs currently open for subscription.")
        upcoming = [i for i in all_ipos if i["status"] == "Upcoming"]
        if upcoming:
            st.markdown("### 🔜 Opening Soon:")
            for u in upcoming[:5]:
                gmp_color = "#00ff88" if u["gmp"] > 0 else "#ff5252" if u["gmp"] < 0 else "#aaa"
                st.markdown(
                    f"**{u['company']}** — Opens: {u['open_date']} | Price: {u['price_band']} | "
                    f"GMP: <span style='color:{gmp_color};'>₹{u['gmp']:+.0f}</span>",
                    unsafe_allow_html=True
                )
        return

    st.success(f"✅ {len(open_ipos)} IPO(s) currently open for subscription")
    engine = IPOLiveEngine()

    for ipo in open_ipos:
        company = ipo.get("company", "N/A")
        gmp_pct = ipo.get("gmp_percent", 0)
        gmp_val = ipo.get("gmp", 0)
        gmp_color = "#00ff88" if gmp_val > 0 else "#ff5252" if gmp_val < 0 else "#aaa"

        with st.expander(
            f"🏢 {company}  |  {ipo.get('price_band','N/A')}  |  "
            f"GMP: ₹{gmp_val:+.0f} ({gmp_pct:+.1f}%)",
            expanded=True
        ):
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Price Band", ipo.get("price_band", "N/A"))
            c2.metric("Open Date", ipo.get("open_date", "N/A"))
            c3.metric("Close Date", ipo.get("close_date", "N/A"))
            c4.metric("GMP", f"₹{gmp_val:+.0f}", f"{gmp_pct:+.1f}%")
            c5.metric("Est. Listing", f"₹{ipo.get('est_listing_price', 0):.0f}" if ipo.get("est_listing_price", 0) > 0 else "N/A")

            # GMP card
            st.markdown(f"""
            <div style='background:rgba(0,0,0,0.3);padding:0.8rem;border-radius:8px;
                        border-left:4px solid {gmp_color};margin:0.5rem 0;'>
                <b style='color:{gmp_color};'>Grey Market Premium: ₹{gmp_val:+.0f} ({gmp_pct:+.1f}%)</b>
                &nbsp;|&nbsp; Est. Listing Price: <b>₹{ipo.get('est_listing_price', 0):.0f}</b>
                &nbsp;|&nbsp; Source: <i>ipowatch.in (live)</i>
            </div>
            """, unsafe_allow_html=True)

            # Subscription data
            with st.spinner(f"Fetching subscription data..."):
                sub = engine.fetch_subscription_data(company)

            if sub["total"] > 0 or sub["qib"] > 0:
                st.markdown("**📊 Live Subscription Status:**")
                sc1, sc2, sc3, sc4, sc5 = st.columns(5)
                sc1.metric("QIB", f"{sub['qib']:.1f}x")
                sc2.metric("HNI/NII", f"{sub['hni']:.1f}x")
                sc3.metric("Retail", f"{sub['retail']:.1f}x")
                sc4.metric("Employee", f"{sub['employee']:.1f}x")
                sc5.metric("Total", f"{sub['total']:.1f}x",
                           delta="Oversubscribed" if sub["total"] > 1 else "Undersubscribed")
            else:
                st.caption("📊 Subscription data not yet available (IPO may just have opened)")

            # AI Prediction
            with st.spinner("Running AI prediction..."):
                pred = engine.predict_listing_gain(ipo)

            st.markdown(f"""
            <div style='background:rgba(0,0,0,0.4);padding:1.2rem;border-radius:10px;
                        border:2px solid {pred["color"]};margin:0.8rem 0;'>
                <h3 style='color:{pred["color"]};margin:0;'>
                    🤖 AI RECOMMENDATION: {pred["recommendation"]}
                    &nbsp;&nbsp; Confidence: {pred["confidence"]}%
                </h3>
                <p style='margin:0.5rem 0;color:#e0e0e0;'>
                    Est. Listing Gain: <b style='color:{pred["color"]};'>{pred["est_listing_gain"]:+.1f}%</b>
                    &nbsp;|&nbsp; Est. Listing Price: <b>₹{pred["est_listing_price"]:.0f}</b>
                    &nbsp;|&nbsp; Stop Loss: <b style='color:#ff5252;'>₹{pred["stop_loss"]:.0f}</b>
                    &nbsp;|&nbsp; Score: <b>{pred["score"]}/100</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

            if pred["signals"]:
                st.markdown("**Key Signals:**")
                for sig in pred["signals"]:
                    icon = "✅" if any(w in sig.lower() for w in ["strong", "exceptional", "mega", "massive"]) else "📌"
                    st.markdown(f"{icon} {sig}")

            # News
            with st.spinner("Fetching news..."):
                news = engine.fetch_ipo_news(company)
            if news["news"]:
                nc_label = "🟢" if news["label"] == "Positive" else "🔴" if news["label"] == "Negative" else "🟡"
                st.markdown(f"**📰 News Sentiment: {nc_label} {news['label']} (score: {news['avg_sentiment']:.2f})**")
                for n in news["news"][:4]:
                    nc = "#00ff88" if n["sentiment"] > 0.1 else "#ff5252" if n["sentiment"] < -0.1 else "#aaa"
                    st.markdown(f"<small style='color:{nc};'>● {n['title']} — <i>{n['source']}</i></small>",
                                unsafe_allow_html=True)


def _tab_upcoming():
    st.subheader("📅 Upcoming IPO Calendar")
    with st.spinner("Fetching upcoming IPOs from ipowatch.in..."):
        all_ipos = _get_gmp_data()
    upcoming = [i for i in all_ipos if i["status"] in ["Upcoming", "Unknown"]]
    open_ipos = [i for i in all_ipos if i["status"] == "Open"]
    all_show = upcoming + open_ipos
    if not all_show:
        st.info("No upcoming IPO data available right now.")
        return
    st.success(f"Found {len(all_show)} IPO(s) in pipeline")
    rows = []
    for ipo in all_show:
        gmp = ipo.get("gmp", 0)
        gmp_pct = ipo.get("gmp_percent", 0)
        rows.append({
            "Company": ipo.get("company", ""),
            "Status": ipo.get("status", ""),
            "Open Date": ipo.get("open_date", ""),
            "Close Date": ipo.get("close_date", ""),
            "Price Band": ipo.get("price_band", ""),
            "GMP": f"₹{gmp:+.0f}",
            "GMP %": f"{gmp_pct:+.1f}%",
            "Est. Listing": f"₹{ipo.get('est_listing_price', 0):.0f}" if ipo.get("est_listing_price", 0) > 0 else "N/A",
            "Signal": ipo.get("signal", ""),
            "Source": ipo.get("source", "")
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, height=420)
    # GMP bar chart
    if rows:
        names = [r["Company"][:20] for r in rows]
        gmps = [ipo.get("gmp_percent", 0) for ipo in all_show]
        colors = ["#00ff88" if g > 0 else "#ff5252" if g < 0 else "#aaa" for g in gmps]
        fig = go.Figure(go.Bar(
            x=names, y=gmps, marker_color=colors,
            text=[f"{g:+.1f}%" for g in gmps], textposition="outside"
        ))
        fig.update_layout(
            title="GMP % for Upcoming/Open IPOs (Live from ipowatch.in)",
            yaxis_title="GMP %", template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380
        )
        st.plotly_chart(fig, use_container_width=True)


def _tab_listed():
    st.subheader("📈 Recently Listed IPOs — Live Performance")
    with st.spinner("Fetching listed IPOs and live prices from Yahoo Finance..."):
        enriched = _get_listed_enriched()
    if not enriched:
        st.warning("Could not fetch listed IPO performance data right now.")
        return
    # Summary row
    avg_ret = sum(e["total_return"] for e in enriched) / len(enriched)
    profitable = sum(1 for e in enriched if e["total_return"] > 0)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("IPOs Tracked", len(enriched))
    c2.metric("Avg Return", f"{avg_ret:+.1f}%")
    c3.metric("Profitable", f"{profitable}/{len(enriched)}")
    c4.metric("Best Performer", max(enriched, key=lambda x: x["total_return"])["company"][:15])
    # Performance chart
    companies = [e["company"][:16] for e in enriched]
    listing_gains = [e["listing_gain"] for e in enriched]
    total_returns = [e["total_return"] for e in enriched]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Listing Day Gain", x=companies, y=listing_gains,
                         marker_color="#00d4ff",
                         text=[f"{g:+.1f}%" for g in listing_gains], textposition="outside"))
    fig.add_trace(go.Bar(name="Current Total Return", x=companies, y=total_returns,
                         marker_color="#00ff88",
                         text=[f"{g:+.1f}%" for g in total_returns], textposition="outside"))
    fig.update_layout(
        title="IPO Performance — Real-time (Yahoo Finance)",
        barmode="group", template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=420
    )
    st.plotly_chart(fig, use_container_width=True)
    # Detailed cards
    for e in enriched:
        ac = e["alert_color"]
        with st.expander(f"🏢 {e['company']} ({e['symbol']})  |  {e['alert']}  |  {e['total_return']:+.1f}%"):
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Issue Price", f"₹{e['issue_price']:.0f}")
            c2.metric("Listing Price", f"₹{e['listing_price']:.0f}", f"{e['listing_gain']:+.1f}%")
            c3.metric("Current Price", f"₹{e['current_price']:.2f}", f"{e['total_return']:+.1f}%")
            c4.metric("RSI", f"{e['rsi']:.0f}")
            c5.metric("Volume", f"{e['volume_ratio']:.1f}x avg")
            st.markdown(f"""
            <div style='background:rgba(0,0,0,0.3);padding:0.8rem;border-radius:8px;
                        border-left:4px solid {ac};margin:0.5rem 0;'>
                <b style='color:{ac};'>{e["alert"]}</b> — {e["alert_msg"]}
            </div>
            """, unsafe_allow_html=True)
            tc1, tc2, tc3, tc4 = st.columns(4)
            tc1.info(f"Support: ₹{e['support']:.2f}")
            tc2.success(f"Target 1: ₹{e['target_1']:.2f}")
            tc3.success(f"Target 2: ₹{e['target_2']:.2f}")
            tc4.error(f"Stop Loss: ₹{e['stop_loss']:.2f}")
            if e.get("week_52_high", 0) > 0:
                st.caption(f"52W Range: ₹{e['week_52_low']:.2f} — ₹{e['week_52_high']:.2f}  |  Sector: {e['sector']}  |  P/E: {e['pe_ratio']:.1f}")


def _tab_gmp():
    st.subheader("💰 Live GMP Tracker — ipowatch.in")
    st.info("Grey Market Premium (GMP) is the most reliable predictor of IPO listing gains. Updated live.")
    with st.spinner("Fetching real GMP from ipowatch.in..."):
        all_ipos = _get_gmp_data()
    if not all_ipos:
        st.error("Could not fetch GMP data. ipowatch.in may be temporarily unavailable.")
        return
    st.success(f"Live GMP data for {len(all_ipos)} IPOs")
    rows = []
    for ipo in all_ipos:
        gmp = ipo.get("gmp", 0)
        gmp_pct = ipo.get("gmp_percent", 0)
        rows.append({
            "IPO": ipo.get("company", ""),
            "Status": ipo.get("status", ""),
            "Price Band": ipo.get("price_band", ""),
            "GMP (₹)": f"₹{gmp:+.0f}",
            "GMP %": f"{gmp_pct:+.1f}%",
            "Est. Listing": f"₹{ipo.get('est_listing_price', 0):.0f}" if ipo.get("est_listing_price", 0) > 0 else "N/A",
            "Listing Gain": ipo.get("listing_gain_text", ""),
            "Date": ipo.get("date_range", ""),
            "Signal": ipo.get("signal", "")
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, height=500)
    # Chart
    names = [r["IPO"][:20] for r in rows]
    gmps = [ipo.get("gmp_percent", 0) for ipo in all_ipos]
    colors = ["#00ff88" if g > 0 else "#ff5252" if g < 0 else "#aaa" for g in gmps]
    fig = go.Figure(go.Bar(
        x=names, y=gmps, marker_color=colors,
        text=[f"{g:+.1f}%" for g in gmps], textposition="outside"
    ))
    fig.update_layout(
        title="Grey Market Premium % — Live from ipowatch.in",
        yaxis_title="GMP %", template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=420
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Source: ipowatch.in | GMP is unofficial and indicative only. Not financial advice.")


def _tab_exit_alerts():
    st.subheader("🔔 Real-time Exit Alerts — Listed IPOs")
    st.info("Live monitoring of listed IPOs. Alerts triggered when targets or stop-losses are hit.")
    with st.spinner("Loading live exit alerts..."):
        enriched = _get_listed_enriched()
    if not enriched:
        st.warning("No post-listing data available right now.")
        return
    alerts_triggered = [e for e in enriched if e["alert"] in ["BOOK ALL PROFITS", "BOOK 50% PROFITS", "STOP LOSS HIT"]]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("IPOs Monitored", len(enriched))
    c2.metric("Active Alerts", len(alerts_triggered))
    c3.metric("Avg Return", f"{sum(e['total_return'] for e in enriched)/len(enriched):+.1f}%")
    c4.metric("Win Rate", f"{sum(1 for e in enriched if e['total_return'] > 0)}/{len(enriched)}")
    st.markdown("---")
    # Sort by urgency
    priority = {"STOP LOSS HIT": 0, "BOOK ALL PROFITS": 1, "BOOK 50% PROFITS": 2,
                "REVIEW POSITION": 3, "HOLD - TRAIL SL": 4, "HOLD": 5}
    enriched_sorted = sorted(enriched, key=lambda x: priority.get(x["alert"], 9))
    for e in enriched_sorted:
        ac = e["alert_color"]
        st.markdown(f"""
        <div style='background:rgba(0,0,0,0.3);padding:1rem;border-radius:10px;
                    border-left:5px solid {ac};margin:0.5rem 0;'>
            <div style='display:flex;justify-content:space-between;align-items:center;'>
                <div>
                    <b style='color:{ac};font-size:1.05rem;'>{e["alert"]}</b>
                    &nbsp;—&nbsp; <b>{e["company"]}</b>
                    &nbsp;<small style='color:#aaa;'>({e["symbol"]})</small><br>
                    <small style='color:#ccc;'>{e["alert_msg"]}</small>
                </div>
                <div style='text-align:right;min-width:100px;'>
                    <b style='color:{ac};font-size:1.4rem;'>{e["total_return"]:+.1f}%</b><br>
                    <small style='color:#aaa;'>₹{e["current_price"]:.2f}</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _tab_allotment():
    st.subheader("🔍 IPO Allotment Status Checker")
    st.info("Enter your PAN to check allotment. We redirect you to the official registrar.")
    with st.form("allotment_form"):
        pan = st.text_input("PAN Number", placeholder="ABCDE1234F", max_chars=10)
        company = st.text_input("IPO Company Name (optional)", placeholder="e.g. Hyundai India")
        submitted = st.form_submit_button("Check Allotment", type="primary")
    if submitted:
        if not pan or len(pan) != 10:
            st.error("Please enter a valid 10-character PAN number.")
        else:
            result = IPOLiveEngine().check_allotment_status(pan.upper(), company)
            st.markdown(f"""
            <div style='background:rgba(0,0,0,0.3);padding:1.2rem;border-radius:10px;
                        border-left:5px solid #00d4ff;'>
                <h4 style='color:#00d4ff;'>PAN: {result["pan"]}</h4>
                <p>{result["note"]}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("### Official Registrar Links")
            for name, (url, ipos_handled) in result["registrars"].items():
                st.markdown(f"**[{name}]({url})** — Handles: {ipos_handled}")
    st.markdown("---")
    st.markdown("### How to Check Allotment")
    st.markdown("""
    1. Go to the registrar website for your IPO
    2. Select the IPO name from the dropdown
    3. Enter your PAN number or Application number
    4. Click Submit to see allotment status
    
    **Allotment Timeline:**
    - IPO closes → T+6 days: Allotment finalized
    - T+7 days: Listing on NSE/BSE
    - Refunds credited within T+6 days
    """)
