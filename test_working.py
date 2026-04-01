import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

print("=" * 60)
print("TRADEGUARD NEWS TEST")
print("=" * 60)

# Check if API key exists
if not NEWS_API_KEY:
    print("\n❌ ERROR: NEWS_API_KEY not found in .env file")
    print("   Please add: NEWS_API_KEY=your_key_here")
    exit()
else:
    print(f"\n✓ API Key found: {NEWS_API_KEY[:10]}...")

# Fetch news
print("\n📡 Fetching news...")

query = "port congestion OR shipping disruption OR freight delay"
url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}&pageSize=10"

try:
    response = requests.get(url, timeout=10)
    data = response.json()
    
    if data.get("status") == "error":
        print(f"\n❌ API Error: {data.get('message')}")
        exit()
    
    articles = data.get("articles", [])
    print(f"\n✓ Found {len(articles)} total articles")
    
    # Filter relevant news
    keywords = ["shipping", "port", "logistics", "freight", "cargo", "vessel", 
                "supply chain", "container", "maritime", "delay", "congestion"]
    
    relevant = []
    for article in articles:
        title = article.get("title", "").lower()
        desc = article.get("description", "").lower()
        text = title + " " + desc
        
        if any(k in text for k in keywords):
            relevant.append(article)
    
    print(f"✓ Found {len(relevant)} supply chain related articles\n")
    
    # Show results
    if relevant:
        for i, article in enumerate(relevant[:5], 1):
            title = article.get("title", "No title")
            print(f"{i}. {title[:100]}")
            print()
    else:
        print("No relevant articles found. Try different query.")
        
        # Try alternative query
        print("\nTrying alternative query...")
        alt_query = "maritime OR shipping OR logistics"
        alt_url = f"https://newsapi.org/v2/everything?q={alt_query}&apiKey={NEWS_API_KEY}&pageSize=5"
        alt_response = requests.get(alt_url, timeout=10)
        alt_data = alt_response.json()
        
        for article in alt_data.get("articles", [])[:3]:
            print(f"- {article.get('title', 'No title')[:80]}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPossible issues:")
    print("1. No internet connection")
    print("2. NewsAPI key is invalid")
    print("3. Rate limit exceeded")

print("\n" + "=" * 60)