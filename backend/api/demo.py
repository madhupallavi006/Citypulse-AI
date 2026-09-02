from fastapi import APIRouter
from backend.services.demo_service import trigger_demo_scenario

router = APIRouter(prefix="/api/demo", tags=["One-Click Demo Scenarios"])

@router.post("/trigger/{scenario_id}")
def trigger_scenario(scenario_id: str):
    res = trigger_demo_scenario(scenario_id)
    return {
        "status": "success",
        "demo_scenario": res
    }
