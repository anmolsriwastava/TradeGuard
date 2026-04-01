import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import directly from the file
from modules.disruption_radar import get_news

# Test the function
print("Fetching news...")
news = get_news()

print(f"\nFound {len(news)} relevant news articles:\n")

for i, article in enumerate(news, 1):
    print(f"{i}. {article['title']}")
    print(f"   {article['description'][:100]}...")
    print()