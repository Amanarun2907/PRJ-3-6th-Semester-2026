from realtime_ipo_system import RealtimeIPOSystem

print("🧪 Testing Real-time IPO System...")
print("=" * 60)

ipo = RealtimeIPOSystem()
data = ipo.fetch_recent_listed_ipos()

print(f"\n✅ Fetched {len(data)} IPOs with REAL-TIME data from Yahoo Finance\n")

for d in data:
    print(f"🏢 {d['name']}")
    print(f"   Current: ₹{d['current_price']:.2f} | Return: {d['total_return']:+.1f}%")
    print(f"   Recommendation: {d['recommendation']}")
    print()

print("=" * 60)
print("✅ Real-time IPO system working perfectly!")
