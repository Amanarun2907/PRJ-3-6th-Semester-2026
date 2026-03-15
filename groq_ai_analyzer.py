"""
Groq AI Analyzer for News & Market Insights
Uses Groq API for advanced market analysis
"""

import requests

class GroqAIAnalyzer:
    """AI-powered market analysis using Groq"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def analyze_market_sentiment(self, news_items):
        """Get AI analysis of overall market sentiment"""
        try:
            news_summary = "\n".join([
                f"- {n['title']} (Sentiment: {n['sentiment_analysis']['sentiment']})"
                for n in news_items[:10]
            ])
            
            prompt = f"""Analyze recent Indian market news:

{news_summary}

Provide:
1. Overall sentiment (Bullish/Bearish/Neutral)
2. Key drivers (3 points)
3. Sectors to watch
4. Short-term outlook

Keep under 150 words."""
            
            return self._call_groq(prompt)
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_news_summary(self, news_items):
        """Get AI summary of top news"""
        try:
            news_text = "\n".join([f"{i+1}. {n['title']}" for i, n in enumerate(news_items[:8])])
            
            prompt = f"""Summarize these Indian market news in 3-4 key points:

{news_text}"""
            
            return self._call_groq(prompt)
        except Exception as e:
            return None
    
    def _call_groq(self, prompt):
        """Make API call to Groq"""
        try:
            payload = {
                "messages": [
                    {"role": "system", "content": "You are an expert Indian stock market analyst."},
                    {"role": "user", "content": prompt}
                ],
                "model": "llama-3.3-70b-versatile",
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                print(f"Groq API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error calling Groq: {e}")
            return None


if __name__ == "__main__":
    print("🤖 Testing Groq AI...")
    analyzer = GroqAIAnalyzer("your_groq_api_key_here")
    
    sample = [{'title': 'Sensex gains 500 points', 'sentiment_analysis': {'sentiment': 'Positive'}}]
    result = analyzer.analyze_market_sentiment(sample)
    
    if result:
        print(f"✅ Success:\n{result}")
    else:
        print("❌ Failed")
