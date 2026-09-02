from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/digital-twin", tags=["Digital Twin & Simulation"])

class ScenarioRequest(BaseModel):
    scenario_name: str # Traffic Increase, Heavy Rain, Accident, Road Closure, Public Event
    severity: str = "HIGH"

@router.get("")
def get_digital_twin_state():
    return {
        "status": "success",
        "digital_twin": {
            "monitored_nodes": 18,
            "monitored_edges": 42,
            "simulation_speed": "1x",
            "active_scenarios": ["Peak Hour Traffic"],
            "network_health_score": 78
        }
    }

@router.post("/simulate")
def trigger_simulation(req: ScenarioRequest):
    return {
        "status": "success",
        "message": f"Scenario '{req.scenario_name}' applied to Digital Twin",
        "impact": {
            "congestion_score_increase": "+25%",
            "affected_roads": ["NH16-01", "ORR-03"],
            "recommended_interventions": ["Reroute line 102 buses", "Extend green light phase at node J4"]
        }
    }
