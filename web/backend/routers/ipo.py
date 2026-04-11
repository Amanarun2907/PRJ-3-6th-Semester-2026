"""
IPO Intelligence Hub — Advanced Backend
Data sources (all live, zero dummy):
  - ipowatch.in main page  → IPO list with dates, size, price band
  - ipowatch.in detail page → financials, KPIs, lot size, peer comparison,
                               promoter holding, allotment dates
  - Groq Llama 3.3 70B     → AI recommendation per IPO
"""
from fastapi import APIRouter, Query
import requests, os, re
from bs4 import BeautifulSoup
from datetime import datetime

router = APIRouter()

_HDR = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# ── helpers ───────────────────────────────────────────────────────────────────

def _n(s):
    """Extract first number from a string."""
    try:
        nums = re.findall(r"-?\d+\.?\d*", str(s).replace(",", ""))
        return float(nums[0]) if nums else 0.0
    except Exception:
        return 0.0


def _parse_date_range(date_str: str):
    today = datetime.now()
    try:
        m = re.search(r"(\d+)-(\d+)\s+(\w+)(?:\s+(\d{4}))?", date_str)
        if m:
            s, e, month, yr = m.groups()
            yr = int(yr) if yr else today.year
            od = datetime.strptime(f"{s} {month} {yr}", "%d %B %Y")
            cd = datetime.strptime(f"{e} {month} {yr}", "%d %B %Y")
            return od, cd
        m2 = re.search(r"(\d+)\s+(\w+)(?:\s+(\d{4}))?", date_str)
        if m2:
            d, month, yr = m2.groups()
            yr = int(yr) if yr else today.year
            dt = datetime.strptime(f"{d} {month} {yr}", "%d %B %Y")
            return dt, dt
    except Exception:
        pass
    return None, None


def _status(date_str: str) -> str:
    today = datetime.now()
    od, cd = _parse_date_range(date_str)
    if od and cd:
        if today.date() < od.date():   return "Upcoming"
        if today.date() <= cd.date():  return "Open"
        return "Closed"
    return "Unknown"


def _score(ipo: dict) -> int:
    score = 40
    # Issue size
    size = _n(ipo.get("issue_size", "0"))
    if size >= 2000:   score += 20
    elif size >= 1000: score += 15
    elif size >= 500:  score += 10
    elif size >= 100:  score += 5
    # Category
    cat = str(ipo.get("category", "")).upper()
    if "MAINBOARD" in cat or "MAIN" in cat: score += 15
    elif "SME" in cat:                       score += 5
    # Subscription
    sub = _n(ipo.get("subscription", "0"))
    if sub >= 50:   score += 20
    elif sub >= 20: score += 15
    elif sub >= 10: score += 10
    elif sub >= 3:  score += 5
    elif 0 < sub < 1: score -= 10
    # GMP
    gmp = _n(ipo.get("gmp", "0"))
    if gmp > 50:   score += 10
    elif gmp > 20: score += 7
    elif gmp > 0:  score += 3
    elif gmp < 0:  score -= 10
    # Financials
    roe = _n(ipo.get("roe", "0"))
    if roe > 20:   score += 5
    elif roe > 10: score += 2
    pat_margin = _n(ipo.get("pat_margin", "0"))
    if pat_margin > 15: score += 5
    elif pat_margin > 8: score += 2
    # Status
    if ipo.get("status") == "Open":     score += 5
    elif ipo.get("status") == "Upcoming": score += 3
    return min(100, max(0, score))


# ── detail scraper ────────────────────────────────────────────────────────────

def _clean(s: str) -> str:
    """Remove placeholder brackets and clean whitespace."""
    s = re.sub(r"\[\.?\]", "", s).strip()
    s = re.sub(r"\s+", " ", s)
    return s if s and s not in ["-", "–", "₹-", "-%", "N/A"] else "N/A"


