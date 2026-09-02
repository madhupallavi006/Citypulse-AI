from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from backend.services.incident_service import (
    fetch_all_incidents,
    create_simulated_incident,
    fetch_detected_anomalies
)

router = APIRouter(prefix="/api/incidents", tags=["Incidents & Anomalies"])

class IncidentCreate(BaseModel):
    type: str
    road_id: str
    severity: str
    duration_mins: int = 30
    description: Optional[str] = None

@router.get("")
def get_incidents():
    incidents = fetch_all_incidents()
    return {
        "status": "success",
        "incidents": incidents
    }

@router.post("")
def create_incident(incident: IncidentCreate):
    res = create_simulated_incident(
        road_id=incident.road_id,
        incident_type=incident.type,
        severity=incident.severity,
        duration_mins=incident.duration_mins
    )
    return {
        "status": "success",
        "message": f"Incident '{incident.type}' created for road {incident.road_id}",
        "incident": res
    }

@router.get("/anomalies")
def get_anomalies():
    anomalies = fetch_detected_anomalies()
    return {
        "status": "success",
        "anomalies_count": len(anomalies),
        "anomalies": anomalies
    }
