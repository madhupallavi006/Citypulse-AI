from fastapi import APIRouter
from backend.services.agent_service import get_agent_system_status, execute_multi_agent_orchestration

router = APIRouter(prefix="/api/agents", tags=["Multi-Agent AI System"])

@router.get("/status")
def get_agents_status():
    agents = get_agent_system_status()
    return {
        "status": "success",
        "agent_count": len(agents),
        "agents": agents
    }

@router.post("/orchestrate")
def run_orchestration():
    orchestration_plan = execute_multi_agent_orchestration()
    return {
        "status": "success",
        "orchestration_plan": orchestration_plan
    }
