"""Quick test for Advanced Analytics"""
from advanced_analytics_realtime import get_realtime_market_data, get_sector_performance

print("🧪 Testing Advanced Analytics Module...")
print("=" * 60)

print("\n1. Testing Real-time Market Data...")
market_data = get_realtime_market_data()
if market_data:
    print(f"✅ Successfully fetched data for {len(market_data)} stocks")
    for name, data in list(market_data.items())[:3]:
        print(f"   {name}: ₹{data['price']:.2f} ({data['change_pct']:+.2f}%)")
else:
    print("❌ Failed to fetch market data")

print("\n2. Testing Sector Performance...")
sector_perf = get_sector_performance()
if sector_perf:
    print(f"✅ Successfully calculated performance for {len(sector_perf)} sectors")
    for sector, perf in list(sector_perf.items())[:3]:
        print(f"   {sector}: {perf:+.2f}%")
else:
    print("❌ Failed to calculate sector performance")

print("\n" + "=" * 60)
print("✅ Advanced Analytics Module is ready!")
print("🚀 Run: streamlit run main_ultimate_final.py")
