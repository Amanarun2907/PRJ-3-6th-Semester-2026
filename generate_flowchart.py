"""
Agentic AI Flowchart Generator
Generates Agentic_AI.jpg -- light theme, large text, no overlapping
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(22, 34))
ax.set_xlim(0, 22)
ax.set_ylim(0, 34)
ax.axis("off")
fig.patch.set_facecolor("#F8F9FA")
ax.set_facecolor("#F8F9FA")

# ── Color palette ─────────────────────────────────────────────────────────────
C = {
    "user":    ("#1565C0", "#E3F2FD"),   # dark blue border, light blue fill
    "input":   ("#2E7D32", "#E8F5E9"),   # green
    "router":  ("#6A1B9A", "#F3E5F5"),   # purple
    "agent":   ("#E65100", "#FFF3E0"),   # orange
    "data":    ("#00695C", "#E0F2F1"),   # teal
    "groq":    ("#AD1457", "#FCE4EC"),   # pink
    "master":  ("#1565C0", "#E3F2FD"),   # blue
    "output":  ("#1B5E20", "#C8E6C9"),   # dark green
    "arrow":   "#455A64",
}

def box(ax, x, y, w, h, text, color_key, fontsize=13, bold=False):
    border, fill = C[color_key]
    rect = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.12",
        linewidth=2.5,
        edgecolor=border,
        facecolor=fill,
        zorder=3,
    )
    ax.add_patch(rect)
    weight = "bold" if bold else "normal"
    ax.text(x, y, text, ha="center", va="center",
            fontsize=fontsize, fontweight=weight,
            color="#1A1A1A", zorder=4,
            wrap=True,
            multialignment="center")

def diamond(ax, x, y, w, h, text, fontsize=12):
    pts = [(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)]
    poly = plt.Polygon(pts, closed=True, linewidth=2.5,
                       edgecolor="#6A1B9A", facecolor="#F3E5F5", zorder=3)
    ax.add_patch(poly)
    ax.text(x, y, text, ha="center", va="center",
            fontsize=fontsize, fontweight="bold",
            color="#1A1A1A", zorder=4, multialignment="center")

def arrow(ax, x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=C["arrow"],
                    lw=2.2,
                    mutation_scale=20,
                ),
                zorder=2)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.15, my, label, fontsize=10, color="#455A64",
                ha="left", va="center", style="italic")

def harrow(ax, x1, y1, x2, y2):
    """Horizontal then vertical arrow."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=C["arrow"],
                    lw=2.0,
                    connectionstyle="arc3,rad=0.0",
                    mutation_scale=18,
                ),
                zorder=2)

# ─────────────────────────────────────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────────────────────────────────────
ax.text(11, 33.2, "Agentic AI Investment Hub  --  Complete Pipeline",
        ha="center", va="center", fontsize=20, fontweight="bold",
        color="#1A237E")
ax.text(11, 32.7, "Sarthak Nivesh  |  Aman Jain  |  B.Tech 2023-27",
        ha="center", va="center", fontsize=13, color="#455A64")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 -- USER INPUT
# ─────────────────────────────────────────────────────────────────────────────
box(ax, 11, 31.8, 9, 0.9,
    "USER  --  Types Investment Query\n"
    "e.g. 'Which stocks should I buy today?'",
    "user", fontsize=13, bold=True)

arrow(ax, 11, 31.35, 11, 30.55)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 -- QUERY ROUTER
# ─────────────────────────────────────────────────────────────────────────────
box(ax, 11, 30.1, 9, 0.85,
    "QUERY ROUTER  (FastAPI  /api/agentic/run)\n"
    "Receives query  |  Selects agents to run  |  Starts pipeline",
    "router", fontsize=12, bold=True)

arrow(ax, 11, 29.67, 11, 28.9)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 -- 6 AGENTS (side by side in 2 columns)
# ─────────────────────────────────────────────────────────────────────────────
ax.text(11, 28.65, "6 SPECIALIST AGENTS RUN IN PARALLEL",
        ha="center", va="center", fontsize=14, fontweight="bold", color="#6A1B9A")

