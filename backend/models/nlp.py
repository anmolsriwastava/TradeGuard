from transformers import pipeline

classifier = pipeline("sentiment-analysis")

def analyze_news(news):
    
    scores = []
    
    for text in news:
        result = classifier(text)[0]
        
        if result["label"] == "NEGATIVE":
            scores.append(80)
        else:
            scores.append(20)
    
    return sum(scores) / len(scores)