from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/traffic", tags=["Traffic"])

class OverviewMetrics(BaseModel):
    total_monitored_roads: int
    active_vehicles: int
    high_risk_roads: int
    critical_roads: int
    active_incidents: int
    average_speed_kmh: float
    predicted_congestion_rate: float
    emergency_vehicles_active: int

@router.get("/overview", response_model=OverviewMetrics)
def get_traffic_overview():
    return OverviewMetrics(
        total_monitored_roads=42,
        active_vehicles=18450,
        high_risk_roads=5,
        critical_roads=2,
        active_incidents=3,
        average_speed_kmh=34.2,
        predicted_congestion_rate=14.5,
        emergency_vehicles_active=1
    )

@router.get("/live")
def get_live_traffic():
    return {
        "status": "success",
        "simulated": True,
        "roads": [
            {
                "road_id": "NH16-01",
                "name": "NH16 Expressway Corridor North",
                "current_speed": 28.5,
                "vehicle_count": 1450,
                "traffic_density": 82.4,
                "occupancy": 76.1,
                "congestion_risk": 87,
                "risk_level": "CRITICAL",
                "prediction": "High congestion expected in 20 mins"
            },
            {
                "road_id": "NH16-02",
                "name": "NH16 Expressway Central Link",
                "current_speed": 45.0,
                "vehicle_count": 820,
                "traffic_density": 45.0,
                "occupancy": 42.0,
                "congestion_risk": 35,
                "risk_level": "MEDIUM",
                "prediction": "Stable traffic flow expected"
            },
            {
                "road_id": "ORR-03",
                "name": "Outer Ring Road Junction South",
                "current_speed": 18.2,
                "vehicle_count": 1680,
                "traffic_density": 91.0,
                "occupancy": 88.5,
                "congestion_risk": 92,
                "risk_level": "CRITICAL",
                "prediction": "Severe bottleneck predicted in 15 mins"
            }
        ]
    }

@router.get("/predictions")
def get_traffic_predictions():
    return {
        "status": "success",
        "predictions": [
            {
                "road_id": "NH16-01",
                "current_status": "Heavy Traffic",
                "predicted_risk": 87,
                "prediction_horizon_mins": 20,
                "confidence": 0.89,
                "main_cause": "High vehicle count + Rainwater logging",
                "recommended_action": "Reroute heavy vehicles to ORR-02"
            },
            {
                "road_id": "ORR-03",
                "current_status": "Congested",
                "predicted_risk": 92,
                "prediction_horizon_mins": 15,
                "confidence": 0.94,
                "main_cause": "Signal malfunction at Sector 4 Flyover",
                "recommended_action": "Simulate Emergency Signal Override"
            }
        ]
    }

@router.get("/risk/{road_id}")
def get_road_risk(road_id: str):
    return {
        "road_id": road_id,
        "current_speed": 28.5,
        "vehicle_count": 1450,
        "congestion_risk": 87,
        "risk_level": "CRITICAL",
        "factors": [
            {"factor": "Traffic Density", "contribution": 32},
            {"factor": "Average Speed Drop", "contribution": 24},
            {"factor": "Rainfall Impact", "contribution": 18},
            {"factor": "Peak Hour Factor", "contribution": 13}
        ]
    }
