from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import json
from datetime import datetime

from modules.disruption_radar import DisruptionRadar
from modules.impact_assessor import ImpactAssessor
from modules.response_engine import ResponseEngine

# Initialize FastAPI
app = FastAPI(
    title="TradeGuard API",
    description="AI-Powered Supply Chain Disruption Intelligence",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
radar = DisruptionRadar()
assessor = ImpactAssessor()
response_engine = ResponseEngine()

# Load mock shipments
with open('data/mock_shipments.json', 'r') as f:
    mock_data = json.load(f)
    mock_shipments = mock_data['shipments']

@app.get("/")
def read_root():
    return {
        "name": "TradeGuard API",
        "version": "1.0.0",
        "status": "operational",
        "message": "AI-Powered Supply Chain Disruption Intelligence"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/shipments")
def get_all_shipments():
    return mock_shipments

@app.get("/api/alerts")
def get_all_alerts():
    affected = radar.scan_all_corridors(mock_shipments)
    alerts = []
    for item in affected:
        shipment = item['shipment']
        risk_score = item['risk_score']
        risk_level = item['risk_level']
        assessment = assessor.assess_shipment_risk(shipment, risk_score, risk_level)
        alerts.append({
            "shipment_id": shipment['shipment_id'],
            "container_no": shipment['container_no'],
            "risk_level": risk_level,
            "predicted_delay": f"{assessment['predicted_delay_days_min']}-{assessment['predicted_delay_days_max']} days",
            "penalty_exposure": f"₹{assessment['financial_exposure_inr']:,.0f}"
        })
    return alerts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)