def _fetch_detail(url: str) -> dict:
    """
    Scrape individual IPO page. Handles all table structures on ipowatch.in.
    Extracts: dates, lot size, KPIs, financials, promoter holding,
              objects of issue, peer comparison.
    """
    detail = {}
    if not url:
        return detail
    try:
        r = requests.get(url, headers=_HDR, timeout=18)
        if r.status_code != 200:
            return detail
        soup = BeautifulSoup(r.content, "html.parser")
        tables = soup.find_all("table")

        for table in tables:
            rows = table.find_all("tr")
            if not rows:
                continue

            # ── 2-column key-value tables ──────────────────────────────────
            if all(len(row.find_all(["td","th"])) <= 2 for row in rows):
                for row in rows:
                    cols = row.find_all(["td","th"])
                    if len(cols) != 2:
                        continue
                    raw_key = cols[0].get_text(strip=True)
                    raw_val = cols[1].get_text(strip=True)
                    key = raw_key.lower().rstrip(":").strip()
                    val = _clean(raw_val)

                    # Date fields
                    if "open date" in key:
                        detail["open_date_full"]  = val
                    elif "close date" in key:
                        detail["close_date_full"] = val
                    elif "listing date" in key and "ipo" in key:
                        detail["listing_date"]    = val
                    elif "allotment" in key or "basis of allotment" in key:
                        detail["allotment_date"]  = val
                    elif "refund" in key:
                        detail["refund_date"]     = val
                    elif "demat" in key or "credit to demat" in key:
                        detail["demat_date"]      = val
                    elif "bidding cut-off" in key:
                        detail["cutoff_time"]     = val
                    # IPO basics
                    elif "price band" in key:
                        detail["price_band_full"] = val
                    elif "issue size" in key:
                        detail["issue_size_full"] = val
                    elif "face value" in key:
                        detail["face_value"]      = val
                    elif "issue type" in key:
                        detail["issue_type"]      = val
                    elif "fresh issue" in key:
                        detail["fresh_issue"]     = val
                    elif "offer for sale" in key:
                        detail["ofs"]             = val
                    # KPIs — exact match with colon stripped
                    elif key == "roe":
                        detail["roe"]             = val
                    elif key == "roce":
                        detail["roce"]            = val
                    elif "ebitda margin" in key:
                        detail["ebitda_margin"]   = val
                    elif "pat margin" in key:
                        detail["pat_margin"]      = val
                    elif "debt to equity" in key or "debt/equity" in key:
                        detail["debt_equity"]     = val
                    elif "earning per share" in key or "eps" in key:
                        detail["eps"]             = val
                    elif "price/earning" in key or "p/e ratio" in key:
                        detail["pe_ratio"]        = val
                    elif "return on net worth" in key or "ronw" in key:
                        detail["ronw"]            = val
                    elif "net asset value" in key or "nav" in key:
                        detail["nav"]             = val
                    # Anchor
                    elif "anchor size" in key:
                        detail["anchor_size"]     = val
                    elif "anchor bidding" in key:
                        detail["anchor_date"]     = val

            # ── Lot size table (Application | Lot Size | Shares | Amount) ──
            header_text = " ".join(c.get_text(strip=True).lower()
                                   for c in rows[0].find_all(["td","th"]))
            if "lot size" in header_text and "application" in header_text:
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if not cols:
                        continue
                    label = cols[0].get_text(strip=True).lower()
                    if "retail minimum" in label and len(cols) >= 4:
                        detail["lot_size"]       = _clean(cols[1].get_text(strip=True))
                        detail["lot_shares"]     = _clean(cols[2].get_text(strip=True))
                        detail["min_investment"] = _clean(cols[3].get_text(strip=True))

            # ── Promoter holding table ──────────────────────────────────────
            if "promoter" in header_text and "particular" in header_text:
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 3:
                        label = cols[0].get_text(strip=True).lower()
                        pct   = _clean(cols[2].get_text(strip=True))
                        if "pre" in label:
                            detail["promoter_pre"]  = pct
                        elif "post" in label:
                            detail["promoter_post"] = pct

            # ── Financials table (Period | Revenue | Expense | PAT | Assets) ─
            if "period ended" in header_text and "revenue" in header_text:
                fin_rows = []
                for row in rows:
                    cols = row.find_all(["td","th"])
                    if len(cols) >= 4:
                        fin_rows.append([_clean(c.get_text(strip=True)) for c in cols[:5]])
                if len(fin_rows) > 1:
                    detail["financials"] = fin_rows

            # ── Objects of issue (Purpose | Crores) ────────────────────────
            if "purpose" in header_text and len(rows) > 1:
                objects = []
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        purpose = _clean(cols[0].get_text(strip=True))
                        amount  = _clean(cols[1].get_text(strip=True))
                        if purpose and purpose != "N/A":
                            objects.append({"purpose": purpose, "amount": amount})
                if objects:
                    detail["objects_of_issue"] = objects

            # ── Peer comparison (Company | EPS | PE | RoNW | NAV | Income) ─
            if "pe ratio" in header_text or ("eps" in header_text and "company" in header_text):
                peers = []
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 3:
                        company = _clean(cols[0].get_text(strip=True))
                        if company and company != "N/A":
                            peers.append({
                                "company": company,
                                "eps":     _clean(cols[1].get_text(strip=True)) if len(cols) > 1 else "N/A",
                                "pe":      _clean(cols[2].get_text(strip=True)) if len(cols) > 2 else "N/A",
                                "ronw":    _clean(cols[3].get_text(strip=True)) if len(cols) > 3 else "N/A",
                                "nav":     _clean(cols[4].get_text(strip=True)) if len(cols) > 4 else "N/A",
                                "income":  _clean(cols[5].get_text(strip=True)) if len(cols) > 5 else "N/A",
                            })
                if peers:
                    detail["peers"] = peers

            # ── Investor category table ─────────────────────────────────────
            if "investor category" in header_text or "qib" in header_text:
                categories = []
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        cat  = _clean(cols[0].get_text(strip=True))
                        pct  = _clean(cols[2].get_text(strip=True)) if len(cols) > 2 else "N/A"
                        if cat and cat != "N/A":
                            categories.append({"category": cat, "percentage": pct})
                if categories:
                    detail["investor_categories"] = categories

    except Exception as e:
        print(f"Detail scrape error {url}: {e}")
    return detail


