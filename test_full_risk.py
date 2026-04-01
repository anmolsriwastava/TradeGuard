import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news():
    """Fetch and score supply chain news"""
    
    query = "port congestion OR shipping disruption OR freight delay OR supply chain crisis"
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}&pageSize=10"
    
    try:
        res = requests.get(url, timeout=10).json()
        articles = res.get("articles", [])
        
        # Filter relevant news
        keywords = ["shipping", "port", "logistics", "freight", "cargo", "vessel", 
                    "supply chain", "container", "maritime", "delay", "congestion", 
                    "disruption", "crisis", "strike", "blocked"]
        
        relevant = []
        for article in articles:
            title = article.get("title", "").lower()
            desc = article.get("description", "").lower()
            text = title + " " + desc
            
            if any(k in text for k in keywords):
                relevant.append(article)
        
        return relevant[:5]
    except:
        return []

def score_news(news_articles):
    """Calculate risk score from news"""
    
    if not news_articles:
        return 20
    
    score = 0
    
    for article in news_articles:
        text = (article.get("title", "") + " " + article.get("description", "")).lower()
        
        # Crisis level (score +25)
        crisis_words = ["war", "attack", "strike", "blocked", "closed", "halted", "crisis"]
        if any(word in text for word in crisis_words):
            score += 25
            print(f"  ⚠️ Crisis detected: {article['title'][:60]}")
        
        # Disruption level (score +15)
        disruption_words = ["delay", "congestion", "disruption", "backlog", "slow", "waiting"]
        if any(word in text for word in disruption_words):
            score += 15
            print(f"  📉 Disruption detected: {article['title'][:60]}")
        
        # Price/trend (score +8)
        trend_words = ["price", "surge", "shortage", "rising", "increase", "spike"]
        if any(word in text for word in trend_words):
            score += 8
            print(f"  📈 Price trend: {article['title'][:60]}")
    
    return min(score, 100)

print("=" * 60)
print("TRADEGUARD RISK SCORING SYSTEM")
print("=" * 60)

# Get news
print("\n📡 Fetching news...")
news = get_news()

print(f"\n📰 Found {len(news)} relevant articles:\n")
for i, article in enumerate(news, 1):
    print(f"{i}. {article.get('title', 'No title')}")

# Score news
print("\n🎯 Analyzing risk signals...\n")
risk_score = score_news(news)

print(f"\n{'='*60}")
print(f"FINAL RISK SCORE: {risk_score}/100")
print(f"{'='*60}")

# Risk level
if risk_score >= 70:
    print("⚠️  CRITICAL - Immediate action required")
elif risk_score >= 50:
    print("⚠️  HIGH - Monitor closely")
elif risk_score >= 30:
    print("📊 MEDIUM - Review options")
else:
    print("✅ LOW - Normal operations")

print("\n💡 Recommended Action:")
if risk_score >= 70:
    print("   → Transship via alternate route")
    print("   → Notify buyers immediately")
elif risk_score >= 50:
    print("   → Prepare contingency plans")
    print("   → Monitor corridor daily")
elif risk_score >= 30:
    print("   → Review options, no immediate action")
else:
    print("   → Proceed normally")

print("\n" + "=" * 60)