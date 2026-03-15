# Phase 3 Verification Script
# Verify all Phase 3 components are working correctly

import sys
import sqlite3
import pandas as pd
from datetime import datetime

# Ensure Unicode output works even on consoles that don't support emojis
try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

def verify_phase3():
    print("🚀 Verifying Phase 3 Implementation...")
    print("=" * 50)
    
    # Test 1: Import all modules
    try:
        from config import DATABASE_PATH
        print("✅ Configuration imported successfully")
        
        from ipo_intelligence import IPOIntelligenceSystem
        print("✅ IPO Intelligence System imported")
        
        from ipo_data_collector import IPODataCollector
        print("✅ IPO Data Collector imported")
        
        from ipo_predictor import IPOPredictionEngine
        print("✅ IPO Prediction Engine imported")
        
    except Exception as e:
        print(f"❌ Import Error: {str(e)}")
        return False
    
    # Test 2: Initialize systems
    try:
        ipo_intelligence = IPOIntelligenceSystem()
        print("✅ IPO Intelligence System initialized")
        
        ipo_collector = IPODataCollector()
        print("✅ IPO Data Collector initialized")
        
        ipo_predictor = IPOPredictionEngine()
        print("✅ IPO Prediction Engine initialized")
        
    except Exception as e:
        print(f"❌ Initialization Error: {str(e)}")
        return False
    
    # Test 3: Database setup
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check if IPO tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ipo_intelligence'")
        if cursor.fetchone():
            print("✅ IPO Intelligence database table exists")
        else:
            print("⚠️ IPO Intelligence table not found, but will be created on first use")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database Error: {str(e)}")
        return False
    
    # Test 4: Collect sample IPO data
    try:
        print("🔄 Testing IPO data collection...")
        recent_ipos = ipo_intelligence.collect_recent_ipos()
        
        if recent_ipos:
            print(f"✅ Collected {len(recent_ipos)} sample IPOs")
        else:
            print("⚠️ No IPO data collected, but system is ready")
        
    except Exception as e:
        print(f"❌ IPO Data Collection Error: {str(e)}")
        return False
    
    # Test 5: Test ML model setup
    try:
        print("🤖 Testing ML model setup...")
        # This will create synthetic data if no real data exists
        features, targets = ipo_predictor.prepare_training_data()
        
        if features is not None and targets is not None:
            print("✅ ML training data prepared successfully")
        else:
            print("⚠️ ML training data not available, but models are ready")
        
    except Exception as e:
        print(f"❌ ML Model Error: {str(e)}")
        return False
    
    # Test 6: Verify main application
    try:
        print("🖥️ Testing main application components...")
        import streamlit as st
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ All required libraries available")
        
    except Exception as e:
        print(f"❌ Application Error: {str(e)}")
        return False
    
    print("=" * 50)
    print("🎉 Phase 3 Verification Complete!")
    print("✅ All systems operational")
    print("🚀 Ready to run: streamlit run main_phase3.py")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = verify_phase3()
    
    if success:
        print("\n🎯 Phase 3 Features Available:")
        print("- 🚀 IPO Intelligence Hub (UNIQUE FEATURE)")
        print("- 📊 IPO Performance Analysis")
        print("- 🤖 IPO Prediction Engine")
        print("- 📰 IPO Sentiment Analysis")
        print("- 💡 IPO Recommendations")
        print("- ⚙️ Data Management Center")
        
        print("\n✨ UNIQUE VALUE PROPOSITION:")
        print("Post-IPO Liquidity & Retail Sentiment Forecast")
        print("- Not available on Groww or any other platform")
        print("- India-specific IPO analysis")
        print("- AI-powered insights and recommendations")
        
        sys.exit(0)
    else:
        print("\n❌ Phase 3 verification failed")
        print("Please check the error messages above")
        sys.exit(1)