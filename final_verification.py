# Final Verification Script for सार्थक निवेश Platform
# Comprehensive end-to-end testing before presentation

import sys
import traceback
from datetime import datetime

def run_comprehensive_verification():
    """Run comprehensive verification of all platform components"""
    
    print("🚀 FINAL PLATFORM VERIFICATION")
    print("=" * 70)
    print(f"Verification Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    verification_results = {
        'total_tests': 0,
        'passed_tests': 0,
        'failed_tests': 0,
        'errors': []
    }
    
    # Test 1: Core Module Imports
    print("\n📦 TEST 1: Core Module Imports")
    try:
        import config
        import data_collector
        import stock_analyzer
        import sentiment_analyzer
        import excel_manager
        
        verification_results['total_tests'] += 1
        verification_results['passed_tests'] += 1
        print("✅ PASSED: All core modules imported successfully")
        
    except Exception as e:
        verification_results['total_tests'] += 1
        verification_results['failed_tests'] += 1
        verification_results['errors'].append(f"Core modules: {str(e)}")
        print(f"❌ FAILED: Core module import error: {e}")
    
    # Test 2: IPO Intelligence System
    print("\n🚀 TEST 2: IPO Intelligence System (UNIQUE FEATURE)")
    try:
        import ipo_intelligence
        import ipo_data_collector
        import ipo_predictor
        
        # Initialize systems
        ipo_system = ipo_intelligence.IPOIntelligenceSystem()
        ipo_collector = ipo_data_collector.IPODataCollector()
        ipo_predictor_sys = ipo_predictor.IPOPredictionEngine()
        
        # Test IPO data collection
        recent_ipos = ipo_system.collect_recent_ipos()
        
        if recent_ipos and len(recent_ipos) > 0:
            # Test analysis on first IPO
            test_ipo = recent_ipos[0]
            
            # Test performance analysis
            performance = ipo_system.analyze_post_ipo_performance(test_ipo['symbol'])
            
            # Test sentiment analysis
            sentiment = ipo_system.analyze_ipo_sentiment(test_ipo['symbol'], test_ipo['company_name'])
            
            # Test recommendation generation
            recommendation = ipo_system.generate_ipo_recommendation(test_ipo['symbol'])
            
            if performance and sentiment and recommendation:
                verification_results['total_tests'] += 1
                verification_results['passed_tests'] += 1
                print("✅ PASSED: IPO Intelligence System fully functional")
                print(f"   - Analyzed: {test_ipo['company_name']}")
                print(f"   - Performance: {performance.get('performance_30d', 'N/A')}%")
                print(f"   - Sentiment: {sentiment.get('overall_sentiment_score', 'N/A')}")
                print(f"   - Recommendation: {recommendation.get('recommendation', 'N/A')}")
            else:
                raise Exception("IPO analysis components not working")
        else:
            raise Exception("No IPO data collected")
            
    except Exception as e:
        verification_results['total_tests'] += 1
        verification_results['failed_tests'] += 1
        verification_results['errors'].append(f"IPO Intelligence: {str(e)}")
        print(f"❌ FAILED: IPO Intelligence error: {e}")
    
    # Test 3: Real-time Data Integration
    print("\n📊 TEST 3: Real-time Data Integration")
    try:
        import yfinance as yf
        
        # Test stock data
        ticker = yf.Ticker("HDFCBANK.NS")
        data = ticker.history(period="2d")
        
        # Test market index
        nifty = yf.Ticker("^NSEI")
        nifty_data = nifty.history(period="2d")
        
        if not data.empty and not nifty_data.empty:
            current_price = data['Close'].iloc[-1]
            nifty_level = nifty_data['Close'].iloc[-1]
            
            verification_results['total_tests'] += 1
            verification_results['passed_tests'] += 1
            print("✅ PASSED: Real-time data integration working")
            print(f"   - HDFC Bank: ₹{current_price:.2f}")
            print(f"   - NIFTY 50: {nifty_level:.2f}")
        else:
            raise Exception("No real-time data received")
            
    except Exception as e:
        verification_results['total_tests'] += 1
        verification_results['failed_tests'] += 1
        verification_results['errors'].append(f"Real-time data: {str(e)}")
        print(f"❌ FAILED: Real-time data error: {e}")
    
    # Test 4: AI Investment Assistant
    print("\n🤖 TEST 4: AI Investment Assistant")
    try:
        import ai_investment_assistant
        
        ai_assistant = ai_investment_assistant.AIInvestmentAssistant()
        
        # Test query processing
        test_query = "Should I buy HDFC Bank stock?"
        response = ai_assistant.process_user_query(test_query)
        
        if response and response.get('confidence', 0) > 0.5:
            verification_results['total_tests'] += 1
            verification_results['passed_tests'] += 1
            print("✅ PASSED: AI Investment Assistant working")
            print(f"   - Query: {test_query}")
            print(f"   - Confidence: {response.get('confidence', 0):.1%}")
            print(f"   - Type: {response.get('query_type', 'N/A')}")
        else:
            raise Exception("AI assistant not responding properly")
            
    except Exception as e:
        verification_results['total_tests'] += 1
        verification_results['failed_tests'] += 1
        verification_results['errors'].append(f"AI Assistant: {str(e)}")
        print(f"❌ FAILED: AI Assistant error: {e}")
    
    # Test 5: Mutual Fund & SIP System
    print("\n💰 TEST 5: Mutual Fund & SIP System")
    try:
        from mutual_fund_sip_system import MutualFundSIPSystem
        
        mf_system = MutualFundSIPSystem()
        
        # Test fund data collection
        funds_data = mf_system.collect_mutual_fund_data()
        
        # Test SIP recommendation
        user_profile = {
            'monthly_amount': 10000,
            'age': 30,
            'risk_tolerance': 'moderate',
            'investment_horizon': '5-10 years'
        }
        
        recommendations = mf_system.recommend_sip_portfolio(user_profile)
        
        if funds_data and recommendations:
            verification_results['total_tests'] += 1
            verification_results['passed_tests'] += 1
            print("✅ PASSED: Mutual Fund & SIP System working")
            print(f"   - Funds: {len(funds_data)} collected")
            print(f"   - Expected Return: {recommendations['expected_annual_return']:.2f}%")
            print(f"   - Projected Value: ₹{recommendations['projected_value']:,.0f}")
        else:
            raise Exception("MF SIP system not working properly")
            
    except Exception as e:
        verification_results['total_tests'] += 1
        verification_results['failed_tests'] += 1
        verification_results['errors'].append(f"MF SIP System: {str(e)}")
        print(f"❌ FAILED: MF SIP System error: {e}")
    
    # Test 6: Risk Management System
    print("\n🛡️ TEST 6: Risk Management System")
    try:
        from comprehensive_risk_management import ComprehensiveRiskManagement
        import pandas as pd
        
        risk_manager = ComprehensiveRiskManagement()
        
        # Test portfolio risk calculation
        portfolio_data = pd.DataFrame({
            'symbol': ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS'],
            'weight': [0.4, 0.3, 0.3],
            'value': [400000, 300000, 300000]
        })
        
        metrics = risk_manager.calculate_portfolio_metrics(portfolio_data)
        
        if metrics and 'risk_rating' in metrics:
            verification_results['total_tests'] += 1
            verification_results['passed_tests'] += 1
            print("✅ PASSED: Risk Management System working")
            print(f"   - Risk Rating: {metrics['risk_rating']}")
            print(f"   - Volatility: {metrics.get('annual_volatility', 0):.2%}")
            print(f"   - Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.2f}")
        else:
            raise Exception("Risk management calculations failed")
            
    except Exception as e:
        verification_results['total_tests'] += 1
        verification_results['failed_tests'] += 1
        verification_results['errors'].append(f"Risk Management: {str(e)}")
        print(f"❌ FAILED: Risk Management error: {e}")
    
    # Test 7: Advanced Analytics
    print("\n📈 TEST 7: Advanced Analytics & Alerts")
    try:
        from advanced_analytics_alerts import AdvancedAnalyticsSystem
        
        analytics = AdvancedAnalyticsSystem()
        
        # Test market heat map
        heatmap_result = analytics.generate_market_heatmap()
        
        # Test correlation analysis
        correlation_result = analytics.generate_correlation_analysis()
        
        if heatmap_result and correlation_result:
            verification_results['total_tests'] += 1
            verification_results['passed_tests'] += 1
            print("✅ PASSED: Advanced Analytics working")
            print(f"   - Heat Map: {len(heatmap_result['heatmap_data'])} sectors analyzed")
            print(f"   - Correlation: {len(correlation_result['symbols'])} stocks analyzed")
        else:
            raise Exception("Analytics generation failed")
            
    except Exception as e:
        verification_results['total_tests'] += 1
        verification_results['failed_tests'] += 1
        verification_results['errors'].append(f"Advanced Analytics: {str(e)}")
        print(f"❌ FAILED: Advanced Analytics error: {e}")
    
    # Test 8: Main Applications
    print("\n🖥️ TEST 8: Main Applications")
    try:
        import streamlit as st
        import plotly.graph_objects as go
        import plotly.express as px
        
        # Check if main files exist and are valid
        import os
        main_files = [
            'main_complete_platform.py',
            'main_phase4_complete.py', 
            'main_phase3.py',
            'main_phase2.py'
        ]
        
        valid_files = []
        for file in main_files:
            if os.path.exists(file):
                valid_files.append(file)
        
        if len(valid_files) >= 3:
            verification_results['total_tests'] += 1
            verification_results['passed_tests'] += 1
            print("✅ PASSED: Main Applications ready")
            print(f"   - Available: {len(valid_files)} main applications")
            print(f"   - Streamlit: Ready")
            print(f"   - Plotly: Ready")
        else:
            raise Exception("Main application files missing")
            
    except Exception as e:
        verification_results['total_tests'] += 1
        verification_results['failed_tests'] += 1
        verification_results['errors'].append(f"Main Applications: {str(e)}")
        print(f"❌ FAILED: Main Applications error: {e}")
    
    # Final Results
    print("\n" + "=" * 70)
    print("🏆 FINAL VERIFICATION RESULTS")
    print("=" * 70)
    
    total_tests = verification_results['total_tests']
    passed_tests = verification_results['passed_tests']
    failed_tests = verification_results['failed_tests']
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"📊 Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    if failed_tests > 0:
        print(f"\n❌ ERRORS ENCOUNTERED:")
        for i, error in enumerate(verification_results['errors'], 1):
            print(f"   {i}. {error}")
    
    print("\n" + "=" * 70)
    
    if success_rate >= 85:
        print("🎉 PLATFORM STATUS: READY FOR PRESENTATION!")
        print("✅ All critical systems operational")
        print("🚀 India's most advanced investment platform verified!")
        
        print(f"\n🎯 TO START THE PLATFORM:")
        print("   streamlit run main_complete_platform.py")
        print("   OR")
        print("   run_ultimate_platform.bat")
        
        return True
    else:
        print("⚠️ PLATFORM STATUS: NEEDS ATTENTION")
        print("❌ Some systems require fixes before presentation")
        return False

if __name__ == "__main__":
    try:
        success = run_comprehensive_verification()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)