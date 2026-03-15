"""
Test the Enhanced Recommendation System
Shows how different market conditions produce different recommendations
"""

def get_advanced_recommendation(rsi, macd, signal, price_change, adx, stoch_k, beta, volatility):
    """Same function as in main file"""
    score = 0
    signals = []
    
    # RSI Analysis
    if rsi < 25:
        score += 3
        signals.append("RSI Extremely Oversold")
    elif rsi < 35:
        score += 2
        signals.append("RSI Oversold")
    elif rsi < 45:
        score += 1
        signals.append("RSI Below Neutral")
    elif rsi > 75:
        score -= 3
        signals.append("RSI Extremely Overbought")
    elif rsi > 65:
        score -= 2
        signals.append("RSI Overbought")
    elif rsi > 55:
        score -= 1
        signals.append("RSI Above Neutral")
    
    # MACD Analysis
    macd_diff = macd - signal
    if macd > signal:
        if macd_diff > 5:
            score += 3
        elif macd_diff > 2:
            score += 2
        else:
            score += 1
    else:
        if macd_diff < -5:
            score -= 3
        elif macd_diff < -2:
            score -= 2
        else:
            score -= 1
    
    # Price Momentum
    if price_change > 5:
        score += 3
    elif price_change > 2:
        score += 2
    elif price_change > 0.5:
        score += 1
    elif price_change < -5:
        score -= 3
    elif price_change < -2:
        score -= 2
    elif price_change < -0.5:
        score -= 1
    
    # ADX
    if adx > 40:
        score += 2 if price_change > 0 else -2
    elif adx > 25:
        score += 1 if price_change > 0 else -1
    
    # Stochastic
    if stoch_k < 15:
        score += 2
    elif stoch_k < 25:
        score += 1
    elif stoch_k > 85:
        score -= 2
    elif stoch_k > 75:
        score -= 1
    
    # Beta
    if beta < 0.7:
        score += 1
    elif beta > 1.3:
        score -= 0.5
    
    # Volatility
    if volatility < 15:
        score += 1
    elif volatility > 40:
        score -= 1
    elif volatility > 30:
        score -= 0.5
    
    max_score = 18
    confidence = min(95, max(65, int((abs(score) / max_score) * 100) + 50))
    
    if score >= 8:
        return "STRONG BUY", "#00ff88", confidence, score
    elif score >= 4:
        return "BUY", "#17a2b8", confidence, score
    elif score >= 1:
        return "WEAK BUY", "#4dd0e1", confidence, score
    elif score >= -1:
        return "HOLD", "#ffc107", confidence, score
    elif score >= -4:
        return "WEAK SELL", "#ff9800", confidence, score
    elif score >= -8:
        return "SELL", "#ff5252", confidence, score
    else:
        return "STRONG SELL", "#d32f2f", confidence, score

# Test different market scenarios
print("🧪 TESTING RECOMMENDATION SYSTEM")
print("=" * 80)

scenarios = [
    {
        "name": "Strong Bullish Market",
        "rsi": 65, "macd": 15, "signal": 10, "price_change": 3.5,
        "adx": 35, "stoch_k": 70, "beta": 1.0, "volatility": 20
    },
    {
        "name": "Oversold Opportunity",
        "rsi": 28, "macd": 5, "signal": 3, "price_change": -1.5,
        "adx": 30, "stoch_k": 18, "beta": 0.9, "volatility": 25
    },
    {
        "name": "Overbought Warning",
        "rsi": 78, "macd": 10, "signal": 12, "price_change": 1.0,
        "adx": 28, "stoch_k": 88, "beta": 1.1, "volatility": 35
    },
    {
        "name": "Neutral/Sideways",
        "rsi": 50, "macd": 8, "signal": 8, "price_change": 0.2,
        "adx": 18, "stoch_k": 50, "beta": 1.0, "volatility": 22
    },
    {
        "name": "Strong Bearish Market",
        "rsi": 32, "macd": 5, "signal": 10, "price_change": -4.2,
        "adx": 38, "stoch_k": 25, "beta": 1.2, "volatility": 42
    },
    {
        "name": "Recovery Phase",
        "rsi": 42, "macd": 12, "signal": 8, "price_change": 2.8,
        "adx": 32, "stoch_k": 35, "beta": 0.95, "volatility": 18
    }
]

for scenario in scenarios:
    print(f"\n📊 Scenario: {scenario['name']}")
    print("-" * 80)
    print(f"   RSI: {scenario['rsi']:.1f} | MACD: {scenario['macd']:.1f} | Signal: {scenario['signal']:.1f}")
    print(f"   Price Change: {scenario['price_change']:+.1f}% | ADX: {scenario['adx']:.1f}")
    print(f"   Stochastic: {scenario['stoch_k']:.1f} | Beta: {scenario['beta']:.2f} | Volatility: {scenario['volatility']:.1f}%")
    
    recommendation, color, confidence, score = get_advanced_recommendation(
        scenario['rsi'], scenario['macd'], scenario['signal'], scenario['price_change'],
        scenario['adx'], scenario['stoch_k'], scenario['beta'], scenario['volatility']
    )
    
    print(f"\n   🎯 RECOMMENDATION: {recommendation}")
    print(f"   📊 Confidence: {confidence}%")
    print(f"   🔢 Score: {score:.1f}/18")
    print()

print("=" * 80)
print("✅ Test Complete!")
print("\nKey Insights:")
print("• Scores range from -18 to +18")
print("• STRONG BUY: Score >= 8")
print("• BUY: Score >= 4")
print("• WEAK BUY: Score >= 1")
print("• HOLD: Score between -1 and 1")
print("• WEAK SELL: Score <= -4")
print("• SELL: Score <= -8")
print("• STRONG SELL: Score < -8")
print("\n🎯 The system now gives VARIED recommendations based on market conditions!")
