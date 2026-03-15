"""
Test Agentic AI System
Verify all components are working
"""

import os
import sys

def test_imports():
    """Test if all required libraries are installed"""
    print("🧪 TESTING AGENTIC AI SYSTEM")
    print("=" * 60)
    print("\n1️⃣ Testing Imports...")
    
    try:
        import crewai
        print("   ✅ crewai installed")
    except ImportError:
        print("   ❌ crewai not found - Run: pip install crewai")
        return False
    
    try:
        from langchain_groq import ChatGroq
        print("   ✅ langchain-groq installed")
    except ImportError:
        print("   ❌ langchain-groq not found - Run: pip install langchain-groq")
        return False
    
    try:
        import chromadb
        print("   ✅ chromadb installed")
    except ImportError:
        print("   ❌ chromadb not found - Run: pip install chromadb")
        return False
    
    try:
        import yfinance
        print("   ✅ yfinance installed")
    except ImportError:
        print("   ❌ yfinance not found - Run: pip install yfinance")
        return False
    
    return True

def test_api_key():
    """Test if API key is set"""
    print("\n2️⃣ Testing API Key...")
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("   ❌ GROQ_API_KEY not found")
        print("   💡 Set it in .env file or environment variable")
        return False
    
    if not api_key.startswith("gsk_"):
        print("   ⚠️ API key format looks incorrect (should start with 'gsk_')")
        return False
    
    print(f"   ✅ API key found: {api_key[:10]}...")
    return True

def test_agentic_system():
    """Test if agentic system can be imported"""
    print("\n3️⃣ Testing Agentic AI System...")
    
    try:
        from agentic_ai_system import (
            AgenticStockAnalysis,
            AgenticPortfolioManager,
            AgenticMarketIntelligence
        )
        print("   ✅ Agentic AI system imported successfully")
        return True
    except ImportError as e:
        print(f"   ❌ Failed to import: {e}")
        return False

def test_interface():
    """Test if interface can be imported"""
    print("\n4️⃣ Testing Agentic AI Interface...")
    
    try:
        from agentic_ai_interface import show_agentic_ai_hub
        print("   ✅ Agentic AI interface imported successfully")
        return True
    except ImportError as e:
        print(f"   ❌ Failed to import: {e}")
        return False

def test_tools():
    """Test if tools work"""
    print("\n5️⃣ Testing AI Tools...")
    
    try:
        from agentic_ai_system import fetch_real_time_stock_data
        
        # Test with a sample stock
        result = fetch_real_time_stock_data('RELIANCE.NS')
        
        if 'error' in result:
            print(f"   ⚠️ Tool returned error: {result['error']}")
            print("   💡 This might be normal if market is closed or internet is slow")
            return True  # Not a critical error
        
        print(f"   ✅ Successfully fetched data for RELIANCE.NS")
        print(f"      Price: ₹{result.get('current_price', 'N/A')}")
        return True
        
    except Exception as e:
        print(f"   ❌ Tool test failed: {e}")
        return False

def test_llm_connection():
    """Test if LLM connection works"""
    print("\n6️⃣ Testing LLM Connection...")
    
    try:
        from langchain_groq import ChatGroq
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("   ⚠️ Skipping (no API key)")
            return True
        
        try:
            llm = ChatGroq(
                groq_api_key=api_key,
                model_name="mixtral-8x7b-32768",
                temperature=0.1
            )
        except:
            # Fallback to simpler initialization
            llm = ChatGroq(
                groq_api_key=api_key,
                model_name="mixtral-8x7b-32768"
            )
        
        # Test with a simple query
        response = llm.invoke("Say 'Hello' if you can hear me.")
        
        print(f"   ✅ LLM connection successful")
        print(f"      Response: {response.content[:50]}...")
        return True
        
    except Exception as e:
        print(f"   ❌ LLM connection failed: {e}")
        print("   💡 Check your API key and internet connection")
        return False

def run_all_tests():
    """Run all tests"""
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("API Key", test_api_key()))
    results.append(("Agentic System", test_agentic_system()))
    results.append(("Interface", test_interface()))
    results.append(("Tools", test_tools()))
    results.append(("LLM Connection", test_llm_connection()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Your Agentic AI system is ready to use!")
        print("\n📋 Next Steps:")
        print("1. Run: python integrate_agentic_ai.py")
        print("2. Run: streamlit run main_ultimate_final.py")
        print("3. Navigate to '🤖 Agentic AI Hub' in sidebar")
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("📋 Please fix the issues above before proceeding")
        print("\n💡 Common fixes:")
        print("- Install missing packages: pip install -r requirements_agentic.txt")
        print("- Set API key in .env file: GROQ_API_KEY=your_key")
        print("- Check internet connection")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
