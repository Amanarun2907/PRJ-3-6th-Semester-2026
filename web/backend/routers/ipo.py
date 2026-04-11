"""
IPO Intelligence Router
Real-time data from ipowatch.in — the most reliable free IPO source.
Scrapes: IPO name, dates, type, size, price band, status, subscription, GMP.
"""
from fastapi import APIRouter
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

router = APIRouter()

_HDR = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def _parse_date_range(date_str: str):
    """Parse '17-21 April' or '23-27 April 2026' into open/close datetime."""
    today = datetime.now()
    try:
        # Pattern: "17-21 April" or "17-21 April 2026"
        m = re.search(r"(\d+)-(\d+)\s+(\w+)(?:\s+(\d{4}))?", date_str)
        if m:
            start_d, end_d, month, year = m.groups()
            year = int(year) if year else today.year
            open_dt  = datetime.strptime(f"{start_d} {month} {year}", "%d %B %Y")
            close_dt = datetime.strptime(f"{end_d} {month} {year}", "%d %B %Y")
            return open_dt, close_dt
        # Pattern: single date "21 April"
        m2 = re.search(r"(\d+)\s+(\w+)(?:\s+(\d{4}))?", date_str)
        if m2:
            d, month, year = m2.groups()
            year = int(year) if year else today.year
            dt = datetime.strptime(f"{d} {month} {year}", "%d %B %Y")
            return dt, dt
    except Exception:
        pass
    return None, None


def _determine_status(date_str: str) -> str:
    today = datetime.now()
    open_dt, close_dt = _parse_date_range(date_str)
    if open_dt and close_dt:
        if today.date() < open_dt.date():
            return "Upcoming"
        elif today.date() <= close_dt.date():
            return "Open"
        else:
            return "Closed"
    return "Unknown"


def _score_ipo(ipo: dict) -> int:
    """Multi-factor IPO score 0-100."""
    score = 40

    # Issue size
    size_str = str(ipo.get("issue_size", "0")).replace(",", "")
    nums = re.findall(r"\d+\.?\d*", size_str)
    size = float(nums[0]) if nums else 0
    if size >= 2000:   score += 20
    elif size >= 1000: score += 15
    elif size >= 500:  score += 10
    elif size >= 100:  score += 5

    # Category
    cat = str(ipo.get("category", "")).upper()
    if "MAINBOARD" in cat or "MAIN" in cat:
        score += 15
    elif "SME" in cat:
        score += 5

    # Subscription
    sub_str = str(ipo.get("subscription", "0")).replace("x", "").replace(",", "")
    sub_nums = re.findall(r"\d+\.?\d*", sub_str)
    sub = float(sub_nums[0]) if sub_nums else 0
    if sub >= 50:   score += 20
    elif sub >= 20: score += 15
    elif sub >= 10: score += 10
    elif sub >= 3:  score += 5
    elif 0 < sub < 1: score -= 10

    # GMP
    gmp_str = str(ipo.get("gmp", "0")).replace("₹", "").replace(",", "").strip()
    gmp_nums = re.findall(r"-?\d+\.?\d*", gmp_str)
    gmp = float(gmp_nums[0]) if gmp_nums else 0
    if gmp > 50:   score += 10
    elif gmp > 20: score += 7
    elif gmp > 0:  score += 3
    elif gmp < 0:  score -= 10

    # Status bonus
    if ipo.get("status") == "Open":     score += 5
    elif ipo.get("status") == "Upcoming": score += 3

    return min(100, max(0, score))


def _fetch_ipowatch_main():
    """Fetch main IPO list from ipowatch.in."""
    ipos = []
    try:
        r = requests.get("https://ipowatch.in/", headers=_HDR, timeout=20)
        if r.status_code != 200:
            return ipos
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        if not table:
            return ipos
        rows = table.find_all("tr")[1:]  # skip header
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            try:
                name       = cols[0].get_text(strip=True)
                date_str   = cols[1].get_text(strip=True)
                category   = cols[2].get_text(strip=True)
                issue_size = cols[3].get_text(strip=True)
                price_band = cols[4].get_text(strip=True) if len(cols) > 4 else "N/A"

                if not name or len(name) < 3:
                    continue

                # Clean price band — remove placeholder brackets
                price_band = re.sub(r"\[\.?\]", "TBA", price_band)

                status = _determine_status(date_str)

                # Parse open/close dates for display
                open_dt, close_dt = _parse_date_range(date_str)
                open_date  = open_dt.strftime("%d %b %Y")  if open_dt  else date_str
                close_date = close_dt.strftime("%d %b %Y") if close_dt else date_str

                ipo = {
                    "name":       name,
                    "date":       date_str,
                    "open_date":  open_date,
                    "close_date": close_date,
                    "category":   category,
                    "issue_size": issue_size,
                    "price_band": price_band,
                    "status":     status,
                    "source":     "ipowatch.in",
                    "subscription": "N/A",
                    "gmp":        "N/A",
                    "listing_date": "N/A",
                }
                ipo["score"]          = _score_ipo(ipo)
                ipo["recommendation"] = (
                    "APPLY"   if ipo["score"] >= 65 else
                    "AVOID"   if ipo["score"] < 45 else
                    "NEUTRAL"
                )
                ipos.append(ipo)
            except Exception:
                continue
    except Exception as e:
        print(f"ipowatch fetch error: {e}")
    return ipos


def _fetch_subscription_data():
    """Fetch live subscription data from ipowatch."""
    subs = {}
    try:
        r = requests.get(
            "https://ipowatch.in/ipo-subscription-status/",
            headers=_HDR, timeout=15
        )
        if r.status_code != 200:
            return subs
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        if not table:
            return subs
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 3:
                name = cols[0].get_text(strip=True)
                sub  = cols[-1].get_text(strip=True)  # last col usually total
                if name:
                    subs[name.lower()[:20]] = sub
    except Exception:
        pass
    return subs


@router.get("/live")
def get_ipos():
    ipos = _fetch_ipowatch_main()
    subs = _fetch_subscription_data()

    # Enrich with subscription data
    for ipo in ipos:
        key = ipo["name"].lower()[:20]
        if key in subs:
            ipo["subscription"] = subs[key]
            ipo["score"]          = _score_ipo(ipo)
            ipo["recommendation"] = (
                "APPLY"   if ipo["score"] >= 65 else
                "AVOID"   if ipo["score"] < 45 else
                "NEUTRAL"
            )

    # Sort: Open first, then Upcoming, then Closed
    order = {"Open": 0, "Upcoming": 1, "Closed": 2, "Unknown": 3}
    ipos.sort(key=lambda x: order.get(x["status"], 3))

    open_count     = sum(1 for i in ipos if i["status"] == "Open")
    upcoming_count = sum(1 for i in ipos if i["status"] == "Upcoming")
    closed_count   = sum(1 for i in ipos if i["status"] == "Closed")

    return {
        "ipos":           ipos,
        "total":          len(ipos),
        "open_count":     open_count,
        "upcoming_count": upcoming_count,
        "closed_count":   closed_count,
        "timestamp":      datetime.now().isoformat(),
        "source":         "ipowatch.in (live)",
    }
