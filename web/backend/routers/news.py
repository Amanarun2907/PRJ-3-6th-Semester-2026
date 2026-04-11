"""News & Sentiment router — live RSS feeds + TextBlob + VADER."""
from fastapi import APIRouter
import feedparser, re
from datetime import datetime
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

router = APIRouter()
_vader = SentimentIntensityAnalyzer()

RSS_FEEDS = [
    ("https://news.google.com/rss/search?q=indian+stock+market+NSE+BSE&hl=en-IN&gl=IN&ceid=IN:en", "Google Finance"),
    ("https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms", "Economic Times"),
    ("https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms", "ET Stocks"),
    ("https://www.moneycontrol.com/rss/latestnews.xml", "MoneyControl"),
]

SECTOR_KEYWORDS = {
    "Banking":  ["bank","rbi","npa","credit","loan","hdfc","icici","sbi"],
    "IT":       ["tcs","infosys","wipro","it sector","software","tech"],
    "Pharma":   ["pharma","drug","fda","medicine","healthcare"],
    "Auto":     ["auto","car","ev","electric vehicle","maruti","tata motors"],
    "Energy":   ["oil","gas","reliance","ongc","energy","power"],
    "FMCG":     ["fmcg","consumer","hul","itc","nestle"],
    "Metals":   ["steel","metal","tata steel","hindalco","copper"],
    "IPO":      ["ipo","listing","grey market","gmp","subscription"],
}

def _sentiment(text):
    tb  = TextBlob(text).sentiment.polarity
    vd  = _vader.polarity_scores(text)["compound"]
    avg = (tb + vd) / 2
    label = "Positive" if avg > 0.1 else "Negative" if avg < -0.1 else "Neutral"
    return {"score": round(avg, 3), "label": label}

def _category(title):
    tl = title.lower()
    for cat, kws in SECTOR_KEYWORDS.items():
        if any(kw in tl for kw in kws):
            return cat
    return "General"

@router.get("/live")
def get_news(limit: int = 40):
    articles = []
    for url, source in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:12]:
                title = entry.get("title","")
                if not title: continue
                sent = _sentiment(title + " " + entry.get("summary",""))
                articles.append({
                    "title":     title,
                    "summary":   entry.get("summary","")[:200],
                    "link":      entry.get("link",""),
                    "source":    source,
                    "published": entry.get("published", datetime.now().isoformat()),
                    "category":  _category(title),
                    "sentiment": sent,
                })
        except Exception as e:
            print(f"RSS error {source}: {e}")
    articles = articles[:limit]
    return {"articles": articles, "total": len(articles),
            "timestamp": datetime.now().isoformat()}

@router.get("/sector_sentiment")
def get_sector_sentiment():
    news = get_news(limit=60)["articles"]
    sector_scores = {s: [] for s in SECTOR_KEYWORDS}
    for a in news:
        cat = a["category"]
        if cat in sector_scores:
            sector_scores[cat].append(a["sentiment"]["score"])
    result = {}
    for s, scores in sector_scores.items():
        if scores:
            avg = sum(scores)/len(scores)
            result[s] = {
                "score": round(avg,3),
                "label": "Positive" if avg>0.05 else "Negative" if avg<-0.05 else "Neutral",
                "count": len(scores),
            }
    return result
