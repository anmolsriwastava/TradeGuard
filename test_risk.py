import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from modules.impact_assessor import ImpactAssessor

# Create instance
assessor = ImpactAssessor()

# Test with sample data
sample_shipment = {
    "shipment_id": "SHP-001",
    "container_no": "INMU456789",
    "origin_port": "INNSA",
    "destination_port": "AEJEA"
}

# Get risk
risk = assessor.assess_shipment_risk(sample_shipment, 74, "HIGH")
print("Risk Assessment:", risk)