# ── main list scraper ─────────────────────────────────────────────────────────

def _fetch_ipowatch_list() -> list:
    ipos = []
    try:
        r = requests.get("https://ipowatch.in/", headers=_HDR, timeout=20)
        if r.status_code != 200:
            return ipos
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        if not table:
            return ipos
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            try:
                name       = cols[0].get_text(strip=True)
                link_tag   = cols[0].find("a")
                detail_url = link_tag["href"] if link_tag else ""
                date_str   = cols[1].get_text(strip=True)
                category   = cols[2].get_text(strip=True)
                issue_size = cols[3].get_text(strip=True)
                price_band = cols[4].get_text(strip=True) if len(cols) > 4 else "TBA"
                price_band = re.sub(r"\[\.?\]", "TBA", price_band)

                if not name or len(name) < 3:
                    continue

                od, cd = _parse_date_range(date_str)
                status = _status(date_str)

                ipo = {
                    "name":        name,
                    "detail_url":  detail_url,
                    "date":        date_str,
                    "open_date":   od.strftime("%d %b %Y") if od else date_str,
                    "close_date":  cd.strftime("%d %b %Y") if cd else date_str,
                    "category":    category,
                    "issue_size":  issue_size,
                    "price_band":  price_band,
                    "status":      status,
                    "source":      "ipowatch.in",
                    "subscription":"N/A",
                    "gmp":         "N/A",
                    "listing_date":"N/A",
                    "lot_size":    "N/A",
                    "min_investment": "N/A",
                    "roe":         "N/A",
                    "pat_margin":  "N/A",
                    "debt_equity": "N/A",
                    "promoter_pre":"N/A",
                    "promoter_post":"N/A",
                    "financials":  [],
                    "peers":       [],
                    "objects_of_issue": [],
                }
                ipo["score"]          = _score(ipo)
                ipo["recommendation"] = (
                    "APPLY"   if ipo["score"] >= 65 else
                    "AVOID"   if ipo["score"] < 45 else
                    "NEUTRAL"
                )
                ipos.append(ipo)
            except Exception:
                continue
    except Exception as e:
        print(f"ipowatch list error: {e}")
    return ipos


