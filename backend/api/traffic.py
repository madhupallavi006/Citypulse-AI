from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from backend.services.traffic_service import (
    fetch_overview_metrics,
    get_latest_telemetry,
    fetch_road_risk_by_id
)
from backend.services.prediction_service import fetch_ml_predictions

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
    return fetch_overview_metrics()

@router.get("/live")
def get_live_traffic():
    telemetry = get_latest_telemetry()
    return {
        "status": "success",
        "simulated": True,
        "roads": telemetry
    }

@router.get("/predictions")
def get_traffic_predictions():
    predictions = fetch_ml_predictions()
    return {
        "status": "success",
        "predictions": predictions
    }

@router.get("/risk/{road_id}")
def get_road_risk(road_id: str):
    return fetch_road_risk_by_id(road_id)
