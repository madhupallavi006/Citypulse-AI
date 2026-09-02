from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/emergency", tags=["Emergency Corridor"])

class EmergencySimulateRequest(BaseModel):
    vehicle_type: str = "Ambulance"
    origin: str
    destination: str

@router.get("")
def get_emergency_status():
    return {
        "status": "success",
        "active_corridor": {
            "vehicle_id": "AMB-911",
            "type": "Ambulance",
            "origin": "Apollo General Hospital",
            "destination": "City Trauma Center",
            "recommended_route": "Sector 3 Flyover -> Express Corridor -> Trauma Gate",
            "intersections_cleared": 4,
            "total_intersections": 6,
            "estimated_eta_mins": 8,
            "time_saved_mins": 12,
            "signal_priority_active": True
        }
    }

@router.post("")
def simulate_emergency(req: EmergencySimulateRequest):
    return {
        "status": "success",
        "message": f"Simulated Emergency Corridor created for {req.vehicle_type}",
        "corridor_details": {
            "vehicle_type": req.vehicle_type,
            "origin": req.origin,
            "destination": req.destination,
            "route": f"{req.origin} -> Outer Ring Link -> {req.destination}",
            "estimated_eta_mins": 9,
            "time_saved_mins": 11,
            "simulated": True
        }
    }
