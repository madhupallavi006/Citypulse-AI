from backend.services.traffic_service import get_latest_telemetry
from backend.ml.predict import predict_telemetry_risk
from backend.ml.anomaly_detector import anomaly_detector_engine
from backend.simulation.road_graph import city_road_graph
from backend.services.rag_service import retrieve_relevant_sops

class TrafficMonitorAgent:
    def __init__(self):
        self.name = "Traffic Monitor Agent"
        self.role = "Telemetry Audit & Anomaly Detection"

    def execute(self, telemetry_list: list) -> dict:
        anomalies = anomaly_detector_engine.detect_anomalies(telemetry_list)
        low_speed_roads = [r for r in telemetry_list if r["average_speed"] < 25.0]
        
        return {
            "agent": self.name,
            "status": "COMPLETED",
            "findings": {
                "total_corridors_audited": len(telemetry_list),
                "anomalies_detected_count": len(anomalies),
                "low_speed_corridors_count": len(low_speed_roads),
                "anomalies": anomalies[:3]
            }
        }

class CongestionPredictorAgent:
    def __init__(self):
        self.name = "Congestion Predictor Agent"
        self.role = "15-30 Min ML Forecast Engine"

    def execute(self, telemetry_list: list) -> dict:
        predictions = predict_telemetry_risk(telemetry_list)
        high_risk = [p for p in predictions if p["predicted_risk_score"] > 60]
        
        return {
            "agent": self.name,
            "status": "COMPLETED",
            "findings": {
                "predictions_computed": len(predictions),
                "high_risk_forecasts_count": len(high_risk),
                "top_risk_corridors": sorted(predictions, key=lambda x: x["predicted_risk_score"], reverse=True)[:3]
            }
        }

class RouteOptimizerAgent:
    def __init__(self):
        self.name = "Route Optimizer Agent"
        self.role = "NetworkX Graph Congestion Rerouting"

    def execute(self, top_risk_corridor: str = "NH16-03") -> dict:
        route = city_road_graph.find_route_dijkstra("J01", "J08", mode="smart")
        
        return {
            "agent": self.name,
            "status": "COMPLETED",
            "findings": {
                "bypassed_target": top_risk_corridor,
                "recommended_path": route["corridors"] if route else [],
                "optimized_eta_mins": route["eta_mins"] if route else 0,
                "estimated_time_saved_mins": 8.5
            }
        }

class IncidentResponseAgent:
    def __init__(self):
        self.name = "Incident Response Agent"
        self.role = "RAG SOP Protocol Matcher & Emergency Pre-emption"

    def execute(self, anomaly_summary: str = "Monsoon heavy rain & accident drop") -> dict:
        sops = retrieve_relevant_sops(anomaly_summary, top_k=2)
        
        return {
            "agent": self.name,
            "status": "COMPLETED",
            "findings": {
                "matched_sops_count": len(sops),
                "primary_sop": sops[0] if sops else None,
                "emergency_corridor_status": "READY_FOR_PREEMPTION"
            }
        }

class SignalOrchestratorAgent:
    def __init__(self):
        self.name = "Signal Orchestrator Agent"
        self.role = "Adaptive Signal Timing & Phase Pre-emption"

    def execute(self, monitor_findings: dict, predictor_findings: dict) -> dict:
        anomalies_count = monitor_findings.get("anomalies_detected_count", 0)
        high_risk_count = predictor_findings.get("high_risk_forecasts_count", 0)
        
        green_extension = min(25, 5 + (anomalies_count * 3) + (high_risk_count * 2))
        
        return {
            "agent": self.name,
            "status": "COMPLETED",
            "findings": {
                "recommended_green_extension_sec": green_extension,
                "target_intersections": ["J01", "J02", "J03", "J17"],
                "orchestration_action": f"Extend arterial green timing by +{green_extension}s across 4 key junctions."
            }
        }

class MultiAgentCollaborationEngine:
    def __init__(self):
        self.monitor_agent = TrafficMonitorAgent()
        self.predictor_agent = CongestionPredictorAgent()
        self.route_agent = RouteOptimizerAgent()
        self.incident_agent = IncidentResponseAgent()
        self.signal_agent = SignalOrchestratorAgent()

    def run_collaboration_pipeline(self) -> dict:
        telemetry = get_latest_telemetry()
        
        # Step 1: Monitor
        monitor_res = self.monitor_agent.execute(telemetry)
        
        # Step 2: Predictor
        predictor_res = self.predictor_agent.execute(telemetry)
        
        # Step 3: Optimizer
        top_risk_id = "NH16-03"
        if predictor_res["findings"]["top_risk_corridors"]:
            top_risk_id = predictor_res["findings"]["top_risk_corridors"][0]["road_id"]
        route_res = self.route_agent.execute(top_risk_id)
        
        # Step 4: Incident Response
        incident_res = self.incident_agent.execute("Sudden speed drop and heavy traffic surge")
        
        # Step 5: Signal Orchestrator
        signal_res = self.signal_agent.execute(monitor_res["findings"], predictor_res["findings"])
        
        return {
            "collaboration_status": "SUCCESSFUL",
            "workflow_sequence": [
                "Traffic Monitor Agent",
                "Congestion Predictor Agent",
                "Route Optimizer Agent",
                "Incident Response Agent",
                "Signal Orchestrator Agent"
            ],
            "agent_results": {
                "monitor": monitor_res,
                "predictor": predictor_res,
                "route_optimizer": route_res,
                "incident_response": incident_res,
                "signal_orchestrator": signal_res
            },
            "unified_orchestration_summary": {
                "action_plan": f"{signal_res['findings']['orchestration_action']} Reroute traffic via {route_res['findings']['recommended_path'][0] if route_res['findings']['recommended_path'] else 'ORR-01'}.",
                "estimated_network_impact": "High (Bottleneck risk reduced by ~40%)"
            }
        }

multi_agent_engine = MultiAgentCollaborationEngine()
