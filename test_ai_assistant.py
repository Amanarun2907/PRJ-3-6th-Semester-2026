"""
Test Enhanced AI Investment Assistant
"""

from groq_ai_analyzer import GroqAIAnalyzer

print("=" * 70)
print("Testing Enhanced AI Investment Assistant")
print("=" * 70)

# Initialize Groq analyzer
api_key = "your_groq_api_key_here"
analyzer = GroqAIAnalyzer(api_key)

# Test 1: Stock Analysis
print("\n1️⃣ Testing Stock Analysis...")
prompt1 = """Provide a comprehensive analysis of HDFC Bank stock including:
1. Current market position
2. Technical indicators
3. Fundamental strengths
4. Investment recommendation
5. Target price

Keep it concise."""

response1 = analyzer._call_groq(prompt1)
if response1:
    print("✅ Stock Analysis:")
    print(response1[:300] + "...")
else:
    print("❌ Failed")

# Test 2: SIP Recommendations
print("\n2️⃣ Testing SIP Recommendations...")
prompt2 = """Recommend top 3 mutual funds for SIP investment with:
- Monthly investment: ₹10,000
- Risk appetite: Moderate

For each fund provide name, category, and expected returns."""

response2 = analyzer._call_groq(prompt2)
if response2:
    print("✅ SIP Recommendations:")
    print(response2[:300] + "...")
else:
    print("❌ Failed")

# Test 3: Portfolio Review
print("\n3️⃣ Testing Portfolio Review...")
prompt3 = """Review this portfolio:
40% HDFC Bank, 30% TCS, 20% Axis Bluechip Fund, 10% Gold ETF

Provide diversification analysis and suggestions."""

response3 = analyzer._call_groq(prompt3)
if response3:
    print("✅ Portfolio Review:")
    print(response3[:300] + "...")
else:
    print("❌ Failed")

# Test 4: Market Outlook
print("\n4️⃣ Testing Market Outlook...")
prompt4 = """Provide Indian stock market outlook for this month:
1. Expected direction
2. Key factors
3. Sectors to watch
4. Investment strategy"""

response4 = analyzer._call_groq(prompt4)
if response4:
    print("✅ Market Outlook:")
    print(response4[:300] + "...")
else:
    print("❌ Failed")

print("\n" + "=" * 70)
print("✅ AI Investment Assistant Test Complete!")
print("=" * 70)
