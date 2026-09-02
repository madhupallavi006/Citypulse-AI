from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from backend.simulation.traffic_simulator import simulator_engine
from backend.services.digital_twin_service import run_what_if_simulation

router = APIRouter(prefix="/api/simulation", tags=["Digital Twin & Simulation Controls"])

class OverrideRequest(BaseModel):
    rain_mode: Optional[bool] = None
    traffic_multiplier: Optional[float] = None
    road_id: Optional[str] = None
    incident_type: Optional[str] = None
    severity: Optional[str] = None

class WhatIfRequest(BaseModel):
    rain_severity: float = 0.0
    demand_multiplier: float = 1.0
    closed_roads: List[str] = []
    signal_override_sec: int = 0
    transit_surge_factor: float = 1.0

@router.get("/state")
def get_simulation_state():
    return {
        "status": "success",
        "rain_mode": simulator_engine.rain_mode,
        "traffic_multiplier": simulator_engine.traffic_multiplier,
        "active_overrides": simulator_engine.incident_overrides
    }

@router.post("/override")
def apply_override(req: OverrideRequest):
    if req.rain_mode is not None:
        simulator_engine.set_rain_mode(req.rain_mode)
    if req.traffic_multiplier is not None:
        simulator_engine.set_traffic_multiplier(req.traffic_multiplier)
    if req.road_id and req.incident_type and req.severity:
        simulator_engine.add_incident_override(req.road_id, req.incident_type, req.severity)
        
    return {
        "status": "success",
        "message": "Simulation override state updated successfully",
        "rain_mode": simulator_engine.rain_mode,
        "traffic_multiplier": simulator_engine.traffic_multiplier
    }

@router.post("/what-if")
def run_what_if_scenario(req: WhatIfRequest):
    res = run_what_if_simulation(
        rain_severity=req.rain_severity,
        demand_multiplier=req.demand_multiplier,
        closed_roads=req.closed_roads,
        signal_override_sec=req.signal_override_sec,
        transit_surge_factor=req.transit_surge_factor
    )
    return {
        "status": "success",
        "digital_twin_scenario": res
    }
