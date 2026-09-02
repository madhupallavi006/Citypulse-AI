from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])

class IncidentCreate(BaseModel):
    type: str
    road_id: str
    severity: str
    duration_mins: int
    description: Optional[str] = None

@router.get("")
def get_incidents():
    return {
        "status": "success",
        "incidents": [
            {
                "id": "INC-101",
                "type": "Vehicle Breakdown",
                "road_id": "NH16-01",
                "severity": "HIGH",
                "status": "ACTIVE",
                "reported_time": "18:30",
                "estimated_clearance_mins": 25
            },
            {
                "id": "INC-102",
                "type": "Rainwater Logging",
                "road_id": "ORR-03",
                "severity": "CRITICAL",
                "status": "ACTIVE",
                "reported_time": "18:40",
                "estimated_clearance_mins": 45
            }
        ]
    }

@router.post("")
def create_incident(incident: IncidentCreate):
    return {
        "status": "success",
        "message": f"Incident '{incident.type}' created for road {incident.road_id}",
        "incident_id": "INC-103",
        "data": incident.model_dump()
    }
