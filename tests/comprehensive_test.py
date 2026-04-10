#!/usr/bin/env python3
"""
COMPREHENSIVE END-TO-END FUNCTIONALITY TEST
Tests all features from Phase 1 to Final Phase
"""

import sys
import traceback
from datetime import datetime
import pandas as pd

def test_phase_1_core_functionality():
    """Test Phase 1: Core Stock Analysis"""
    print("\n🚀 PHASE 1 TESTING: Core Stock Analysis")
    print("=" * 60)
    
    try:
        # Test 1: Configuration and Data Collection
        print("📦 Test 1.1: Configuration & Data Collection")
        import config
        import data_collector
        
        collector = data_collector.DataCollector()
        data = collector.get_stock_data("HDFCBANK.NS")
        print(f"✅ Stock data collected: {len(data)} records for HDFC Bank")
        
        # Test 2: Stock Analysis
        print("📊 Test 1.2: Stock Analysis Engine")
        import stock_analyzer
        
        analyzer = stock_analyzer.AdvancedStockAnalyzer()
        analysis = analyzer.analyze_stock("HDFCBANK.NS")
        print(f"✅ Stock analysis complete: {analysis.get('recommendation', 'N/A')}")
        
        # Test 3: Sentiment Analysis
        print("📰 Test 1.3: Sentiment Analysis")
        import sentiment_analyzer
        
        sentiment = sentiment_analyzer.SentimentAnalyzer()
        score = sentiment.analyze_stock_sentiment("HDFC Bank")
        print(f"✅ Sentiment analysis: {score:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Phase 1 Error: {e}")
        return False

def test_phase_2_advanced_features():
    """Test Phase 2: Advanced Analytics"""
    print("\n🚀 PHASE 2 TESTING: Advanced Analytics")
    print("=" * 60)
    
    try:
        # Test 1: Market Intelligence
        print("🧠 Test 2.1: Market Intelligence")
        import market_intelligence
        
        market_intel = market_intelligence.AdvancedMarketIntelligence()
        insights = market_intel.get_market_insights()
        print(f"✅ Market insights generated: {len(insights)} insights")
        
        # Test 2: Professional Analysis
        print("💼 Test 2.2: Professional Analysis")
        import professional_analyzer
        
        prof_analyzer = professional_analyzer.ProfessionalAnalyzer()
        report = prof_analyzer.generate_comprehensive_report("HDFCBANK.NS")
        print(f"✅ Professional report: {report['overall_rating']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Phase 2 Error: {e}")
        return False

def test_phase_3_ipo_intelligence():
    """Test Phase 3: IPO Intelligence (UNIQUE FEATURE)"""
    print("\n🚀 PHASE 3 TESTING: IPO Intelligence System")
    print("=" * 60)
    
    try:
        # Test 1: IPO Data Collection
        print("📊 Test 3.1: IPO Data Collection")
        import ipo_data_collector
        
        ipo_collector = ipo_data_collector.IPODataCollector()
        ipos = ipo_collector.comprehensive_ipo_data_collection()
        print(f"✅ IPO data collected: {len(ipos)} IPOs")
        
        # Test 2: IPO Intelligence Analysis
        print("🧠 Test 3.2: IPO Intelligence Analysis")
        import ipo_intelligence
        
        ipo_intel = ipo_intelligence.IPOIntelligenceSystem()
        if ipos:
            analysis = ipo_intel.analyze_ipo_performance(ipos[0].get('symbol', 'TATATECH.NS'))
            print(f"✅ IPO analysis complete: {analysis.get('recommendation', 'N/A')}")
        
        # Test 3: IPO Prediction Engine
        print("🤖 Test 3.3: IPO Prediction Engine")
        import ipo_predictor
        
        predictor = ipo_predictor.IPOPredictor()
        if ipos:
            prediction = predictor.predict_ipo_success(ipos[0])
            print(f"✅ IPO prediction: {prediction:.2f}% success probability")
        
        return True
        
    except Exception as e:
        print(f"❌ Phase 3 Error: {e}")
        return False