# ── AI recommendation ─────────────────────────────────────────────────────────

def _ai_recommend(ipo: dict) -> str:
    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        return None

    # Build financials text
    fin_text = ""
    if ipo.get("financials") and len(ipo["financials"]) > 1:
        fin_text = "\n".join([" | ".join(r) for r in ipo["financials"][:5]])

    # Build peers text
    peers_text = ""
    if ipo.get("peers"):
        peers_text = "\n".join([
            f"  {p['company'][:35]} — EPS: {p['eps']}, PE: {p['pe']}, RoNW: {p['ronw']}, NAV: {p.get('nav','N/A')}"
            for p in ipo["peers"][:4]
        ])

    # Build objects of issue text
    objects_text = ""
    if ipo.get("objects_of_issue"):
        objects_text = "\n".join([
            f"  {o['purpose'][:50]}: {o['amount']}"
            for o in ipo["objects_of_issue"][:5]
        ])

    # Build investor categories
    cat_text = ""
    if ipo.get("investor_categories"):
        cat_text = " | ".join([
            f"{c['category']}: {c['percentage']}"
            for c in ipo["investor_categories"][:5]
        ])

    prompt = f"""
You are India's top IPO analyst. Give a comprehensive, data-driven analysis for this IPO.

=== IPO DETAILS ===
Company: {ipo['name']}
Category: {ipo['category']} | Status: {ipo['status']}
Price Band: {ipo.get('price_band_full') or ipo.get('price_band','N/A')}
Issue Size: {ipo.get('issue_size_full') or ipo.get('issue_size','N/A')}
Issue Type: {ipo.get('issue_type','N/A')} | Face Value: {ipo.get('face_value','N/A')}
Fresh Issue: {ipo.get('fresh_issue','N/A')} | OFS: {ipo.get('ofs','N/A')}
Lot Size: {ipo.get('lot_size','N/A')} lots ({ipo.get('lot_shares','N/A')} shares)
Min Investment: {ipo.get('min_investment','N/A')}
Open: {ipo.get('open_date_full') or ipo.get('open_date','N/A')} | Close: {ipo.get('close_date_full') or ipo.get('close_date','N/A')}
Listing Date: {ipo.get('listing_date','N/A')} | Allotment: {ipo.get('allotment_date','N/A')}
Subscription: {ipo.get('subscription','N/A')} | GMP: {ipo.get('gmp','N/A')}
IPO Score: {ipo['score']}/100

=== FINANCIAL KPIs ===
ROE: {ipo.get('roe','N/A')} | ROCE: {ipo.get('roce','N/A')}
EBITDA Margin: {ipo.get('ebitda_margin','N/A')} | PAT Margin: {ipo.get('pat_margin','N/A')}
Debt/Equity: {ipo.get('debt_equity','N/A')} | EPS: {ipo.get('eps','N/A')}
P/E Ratio: {ipo.get('pe_ratio','N/A')} | RoNW: {ipo.get('ronw','N/A')} | NAV: {ipo.get('nav','N/A')}
Promoter Pre-Issue: {ipo.get('promoter_pre','N/A')} | Post-Issue: {ipo.get('promoter_post','N/A')}

=== INVESTOR ALLOCATION ===
{cat_text if cat_text else 'Not available'}

=== FINANCIAL HISTORY (Revenue | Expense | PAT | Assets in ₹ Cr) ===
{fin_text if fin_text else 'Not available'}

=== PEER COMPARISON ===
{peers_text if peers_text else 'Not available'}

=== USE OF IPO PROCEEDS ===
{objects_text if objects_text else 'Not available'}

Write a comprehensive IPO analysis with these EXACT sections:

**1. VERDICT** — APPLY / AVOID / NEUTRAL with a one-line reason

**2. INVESTMENT THESIS** — 3 bullet points explaining WHY this IPO is worth applying (or not). Be specific with numbers from the data above.

**3. KEY RISKS** — 3 specific risks. Be honest about red flags.

**4. FINANCIAL HEALTH ASSESSMENT** — Rate the company: Strong / Moderate / Weak. Comment on ROE, margins, debt, and revenue growth trend.

**5. VALUATION CHECK** — Is the IPO priced fairly vs peers? Compare P/E and RoNW with peer companies.

**6. PROFIT MAXIMISATION STRATEGY** — This is the most important section. Give a specific exit plan:
   - **Listing Day Strategy**: Should the investor sell on listing day? At what % gain should they exit?
   - **Short-term (30 days)**: Hold or sell? What price target?
   - **Medium-term (60-90 days)**: What to do if listing gain is moderate?
   - **Recommended Split**: e.g. "Sell 50% on listing day, hold 50% for 90 days"
   - **Stop Loss**: At what % below issue price should the investor exit to cut losses?

**7. WHO SHOULD APPLY** — Listing gain seekers / Long-term investors / Both / Neither

Keep total under 450 words. Use ₹ for amounts. Be direct, specific, and actionable.
""".strip()

    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {key}"},
            json={"model": "llama-3.3-70b-versatile", "temperature": 0.5,
                  "max_tokens": 700,
                  "messages": [
                      {"role": "system",
                       "content": ("You are India's top IPO analyst. Be direct, data-driven, "
                                   "and give specific profit-maximising advice. "
                                   "Always give a clear exit strategy with numbers.")},
                      {"role": "user", "content": prompt},
                  ]},
            timeout=40,
        )
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq IPO error: {e}")
    return None


