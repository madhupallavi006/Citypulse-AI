from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/routes", tags=["Routes"])

class RouteRequest(BaseModel):
    origin: str
    destination: str
    consider_predictions: bool = True

@router.get("")
def get_routes():
    return {
        "status": "success",
        "routes": [
            {
                "route_id": "R1-DEFAULT",
                "name": "Direct Highway Corridor",
                "risk_score": 87,
                "risk_level": "HIGH",
                "eta_mins": 32,
                "distance_km": 14.2
            },
            {
                "route_id": "R2-OPTIMIZED",
                "name": "CityPulse Optimized Bypass",
                "risk_score": 24,
                "risk_level": "LOW",
                "eta_mins": 24,
                "distance_km": 15.8,
                "time_saved_mins": 8
            }
        ]
    }

@router.post("")
def optimize_route(req: RouteRequest):
    return {
        "status": "success",
        "origin": req.origin,
        "destination": req.destination,
        "normal_route": {"name": "Standard Route", "eta_mins": 35, "risk": "HIGH"},
        "recommended_route": {"name": "CityPulse Dynamic Route", "eta_mins": 25, "risk": "LOW", "time_saved_mins": 10}
    }