def test_phase_4_complete_platform():
    """Test Phase 4: Complete Investment Platform"""
    print("\n🚀 PHASE 4 TESTING: Complete Investment Platform")
    print("=" * 60)
    
    try:
        # Test 1: AI Investment Assistant
        print("🤖 Test 4.1: AI Investment Assistant")
        import ai_investment_assistant
        
        ai_assistant = ai_investment_assistant.AIInvestmentAssistant()
        response = ai_assistant.process_user_query("Should I invest in technology stocks?")
        print(f"✅ AI Assistant response: {response.get('confidence', 0)}% confidence")
        
        # Test 2: Mutual Fund & SIP System
        print("💰 Test 4.2: Mutual Fund & SIP System")
        import mutual_fund_sip_system
        
        mf_system = mutual_fund_sip_system.MutualFundSIPSystem()
        recommendations = mf_system.get_sip_recommendations(10000)
        print(f"✅ SIP recommendations: {recommendations['expected_return']:.2f}% return")
        
        # Test 3: Comprehensive Risk Management
        print("🛡️ Test 4.3: Risk Management System")
        import comprehensive_risk_management
        
        risk_manager = comprehensive_risk_management.ComprehensiveRiskManagement()
        portfolio = ['HDFCBANK.NS', 'INFY.NS', 'TCS.NS']
        risk_analysis = risk_manager.analyze_portfolio_risk(portfolio)
        print(f"✅ Risk analysis: {risk_analysis['risk_rating']}")
        
        # Test 4: Advanced Analytics & Alerts
        print("📈 Test 4.4: Advanced Analytics & Alerts")
        import advanced_analytics_alerts
        
        analytics = advanced_analytics_alerts.AdvancedAnalyticsSystem()
        heat_map = analytics.generate_market_heatmap()
        print(f"✅ Market heat map: {len(heat_map)} sectors analyzed")
        
        return True
        
    except Exception as e:
        print(f"❌ Phase 4 Error: {e}")
        return False

def test_unique_features():
    """Test Unique Features that solve the Problem Statement"""
    print("\n🚀 UNIQUE FEATURES TESTING: Problem Statement Solutions")
    print("=" * 70)
    
    try:
        # Test 1: Advanced IPO Post-listing Analysis
        print("🎯 Test U.1: Advanced IPO Post-listing Analysis")
        import ipo_intelligence
        
        ipo_intel = ipo_intelligence.IPOIntelligenceSystem()
        # Test with a real IPO
        analysis = ipo_intel.analyze_ipo_performance("TATATECH.NS")
        print(f"✅ Post-listing analysis: {analysis.get('performance_30d', 'N/A')}% in 30 days")
        
        # Test 2: Sentiment-based Predictions
        print("📰 Test U.2: Sentiment-based IPO Predictions")
        sentiment_score = ipo_intel.analyze_ipo_sentiment("Tata Technologies Limited")
        print(f"✅ Sentiment prediction: {sentiment_score:.3f} sentiment score")
        
        # Test 3: Retail Investor Exit Strategies
        print("🎯 Test U.3: Retail Investor Exit Strategies")
        recommendation = ipo_intel.generate_ipo_recommendation("TATATECH.NS")
        print(f"✅ Exit strategy: {recommendation.get('action', 'N/A')} recommendation")
        
        # Test 4: Real-time Market Data Integration
        print("📊 Test U.4: Real-time Market Data Integration")
        import data_collector
        
        collector = data_collector.DataCollector()
        live_data = collector.get_live_market_data()
        print(f"✅ Live data: NIFTY at {live_data.get('NIFTY_50', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Unique Features Error: {e}")
        return False

def main():
    """Run comprehensive end-to-end testing"""
    print("🚀 COMPREHENSIVE END-TO-END FUNCTIONALITY TEST")
    print("=" * 80)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    results = []
    
    # Test all phases
    results.append(("Phase 1: Core Functionality", test_phase_1_core_functionality()))
    results.append(("Phase 2: Advanced Features", test_phase_2_advanced_features()))
    results.append(("Phase 3: IPO Intelligence", test_phase_3_ipo_intelligence()))
    results.append(("Phase 4: Complete Platform", test_phase_4_complete_platform()))
    results.append(("Unique Features", test_unique_features()))
    
    # Summary
    print("\n" + "=" * 80)
    print("🏆 COMPREHENSIVE TEST RESULTS")
    print("=" * 80)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    success_rate = (passed / total) * 100
    print(f"\n📊 Success Rate: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate == 100:
        print("\n🎉 ALL TESTS PASSED - PLATFORM FULLY FUNCTIONAL!")
        print("🚀 Ready for production deployment and presentation!")
    else:
        print(f"\n⚠️ {total - passed} tests failed - needs attention")
    
    return success_rate == 100

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)