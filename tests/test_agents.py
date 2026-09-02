from backend.agents.multi_agent_system import (
    TrafficMonitorAgent,
    CongestionPredictorAgent,
    RouteOptimizerAgent,
    IncidentResponseAgent,
    SignalOrchestratorAgent,
    multi_agent_engine
)
from backend.services.agent_service import get_agent_system_status, execute_multi_agent_orchestration

def test_individual_agents():
    monitor = TrafficMonitorAgent()
    res1 = monitor.execute([])
    assert res1["status"] == "COMPLETED"

    predictor = CongestionPredictorAgent()
    res2 = predictor.execute([])
    assert res2["status"] == "COMPLETED"

    optimizer = RouteOptimizerAgent()
    res3 = optimizer.execute("NH16-03")
    assert res3["status"] == "COMPLETED"

    response_agent = IncidentResponseAgent()
    res4 = response_agent.execute("Monsoon rain drop")
    assert res4["status"] == "COMPLETED"

    orchestrator = SignalOrchestratorAgent()
    res5 = orchestrator.execute(res1["findings"], res2["findings"])
    assert res5["status"] == "COMPLETED"

def test_multi_agent_collaboration_engine():
    plan = multi_agent_engine.run_collaboration_pipeline()
    assert plan["collaboration_status"] == "SUCCESSFUL"
    assert len(plan["workflow_sequence"]) == 5
    assert "agent_results" in plan
    assert "unified_orchestration_summary" in plan

def test_agent_service_and_status():
    status = get_agent_system_status()
    assert len(status) == 5
    orchestration = execute_multi_agent_orchestration()
    assert orchestration["collaboration_status"] == "SUCCESSFUL"
