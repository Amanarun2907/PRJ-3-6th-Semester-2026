"""
Quick Test - Agentic AI with Real API
"""

from agentic_ai_simple import SimpleAgenticStockAnalysis
import time

print("🧪 QUICK TEST - AGENTIC AI")
print("=" * 60)

# Test stock analysis
print("\n📊 Testing AI Stock Analysis...")
print("Analyzing RELIANCE.NS...")

analyzer = SimpleAgenticStockAnalysis()

start_time = time.time()
result = analyzer.analyze_stock('RELIANCE.NS')
end_time = time.time()

if result['success']:
    print(f"\n✅ Analysis Complete! (took {end_time - start_time:.1f} seconds)")
    print("\n" + "=" * 60)
    print("AI ANALYSIS RESULT:")
    print("=" * 60)
    print(result['analysis'])
    print("=" * 60)
    print("\n🎉 SUCCESS! Your Agentic AI is working perfectly!")
else:
    print(f"\n❌ Analysis Failed: {result.get('error', 'Unknown error')}")
    print("\n💡 Troubleshooting:")
    print("1. Check internet connection")
    print("2. Verify API key is correct")
    print("3. Try again in a few seconds")

print("\n" + "=" * 60)
print("✅ Test Complete!")
print("=" * 60)
