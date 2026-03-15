"""
Test News Fetching for Stocks
"""
import yfinance as yf
from textblob import TextBlob
from datetime import datetime

def test_news_fetch(stock_symbol, company_name):
    print(f"\n{'='*60}")
    print(f"📰 Testing News Fetch for: {company_name} ({stock_symbol})")
    print(f"{'='*60}\n")
    
    # Method 1: Yahoo Finance
    print("1️⃣ Testing Yahoo Finance News API...")
    try:
        ticker = yf.Ticker(stock_symbol)
        news = ticker.news
        
        if news and len(news) > 0:
            print(f"   ✅ SUCCESS! Found {len(news)} articles")
            for i, article in enumerate(news[:3], 1):
                title = article.get('title', 'No title')
                print(f"   {i}. {title[:60]}...")
        else:
            print("   ⚠️ No news found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Method 2: Google News RSS
    print("\n2️⃣ Testing Google News RSS...")
    try:
        import feedparser
        search_query = company_name.replace(' ', '+')
        url = f"https://news.google.com/rss/search?q={search_query}+stock&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(url)
        
        if feed.entries:
            print(f"   ✅ SUCCESS! Found {len(feed.entries)} articles")
            for i, entry in enumerate(feed.entries[:3], 1):
                title = entry.get('title', 'No title')
                print(f"   {i}. {title[:60]}...")
        else:
            print("   ⚠️ No articles found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Method 3: Economic Times
    print("\n3️⃣ Testing Economic Times RSS...")
    try:
        import feedparser
        url = "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms"
        feed = feedparser.parse(url)
        
        if feed.entries:
            print(f"   ✅ SUCCESS! Found {len(feed.entries)} total articles")
            
            # Filter for company
            relevant = []
            for entry in feed.entries:
                title = entry.get('title', '')
                if company_name.lower() in title.lower():
                    relevant.append(title)
            
            if relevant:
                print(f"   ✅ Found {len(relevant)} relevant articles:")
                for i, title in enumerate(relevant[:3], 1):
                    print(f"   {i}. {title[:60]}...")
            else:
                print(f"   ⚠️ No articles mentioning '{company_name}'")
        else:
            print("   ⚠️ No articles found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n{'='*60}\n")

# Test with multiple stocks
test_stocks = [
    ('RELIANCE.NS', 'Reliance Industries'),
    ('TCS.NS', 'TCS'),
    ('HDFCBANK.NS', 'HDFC Bank')
]

for symbol, name in test_stocks:
    test_news_fetch(symbol, name)

print("✅ All tests complete!")
