"""
Test Live APIs During Market Hours
"""
from smart_money_tracker import SmartMoneyTracker
import requests

print("🧪 TESTING LIVE APIs DURING MARKET HOURS")
print("=" * 80)

tracker = SmartMoneyTracker()

# Test 1: FII/DII (Should work)
print("\n1️⃣ Testing FII/DII Data...")
fii_dii = tracker.fetch_fii_dii_data()
if not fii_dii.empty:
    print(f"✅ FII/DII: {len(fii_dii)} records")
    print(f"   FII Net: ₹{fii_dii.iloc[0]['fii_net']:.2f} Cr")
    print(f"   DII Net: ₹{fii_dii.iloc[0]['dii_net']:.2f} Cr")
else:
    print("❌ FII/DII: No data")

# Test 2: Bulk Deals (Should have data during market hours)
print("\n2️⃣ Testing Bulk Deals...")
bulk = tracker.fetch_bulk_deals()
if not bulk.empty:
    print(f"✅ Bulk Deals: {len(bulk)} deals found")
    print(f"   Total Value: ₹{bulk['value'].sum()/10000000:.2f} Cr")
    for _, deal in bulk.head(3).iterrows():
        print(f"   - {deal['company']}: {deal['deal_type']} ₹{deal['value']/10000000:.2f} Cr")
else:
    print("❌ Bulk Deals: No data")

# Test 3: Block Deals
print("\n3️⃣ Testing Block Deals...")
block = tracker.fetch_block_deals()
if not block.empty:
    print(f"✅ Block Deals: {len(block)} deals found")
    for _, deal in block.head(3).iterrows():
        print(f"   - {deal['company']}: ₹{deal['value']/10000000:.2f} Cr")
else:
    print("❌ Block Deals: No data")

# Test 4: Direct NSE API Test
print("\n4️⃣ Testing Direct NSE APIs...")
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

# Get NSE cookies
print("   Getting NSE cookies...")
response = session.get('https://www.nseindia.com', timeout=10)
print(f"   Cookie response: {response.status_code}")

# Test Bulk Deals API
print("   Testing Bulk Deals API...")
bulk_url = "https://www.nseindia.com/api/snapshot-capital-market-largedeal"
response = session.get(bulk_url, timeout=15)
print(f"   Bulk API response: {response.status_code}")
if response.status_code == 200:
    try:
        data = response.json()
        print(f"   Bulk API data: {len(data.get('data', []))} records")
    except:
        print("   Bulk API: Invalid JSON")

# Test Block Deals API
print("   Testing Block Deals API...")
block_url = "https://www.nseindia.com/api/block-deal"
response = session.get(block_url, timeout=15)
print(f"   Block API response: {response.status_code}")
if response.status_code == 200:
    try:
        data = response.json()
        print(f"   Block API data: {len(data.get('data', []))} records")
    except:
        print("   Block API: Invalid JSON")

print("\n" + "=" * 80)
print("📊 DIAGNOSIS COMPLETE")
print("=" * 80)