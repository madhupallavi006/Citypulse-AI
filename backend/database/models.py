from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RoadModel(BaseModel):
    road_id: str
    name: str
    speed_limit_kmh: float
    length_km: float
    start_lat: float
    start_lng: float
    end_lat: float
    end_lng: float

class IntersectionModel(BaseModel):
    intersection_id: str
    name: str
    lat: float
    lng: float
    signal_status: str = "GREEN"

class TrafficObservationModel(BaseModel):
    timestamp: str
    road_id: str
    intersection_id: str
    vehicle_count: int
    average_speed: float
    road_occupancy: float
    traffic_density: float
    rainfall: float
    weather_condition: str
    accident: int
    construction: int
    road_closure: int
    event: int
    signal_failure: int
    congestion_risk: int
    risk_level: str

class IncidentModel(BaseModel):
    id: str
    road_id: str
    type: str
    severity: str
    status: str
    created_at: str
    description: Optional[str] = None
