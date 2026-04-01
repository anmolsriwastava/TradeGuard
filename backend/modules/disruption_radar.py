import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news():
    """Fetch and filter supply chain relevant news"""
    
    if not NEWS_API_KEY:
        return []
    
    # Better query for supply chain disruptions
    query = "port congestion OR shipping disruption OR freight delay OR maritime crisis OR supply chain"
    
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}&language=en&pageSize=10"
    
    try:
        res = requests.get(url, timeout=10).json()
    except:
        return []
    
    # Keywords to filter relevant news
    relevant_keywords = [
        "shipping", "port", "logistics", "freight", "cargo", "vessel",
        "supply chain", "container", "maritime", "oil", "strait", "canal",
        "delay", "congestion", "strike", "disruption", "blocked", "closed"
    ]
    
    filtered = []
    
    for article in res.get("articles", []):
        title = article.get("title", "").lower()
        description = article.get("description", "").lower()
        
        text = title + " " + description
        
        if any(word in text for word in relevant_keywords):
            filtered.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", "")
            })
    
    return filtered[:5]  # Return top 5 relevant news


def disruption_signals():
    """Get all disruption signals"""
    news = get_news()
    
    return {
        "news": news
    }


# Quick test
if __name__ == "__main__":
    signals = disruption_signals()
    print("News found:", len(signals["news"]))
    for n in signals["news"]:
        print("-", n["title"][:80])