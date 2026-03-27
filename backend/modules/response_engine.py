class ResponseEngine:
    
    def __init__(self):
        self.alternative_routes = {
            "INNSA-AEJEA": [
                {"route": "Direct via Jebel Ali", "extra_cost": 0, "extra_days": 0, "co2": 0},
                {"route": "Tranship via Colombo", "extra_cost": 18000, "extra_days": 1, "co2": 2},
                {"route": "Alternate: Mundra", "extra_cost": 8000, "extra_days": 2, "co2": -5}
            ]
        }
    
    def generate_response_options(self, shipment, risk_level, risk_score):
        return [
            {
                "option_id": 1,
                "title": "Alternative Route Available",
                "description": f"Switch to alternate vessel to avoid {risk_level.lower()} risk corridor",
                "extra_cost_inr": 15000,
                "extra_days": 2,
                "recommended": True
            },
            {
                "option_id": 2,
                "title": "Proactive Buyer Communication",
                "description": "Auto-generate force majeure notification to buyer",
                "extra_cost_inr": 0,
                "extra_days": 0,
                "recommended": False
            },
            {
                "option_id": 3,
                "title": "Expedited Clearance",
                "description": "Priority handling at destination port",
                "extra_cost_inr": 12000,
                "extra_days": -1,
                "recommended": False
            }
        ]