agents = [
    ("STOCK INTELLIGENCE AGENT",
     "Fetches live prices via fast_info\nComputes RSI, MACD, Bollinger Bands\nGenerates BUY / HOLD / SELL signals\nfor 15 NSE stocks",
     4.0, 27.3),
    ("MARKET ANALYSIS AGENT",
     "Fetches NIFTY 50 & SENSEX live\nCalculates sector performance\nIdentifies best & worst sectors\nMarket mood assessment",
     11.0, 27.3),
    ("SMART MONEY AGENT",
     "Calls NSE official API live\nFetches FII & DII net flows\nGenerates STRONG BUY / SELL signal\nbased on institutional activity",
     18.0, 27.3),
    ("NEWS & SENTIMENT AGENT",
     "Reads live RSS feeds (ET, Google)\nScores each headline with VADER\nCalculates overall market mood\nPositive / Negative / Neutral",
     4.0, 24.5),
    ("RISK MANAGEMENT AGENT",
     "Computes 1-year volatility per stock\nCalculates VaR at 95% confidence\nMeasures portfolio correlation\nRisk level: Low / Medium / High",
     11.0, 24.5),
    ("ADVANCED ANALYTICS AGENT",
     "Detects unusual volume (>1.5x avg)\nTracks sector rotation signals\nMeasures 1-week & 1-month momentum\nIdentifies breakout / breakdown",
     18.0, 24.5),
]

for title, desc, cx, cy in agents:
    box(ax, cx, cy, 6.2, 2.0, f"{title}\n\n{desc}", "agent", fontsize=10.5)
    # Arrow from router to each agent
    harrow(ax, 11, 29.47, cx, cy + 1.0)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 -- DATA SOURCES
# ─────────────────────────────────────────────────────────────────────────────
ax.text(11, 23.1, "LIVE DATA SOURCES USED BY AGENTS",
        ha="center", va="center", fontsize=13, fontweight="bold", color="#00695C")

sources = [
    ("Yahoo Finance\nfast_info API\n(Live prices)", 3.0),
    ("NSE India\nOfficial API\n(FII/DII flows)", 7.0),
    ("AMFI NAV File\n+ mfapi.in\n(MF returns)", 11.0),
    ("Google Finance\n+ ET RSS Feeds\n(Live news)", 15.0),
    ("1-Year Historical\nPrice Data\n(Risk metrics)", 19.0),
]
for text, cx in sources:
    box(ax, cx, 22.3, 3.6, 1.3, text, "data", fontsize=10)

# Arrows from agents to data sources
for _, _, acx, acy in agents:
    arrow(ax, acx, acy - 1.0, acx, 23.0)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 -- GROQ AI ANALYSIS PER AGENT
# ─────────────────────────────────────────────────────────────────────────────
arrow(ax, 11, 21.65, 11, 20.9)

box(ax, 11, 20.45, 14, 0.85,
    "GROQ LLAMA 3.3 70B  --  Each Agent Gets AI Analysis\n"
    "Live data is packed into a structured prompt → Groq generates expert analysis for each domain",
    "groq", fontsize=12, bold=True)

arrow(ax, 11, 20.02, 11, 19.25)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 -- AGENT OUTPUTS
# ─────────────────────────────────────────────────────────────────────────────
box(ax, 11, 18.8, 14, 0.85,
    "6 AGENT REPORTS COLLECTED\n"
    "Each report: Live data + AI analysis + Status (complete / error)",
    "router", fontsize=12, bold=True)

arrow(ax, 11, 18.37, 11, 17.6)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 -- MASTER REPORT AGENT
# ─────────────────────────────────────────────────────────────────────────────
box(ax, 11, 17.15, 14, 0.85,
    "MASTER REPORT AGENT  --  Groq Llama 3.3 70B\n"
    "Reads all 6 agent reports → Synthesises into one complete investment report",
    "master", fontsize=12, bold=True)

arrow(ax, 11, 16.72, 11, 15.95)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 8 -- MASTER REPORT SECTIONS
# ─────────────────────────────────────────────────────────────────────────────
ax.text(11, 15.7, "MASTER REPORT CONTAINS 6 SECTIONS",
        ha="center", va="center", fontsize=13, fontweight="bold", color="#1565C0")

sections = [
    ("1.  Executive Summary\nOverall market verdict\nin 2-3 sentences", 3.5, 14.5),
    ("2.  Top 3 Opportunities\nSpecific stocks/sectors\nwith exact reasoning", 8.5, 14.5),
    ("3.  Key Risks\n3 specific risks\nfrom live data", 13.5, 14.5),
    ("4.  Smart Money Signal\nFII/DII interpretation\nfor retail investors", 18.5, 14.5),
    ("5.  Action Plan\n3 concrete steps\nto take today", 6.5, 12.5),
    ("6.  Confidence Level\nHigh / Medium / Low\nwith reasoning", 15.5, 12.5),
]
for text, cx, cy in sections:
    box(ax, cx, cy, 4.5, 1.6, text, "master", fontsize=10.5)
    arrow(ax, 11, 15.47, cx, cy + 0.8)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 9 -- VISUALIZATIONS
