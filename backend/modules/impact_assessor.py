import json
import math
from datetime import datetime, date, timedelta
from typing import Dict, Tuple

class ImpactAssessor:
    """
    Module 2: Personalised Shipment Risk Engine
    """
    
    def __init__(self):
        with open('data/mock_shipments.json', 'r') as f:
            self.shipment_data = json.load(f)
    
    def estimate_delay_probability(self, risk_score: int, days_until_deadline: int) -> float:
        # Simplified logistic regression without numpy
        beta_0 = -2.5
        beta_1 = 0.05
        beta_2 = -0.15
        
        log_odds = beta_0 + (beta_1 * risk_score) + (beta_2 * days_until_deadline)
        
        # Manual exponential
        try:
            probability = 1 / (1 + math.exp(-log_odds))
        except:
            probability = 0.5
        
        if probability < 0.05:
            probability = 0.05
        if probability > 0.95:
            probability = 0.95
            
        return probability
    
    def estimate_delay_days(self, risk_score: int, risk_level: str) -> Tuple[int, int]:
        if risk_level == "CRITICAL":
            return (7, 14)
        elif risk_level == "HIGH":
            return (4, 7)
        elif risk_level == "MEDIUM":
            return (2, 4)
        else:
            return (0, 2)
    
    def calculate_financial_exposure(self, delay_probability: float, penalty_per_day: float, expected_delay_days: int, cargo_value: float) -> float:
        storage_cost_per_day = penalty_per_day * 0.05
        storage_total = storage_cost_per_day * expected_delay_days
        penalty_exposure = penalty_per_day * expected_delay_days
        total_exposure = delay_probability * (penalty_exposure + storage_total)
        return round(total_exposure, 2)
    
    def assess_shipment_risk(self, shipment: Dict, risk_score: int, risk_level: str) -> Dict:
        eta = datetime.strptime(shipment['eta'], '%Y-%m-%d').date()
        deadline = datetime.strptime(shipment['delivery_deadline'], '%Y-%m-%d').date()
        days_until_deadline = (deadline - date.today()).days
        
        delay_prob = self.estimate_delay_probability(risk_score, days_until_deadline)
        min_delay, max_delay = self.estimate_delay_days(risk_score, risk_level)
        expected_delay = (min_delay + max_delay) // 2
        
        financial_exposure = self.calculate_financial_exposure(
            delay_prob, shipment['penalty_per_day_inr'], expected_delay, shipment['cargo_value_inr']
        )
        
        if delay_prob > 0.7:
            breach_risk = "HIGH"
        elif delay_prob > 0.4:
            breach_risk = "MEDIUM"
        else:
            breach_risk = "LOW"
        
        return {
            "shipment_id": shipment['shipment_id'],
            "corridor_id": f"{shipment['origin_port']}-{shipment['destination_port']}",
            "risk_score": risk_score,
            "risk_level": risk_level,
            "predicted_delay_days_min": min_delay,
            "predicted_delay_days_max": max_delay,
            "delay_probability": round(delay_prob * 100, 1),
            "financial_exposure_inr": financial_exposure,
            "deadline_breach_risk": breach_risk
        }
    
    def get_alert_message(self, assessment: Dict) -> str:
        return f"""⚠️ TradeGuard Alert — {assessment['risk_level']} RISK

Container: {assessment.get('shipment_id', 'N/A')}
Risk Level: {assessment['risk_level']} (Score: {assessment['risk_score']}/100)

Predicted delay: {assessment['predicted_delay_days_min']}-{assessment['predicted_delay_days_max']} days ({assessment['delay_probability']}% confidence)

Penalty exposure: ₹{assessment['financial_exposure_inr']:,.0f} if deadline missed

3 response options ready. Tap to view."""