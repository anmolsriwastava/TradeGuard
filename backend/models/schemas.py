from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List, Dict, Any

class Shipment(BaseModel):
    shipment_id: str
    container_no: str
    vessel_name: str
    origin_port: str
    destination_port: str
    eta: date
    delivery_deadline: date
    cargo_value_inr: float
    penalty_per_day_inr: float
    lifecycle_stage: str  # pre_booking, booked, mid_ocean, destination
    buyer_contact: str
    priority: str  # cost, speed, green

class CorridorRisk(BaseModel):
    corridor_id: str
    timestamp: datetime
    risk_score: int
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    components: Dict[str, int]

class RiskAssessmentResponse(BaseModel):
    shipment_id: str
    corridor_id: str
    risk_score: int
    risk_level: str
    predicted_delay_days_min: int
    predicted_delay_days_max: int
    delay_probability: float
    financial_exposure_inr: float
    deadline_breach_risk: str  # LOW, MEDIUM, HIGH

class ResponseOption(BaseModel):
    option_id: int
    title: str
    description: str
    extra_cost_inr: Optional[float] = 0
    extra_days: int
    co2_impact_percent: Optional[int] = 0
    recommended: bool

class LifecycleResponse(BaseModel):
    shipment_id: str
    lifecycle_stage: str
    disruption_alert: str
    response_options: List[ResponseOption]

class AlertOutput(BaseModel):
    shipment_id: str
    container_no: str
    message: str
    risk_level: str
    predicted_delay: str
    penalty_exposure: str
    response_options_count: int