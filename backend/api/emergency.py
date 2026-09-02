from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.services.emergency_service import (
    get_active_emergency_corridor,
    create_emergency_green_corridor
)
from backend.services.transit_service import fetch_bus_transit_priorities

router = APIRouter(prefix="/api/emergency", tags=["Emergency Corridor & Public Transit"])

class EmergencySimulateRequest(BaseModel):
    vehicle_type: str = "Ambulance"
    origin: str = "J01"
    destination: str = "J08"

@router.get("")
def get_emergency_status():
    corridor = get_active_emergency_corridor()
    return {
        "status": "success",
        "active_corridor": corridor
    }

@router.post("")
def simulate_emergency(req: EmergencySimulateRequest):
    corridor = create_emergency_green_corridor(
        vehicle_type=req.vehicle_type,
        origin_node=req.origin,
        destination_node=req.destination
    )
    return {
        "status": "success",
        "message": f"Simulated Emergency Green Corridor generated for {req.vehicle_type}",
        "corridor_details": corridor
    }

@router.get("/transit")
def get_bus_transit_priorities():
    priorities = fetch_bus_transit_priorities()
    return {
        "status": "success",
        "bus_priorities": priorities
    }
