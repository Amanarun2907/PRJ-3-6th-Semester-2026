import requests
import json

print("Testing NSE APIs...")

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

# Get cookies
session.get('https://www.nseindia.com', timeout=5)

# Test Bulk Deals
try:
    response = session.get('https://www.nseindia.com/api/snapshot-capital-market-largedeal', timeout=10)
    print(f"Bulk Deals API: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Bulk Records: {len(data.get('data', []))}")
        if data.get('data'):
            print("Sample:", data['data'][0])
except Exception as e:
    print(f"Bulk API Error: {e}")

# Test Block Deals
try:
    response = session.get('https://www.nseindia.com/api/block-deal', timeout=10)
    print(f"Block Deals API: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Block Records: {len(data.get('data', []))}")
except Exception as e:
    print(f"Block API Error: {e}")