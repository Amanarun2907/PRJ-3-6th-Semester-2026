from ipo_live_engine import IPOLiveEngine
e = IPOLiveEngine()

print("Testing ipowatch.in GMP scraper...")
gmp_data = e.fetch_gmp_ipowatch()
print(f"GMP entries: {len(gmp_data)}")
for ipo in gmp_data[:5]:
    print(f"  {ipo['company']}: GMP={ipo['gmp']} ({ipo['gmp_percent']}%) | Price={ipo['price_band']} | Status={ipo['status']}")

print("\nOpen IPOs:")
open_ipos = [i for i in gmp_data if i['status'] == 'Open']
for ipo in open_ipos:
    print(f"  OPEN: {ipo['company']} | {ipo['price_band']} | {ipo['open_date']}-{ipo['close_date']}")

print("\nUpcoming IPOs:")
upcoming = [i for i in gmp_data if i['status'] == 'Upcoming']
for ipo in upcoming:
    print(f"  UPCOMING: {ipo['company']} | {ipo['price_band']}")

print("\nTesting listed IPOs...")
listed = e.fetch_listed_ipos_ipowatch()
print(f"Listed: {len(listed)}")
for l in listed[:3]:
    print(f"  {l['company']} | Issue: {l['issue_price']} | Listing: {l['listing_price']} | Gain: {l['listing_gain']}%")

print("\nAll tests done!")
