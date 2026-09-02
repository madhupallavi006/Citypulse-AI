from backend.simulation.traffic_simulator import simulator_engine
from backend.services.emergency_service import create_emergency_green_corridor
from backend.services.digital_twin_service import run_what_if_simulation
from backend.services.route_service import get_optimized_route

def trigger_demo_scenario(scenario_id: str):
    if scenario_id == "morning_peak":
        simulator_engine.set_rain_mode(False)
        simulator_engine.set_traffic_multiplier(1.8)
        simulator_engine.add_incident_override("CBD-01", "Heavy Peak Commute", "HIGH")
        simulator_engine.add_incident_override("NH16-01", "Expressway Surge", "HIGH")
        
        return {
            "scenario_id": "morning_peak",
            "name": "Morning Peak Congestion Mode",
            "status": "ACTIVATED",
            "description": "Simulating 8:30 AM citywide commute surge. Traffic volume multiplied by 1.8x across CBD & Expressway corridors.",
            "metrics": {
                "traffic_multiplier": 1.8,
                "rain_mode": False,
                "flagged_corridors": ["CBD-01", "NH16-01"]
            }
        }
        
    elif scenario_id == "monsoon_disaster":
        simulator_engine.set_rain_mode(True)
        simulator_engine.set_traffic_multiplier(1.4)
        simulator_engine.add_incident_override("ORR-03", "Rainwater Logging", "CRITICAL")
        simulator_engine.add_incident_override("CBD-02", "Low Visibility Bottleneck", "HIGH")
        
        what_if_res = run_what_if_simulation(
            rain_severity=85.0,
            demand_multiplier=1.4,
            closed_roads=["ORR-03"],
            signal_override_sec=15
        )
        
        return {
            "scenario_id": "monsoon_disaster",
            "name": "Monsoon Disaster Heavy Rain Mode",
            "status": "ACTIVATED",
            "description": "Simulating 85% rain intensity with severe surface water logging on ORR-03. Expressway speed limits throttled by 35%.",
            "metrics": {
                "rain_severity": 85.0,
                "traffic_multiplier": 1.4,
                "closed_roads": ["ORR-03"],
                "digital_twin_impact_score": what_if_res["scenario"]["system_impact_score"]
            }
        }
        
    elif scenario_id == "emergency_ambulance":
        simulator_engine.set_rain_mode(False)
        simulator_engine.set_traffic_multiplier(1.2)
        corridor = create_emergency_green_corridor("Ambulance", "J01", "J08")
        
        return {
            "scenario_id": "emergency_ambulance",
            "name": "Emergency Ambulance Green Corridor Mode",
            "status": "ACTIVATED",
            "description": "Rapid trauma ambulance dispatched from Vani Vihar (J01) to KIIT Campus (J08). Automated green wave pre-emption active across 7 intersections.",
            "metrics": {
                "vehicle_id": corridor["vehicle_id"],
                "intersections_preempted": len(corridor["intersections"]),
                "estimated_eta_mins": corridor["estimated_eta_mins"],
                "time_saved_mins": corridor["time_saved_mins"]
            }
        }
        
    elif scenario_id == "stadium_event":
        simulator_engine.set_rain_mode(False)
        simulator_engine.set_traffic_multiplier(2.5)
        simulator_engine.add_incident_override("NH16-03", "Kalinga Stadium Event Surge", "CRITICAL")
        
        route = get_optimized_route("J01", "J08")
        
        return {
            "scenario_id": "stadium_event",
            "name": "Stadium Event Traffic Surge Mode",
            "status": "ACTIVATED",
            "description": "2.5x traffic surge around Kalinga Stadium Junction (J17). NetworkX predicted-congestion routing dynamically diverting traffic via Outer Ring Road.",
            "metrics": {
                "traffic_multiplier": 2.5,
                "event_location": "Kalinga Stadium (J17)",
                "recommended_bypass": route["recommended_route"]["corridors"] if "recommended_route" in route else [],
                "time_saved_mins": route["recommended_route"]["time_saved_mins"] if "recommended_route" in route else 8.5
            }
        }
        
    else:
        return {
            "scenario_id": "unknown",
            "status": "FAILED",
            "message": f"Unknown scenario_id '{scenario_id}'"
        }
