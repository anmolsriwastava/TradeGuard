import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.disruption_radar import disruption_signals
from utils.scoring import score_news_from_articles


class ImpactAssessor:
    def __init__(self):
        pass
    
    def assess_shipment_risk(self, shipment, risk_score, risk_level):
        """Calculate risk for a specific shipment"""
        return {
            "shipment_id": shipment.get("shipment_id", ""),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "predicted_delay_days_min": 4 if risk_score >= 70 else 2 if risk_score >= 50 else 1,
            "predicted_delay_days_max": 7 if risk_score >= 70 else 4 if risk_score >= 50 else 2,
            "financial_exposure_inr": risk_score * 1000,
            "delay_probability": risk_score / 100
        }