from backend.agents.multi_agent_system import multi_agent_engine

def execute_multi_agent_orchestration():
    return multi_agent_engine.run_collaboration_pipeline()

def get_agent_system_status():
    return [
        {"name": "Traffic Monitor Agent", "status": "ONLINE", "role": "Telemetry Audit & Anomaly Detection"},
        {"name": "Congestion Predictor Agent", "status": "ONLINE", "role": "15-30 Min ML Forecast Engine"},
        {"name": "Route Optimizer Agent", "status": "ONLINE", "role": "NetworkX Graph Congestion Rerouting"},
        {"name": "Incident Response Agent", "status": "ONLINE", "role": "RAG SOP Protocol Matcher & Emergency Pre-emption"},
        {"name": "Signal Orchestrator Agent", "status": "ONLINE", "role": "Adaptive Signal Timing & Phase Pre-emption"}
    ]