# ── routes ────────────────────────────────────────────────────────────────────

@router.get("/live")
def get_ipos():
    ipos = _fetch_ipowatch_list()
    order = {"Open": 0, "Upcoming": 1, "Closed": 2, "Unknown": 3}
    ipos.sort(key=lambda x: order.get(x["status"], 3))
    return {
        "ipos":           ipos,
        "total":          len(ipos),
        "open_count":     sum(1 for i in ipos if i["status"] == "Open"),
        "upcoming_count": sum(1 for i in ipos if i["status"] == "Upcoming"),
        "closed_count":   sum(1 for i in ipos if i["status"] == "Closed"),
        "timestamp":      datetime.now().isoformat(),
        "source":         "ipowatch.in (live)",
    }


@router.get("/detail")
def get_detail(url: str = Query(...)):
    """Fetch rich detail for a single IPO from its detail page."""
    detail = _fetch_detail(url)
    return detail


@router.get("/ai_analysis")
def get_ai_analysis(url: str = Query(...), name: str = Query("")):
    """Fetch detail + AI recommendation for one IPO."""
    # Get base IPO data
    ipos = _fetch_ipowatch_list()
    ipo = next((i for i in ipos if i.get("detail_url") == url), None)
    if not ipo:
        ipo = {"name": name, "category": "Unknown", "status": "Unknown",
               "price_band": "N/A", "issue_size": "N/A", "score": 50,
               "recommendation": "NEUTRAL"}
    # Enrich with detail page
    detail = _fetch_detail(url)
    ipo.update(detail)
    ipo["score"] = _score(ipo)
    ipo["recommendation"] = (
        "APPLY"   if ipo["score"] >= 65 else
        "AVOID"   if ipo["score"] < 45 else
        "NEUTRAL"
    )
    # AI recommendation
    ipo["ai_analysis"] = _ai_recommend(ipo)
    return ipo
