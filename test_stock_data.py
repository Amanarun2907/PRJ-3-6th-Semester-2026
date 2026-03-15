"""
Test script to check if stock data is loading properly
"""
import yfinance as yf
import pandas as pd

print("🔍 Testing Stock Data Fetch...")
print("=" * 60)

# Test with a popular stock
test_stock = "RELIANCE.NS"
print(f"\n📊 Testing: {test_stock}")

try:
    # Method 1: Using yfinance Ticker
    print("\n1️⃣ Testing yf.Ticker().history()...")
    ticker = yf.Ticker(test_stock)
    data = ticker.history(period='1mo')
    
    if not data.empty:
        print(f"✅ SUCCESS! Got {len(data)} days of data")
        print(f"   Latest Close: ₹{data['Close'].iloc[-1]:.2f}")
        print(f"   Date Range: {data.index[0]} to {data.index[-1]}")
    else:
        print("❌ FAILED! Data is empty")
    
    # Method 2: Get stock info
    print("\n2️⃣ Testing ticker.info...")
    info = ticker.info
    
    if info:
        print(f"✅ SUCCESS! Got stock info")
        print(f"   Company: {info.get('longName', 'N/A')}")
        print(f"   Sector: {info.get('sector', 'N/A')}")
        print(f"   Market Cap: ₹{info.get('marketCap', 0)/1e9:.2f}B")
    else:
        print("❌ FAILED! Info is empty")
    
    # Method 3: Test multiple stocks
    print("\n3️⃣ Testing multiple stocks...")
    test_stocks = ['TCS.NS', 'HDFCBANK.NS', 'INFY.NS']
    
    for stock in test_stocks:
        try:
            data = yf.Ticker(stock).history(period='5d')
            if not data.empty:
                print(f"   ✅ {stock}: ₹{data['Close'].iloc[-1]:.2f}")
            else:
                print(f"   ❌ {stock}: No data")
        except Exception as e:
            print(f"   ❌ {stock}: Error - {e}")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nPossible issues:")
    print("1. Internet connection problem")
    print("2. Yahoo Finance API is down")
    print("3. yfinance library needs update: pip install --upgrade yfinance")

print("\n" + "=" * 60)
print("✅ Test Complete!")
