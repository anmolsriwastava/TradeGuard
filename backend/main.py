from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
import os

app = FastAPI(title="VyaparAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load shipments
shipments_file = os.path.join(os.path.dirname(__file__), 'data', 'mock_shipments.json')
try:
    with open(shipments_file, 'r') as f:
        mock_data = json.load(f)
        mock_shipments = mock_data.get('shipments', [])
except:
    mock_shipments = [
        {"shipment_id": "SHP-001", "container_no": "INMU456789", "origin_port": "INNSA", 
         "destination_port": "AEJEA", "eta": "2026-04-01", "delivery_deadline": "2026-04-03",
         "cargo_value_inr": 850000, "penalty_per_day_inr": 25000, "lifecycle_stage": "mid_ocean"}
    ]

@app.get("/")
def root():
    return {"name": "VyaparAI API", "status": "running", "time": datetime.now().isoformat()}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/shipments")
def get_shipments():
    return mock_shipments

@app.get("/api/alerts")
def get_alerts():
    alerts = []
    for s in mock_shipments:
        alerts.append({
            "shipment_id": s.get("shipment_id", ""),
            "container_no": s.get("container_no", ""),
            "risk_level": "HIGH",
            "predicted_delay": "4-7 days",
            "penalty_exposure": f"₹{s.get('penalty_per_day_inr', 25000) * 5:,.0f}"
        })
    return alerts[:3]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)