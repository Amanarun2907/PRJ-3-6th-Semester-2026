"""
Test IPO Data Fetching
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def test_ipo_fetch():
    """Test fetching real IPO data"""
    print("🔍 Testing IPO Data Fetch...")
    print("=" * 60)
    
    # Test 1: Chittorgarh
    print("\n📊 Test 1: Chittorgarh IPO Data")
    try:
        url = "https://www.chittorgarh.com/report/ipo-in-india-list-main-board-sme/82/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')
            print(f"Found {len(tables)} tables")
            
            if tables:
                print("\n📋 Sample IPO Data:")
                for table in tables[:2]:  # Check first 2 tables
                    rows = table.find_all('tr')
                    print(f"  Table has {len(rows)} rows")
                    
                    for row in rows[1:6]:  # Show first 5 data rows
                        cols = row.find_all('td')
                        if len(cols) >= 4:
                            company = cols[0].get_text(strip=True)
                            dates = cols[1].get_text(strip=True) if len(cols) > 1 else 'N/A'
                            print(f"  - {company}: {dates}")
        else:
            print("❌ Failed to fetch data")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Show fallback data
    print("\n📊 Test 2: Fallback IPO Data (Always Available)")
    fallback_ipos = [
        'Gaudium IVF & Women Health',
        'Shree Ram Twistex Limited',
        'Clean Max Enviro Energy Solutions',
        'PNGS Reva Enviro Energy',
        'Omitech Engineering Limited'
    ]
    
    for ipo in fallback_ipos:
        print(f"  ✓ {ipo}")
    
    print("\n" + "=" * 60)
    print("✅ Test Complete!")
    print("\nNote: The app will show:")
    print("  1. Live IPOs if available from web sources")
    print("  2. Recent IPOs (like those from Groww) as fallback")
    print("  3. These IPOs update when you refresh the page")

if __name__ == "__main__":
    test_ipo_fetch()