# ─────────────────────────────────────────────────────────────────────────────
arrow(ax, 11, 11.7, 11, 10.95)

box(ax, 11, 10.5, 14, 0.85,
    "INTERACTIVE CHARTS & VISUALIZATIONS  (Plotly.js)\n"
    "Stock % change bar | RSI scatter | Sector heatmap | Sentiment pie | Volatility bar | FII gauge",
    "data", fontsize=12, bold=True)

arrow(ax, 11, 10.07, 11, 9.3)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 10 -- FINAL OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
box(ax, 11, 8.85, 14, 0.85,
    "FINAL OUTPUT DISPLAYED TO USER  (React Dashboard)\n"
    "Agent status cards | 7 interactive charts | Complete Master Investment Report",
    "output", fontsize=12, bold=True)

arrow(ax, 11, 8.42, 11, 7.65)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 11 -- USER DECISION
# ─────────────────────────────────────────────────────────────────────────────
diamond(ax, 11, 7.1, 8, 1.0,
        "User Reviews Report\n& Makes Investment Decision", fontsize=12)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 12 -- OUTCOMES
# ─────────────────────────────────────────────────────────────────────────────
arrow(ax, 7.0, 7.1, 4.5, 5.8)
arrow(ax, 11.0, 6.6, 11.0, 5.8)
arrow(ax, 15.0, 7.1, 17.5, 5.8)

box(ax, 4.5, 5.3, 5.5, 0.9,
    "BUY\nInvest in recommended\nstocks / sectors",
    "output", fontsize=11)
box(ax, 11.0, 5.3, 5.5, 0.9,
    "HOLD\nMonitor portfolio\nwith stop loss set",
    "input", fontsize=11)
box(ax, 17.5, 5.3, 5.5, 0.9,
    "ASK AGAIN\nRefine query &\nrun agents again",
    "router", fontsize=11)

# ─────────────────────────────────────────────────────────────────────────────
# TIMING NOTE
# ─────────────────────────────────────────────────────────────────────────────
box(ax, 11, 3.9, 14, 0.75,
    "Total Pipeline Time: 60–120 seconds  |  All data is 100% Real-Time  |  Zero Dummy Data",
    "data", fontsize=12, bold=True)

# ─────────────────────────────────────────────────────────────────────────────
# LEGEND
# ─────────────────────────────────────────────────────────────────────────────
legend_items = [
    (C["user"][0],   C["user"][1],   "User / Output"),
    (C["router"][0], C["router"][1], "System / Router"),
    (C["agent"][0],  C["agent"][1],  "AI Agent"),
    (C["data"][0],   C["data"][1],   "Data Source"),
    (C["groq"][0],   C["groq"][1],   "Groq AI (LLM)"),
    (C["master"][0], C["master"][1], "Master Report"),
]
lx, ly = 1.0, 2.8
ax.text(lx, ly + 0.3, "LEGEND:", fontsize=12, fontweight="bold", color="#1A1A1A")
for i, (border, fill, label) in enumerate(legend_items):
    bx = lx + (i % 3) * 4.5
    by = ly - 0.5 - (i // 3) * 0.7
    rect = FancyBboxPatch((bx, by - 0.2), 1.2, 0.4,
                          boxstyle="round,pad=0.05",
                          linewidth=2, edgecolor=border, facecolor=fill)
    ax.add_patch(rect)
    ax.text(bx + 1.35, by, label, fontsize=10.5, va="center", color="#1A1A1A")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
ax.text(11, 0.5,
        "सार्थक निवेश -- Agentic AI Investment Hub  |  Aman Jain, B.Tech 2023–27  |  "
        "Data: NSE | Yahoo Finance | AMFI | Google Finance RSS",
        ha="center", va="center", fontsize=11, color="#455A64",
        style="italic")

plt.tight_layout(pad=0.5)
plt.savefig("Agentic_AI.jpg", dpi=180, bbox_inches="tight",
            facecolor="#F8F9FA", format="jpg")
plt.close()
print("Saved: Agentic_AI.jpg")
