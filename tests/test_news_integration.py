"""
Test News & Sentiment Integration
"""

from realtime_news_fetcher import RealtimeNewsFetcher

print("=" * 60)
print("Testing News & Sentiment Integration")
print("=" * 60)

fetcher = RealtimeNewsFetcher()

# Test 1: Fetch news
print("\n1️⃣ Fetching Real-time News...")
news = fetcher.get_comprehensive_news()

if news:
    print(f"✅ Fetched {len(news)} news articles")
    
    # Show sample
    print("\n📰 Sample News:")
    sample = news[0]
    print(f"  Title: {sample['title']}")
    print(f"  Source: {sample['source']}")
    print(f"  Category: {sample['category']}")
    print(f"  Sentiment: {sample['sentiment_analysis']['sentiment']} {sample['sentiment_analysis']['emoji']}")
    print(f"  Score: {sample['sentiment_analysis']['score']:.3f}")
    print(f"  Impact: {sample['impact_score']}/100")
    print(f"  Time: {sample['time_ago']}")
    
    # Test 2: Sector sentiment
    print("\n2️⃣ Sector Sentiment:")
    sector_sent = fetcher.get_sector_sentiment(news)
    for sector, data in list(sector_sent.items())[:5]:
        emoji = '🟢' if data['score'] > 0.1 else '🔴' if data['score'] < -0.1 else '🟡'
        print(f"  {sector}: {data['score']:.3f} {emoji} ({data['count']} news)")
    
    # Test 3: Trending topics
    print("\n3️⃣ Trending Topics:")
    trending = fetcher.get_trending_topics(news)
    for topic in trending[:5]:
        print(f"  {topic['topic']}: {topic['count']} mentions")
    
    # Test 4: Stock mentions
    print("\n4️⃣ Stock Mentions:")
    stock_mentions = {}
    for n in news:
        for stock in n.get('stock_mentions', []):
            stock_mentions[stock] = stock_mentions.get(stock, 0) + 1
    
    for stock, count in sorted(stock_mentions.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {stock}: {count} mentions")
    
    print("\n✅ All tests passed!")
else:
    print("❌ No news fetched")

print("=" * 60)
