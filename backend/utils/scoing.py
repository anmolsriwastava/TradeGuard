def score_news_from_articles(news_articles):
    """Convert news articles to risk score (0-100)"""
    if not news_articles:
        return 20
    
    score = 0
    for article in news_articles:
        text = (article.get("title", "") + " " + article.get("description", "")).lower()
        
        # Crisis keywords (high impact)
        crisis_words = ["war", "attack", "crisis", "strike", "blocked", "closed", "halted"]
        if any(word in text for word in crisis_words):
            score += 25
        
        # Disruption keywords (medium impact)
        disruption_words = ["delay", "congestion", "disruption", "backlog", "slow", "waiting"]
        if any(word in text for word in disruption_words):
            score += 15
        
        # Price/trend keywords (low impact)
        trend_words = ["price", "surge", "shortage", "rising", "increase", "spike"]
        if any(word in text for word in trend_words):
            score += 8
    
    return min(score, 100)


def calculate_risk(weather, news_score):
    """Calculate combined risk score from weather and news"""
    weather_score = 0
    
    if weather.get("wind", 0) > 10:
        weather_score += 40
    
    if weather.get("weather", "") in ["Storm", "Rain", "Cyclone"]:
        weather_score += 30
    
    risk = 0.6 * weather_score + 0.4 * news_score
    return min(100, risk)