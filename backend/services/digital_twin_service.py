from backend.services.traffic_service import get_latest_telemetry
from backend.ml.predict import predict_telemetry_risk

def run_what_if_simulation(
    rain_severity: float = 0.0,
    demand_multiplier: float = 1.0,
    closed_roads: list = None,
    signal_override_sec: int = 0,
    transit_surge_factor: float = 1.0
):
    if closed_roads is None:
        closed_roads = []
        
    baseline_telemetry = get_latest_telemetry()
    baseline_preds = predict_telemetry_risk(baseline_telemetry)
    
    baseline_speeds = [r["average_speed"] for r in baseline_telemetry]
    baseline_avg_speed = round(sum(baseline_speeds) / max(1, len(baseline_speeds)), 1)
    
    baseline_risks = [p["predicted_risk_score"] for p in baseline_preds]
    baseline_avg_risk = round(sum(baseline_risks) / max(1, len(baseline_risks)), 1)
    
    # Calculate simulated perturbation factors
    simulated_roads = []
    simulated_bottlenecks = []
    
    for r in baseline_telemetry:
        road_id = r["road_id"]
        speed = r["average_speed"]
        density = r["traffic_density"]
        occupancy = r["road_occupancy"]
        
        # Apply Rain Impact (-15% speed at 100% rain)
        rain_speed_penalty = (rain_severity / 100.0) * 0.25 * speed
        
        # Apply Demand Multiplier (+density, -speed)
        demand_speed_penalty = (demand_multiplier - 1.0) * 0.35 * speed
        
        # Apply Signal Override (+speed if positive optimization, -speed if delayed)
        signal_effect = (signal_override_sec / 30.0) * 0.10 * speed
        
        # Calculate new simulated speed & density
        sim_speed = max(5.0, round(speed - rain_speed_penalty - demand_speed_penalty + signal_effect, 1))
        sim_density = min(100.0, round(density * demand_multiplier * (1.0 + (rain_severity / 200.0)), 1))
        
        if road_id in closed_roads:
            sim_speed = 0.0
            sim_density = 100.0
            
        sim_risk = min(100, round(100.0 - (sim_speed / 70.0 * 100.0) + (sim_density * 0.3), 1))
        
        simulated_roads.append({
            "road_id": road_id,
            "simulated_speed": sim_speed,
            "simulated_density": sim_density,
            "simulated_risk": sim_risk
        })
        
        if sim_risk > 65 or sim_speed < 20.0:
            simulated_bottlenecks.append({
                "road_id": road_id,
                "simulated_speed": sim_speed,
                "risk_score": sim_risk,
                "cause": "Road Closure" if road_id in closed_roads else ("Heavy Rain & Traffic Surge" if rain_severity > 50 else "Demand Spike")
            })

    sim_speeds = [r["simulated_speed"] for r in simulated_roads if r["simulated_speed"] > 0]
    sim_avg_speed = round(sum(sim_speeds) / max(1, len(sim_speeds)), 1) if sim_speeds else 0.0
    
    sim_risks = [r["simulated_risk"] for r in simulated_roads]
    sim_avg_risk = round(sum(sim_risks) / max(1, len(sim_risks)), 1)
    
    # Calculate System Impact Score (0-100)
    speed_delta = max(0, baseline_avg_speed - sim_avg_speed)
    impact_score = min(100, round((speed_delta / max(1, baseline_avg_speed)) * 100 + (len(simulated_bottlenecks) * 3), 1))
    
    # Generate AI Recommended Countermeasures
    countermeasures = []
    if rain_severity > 40:
        countermeasures.append("Enable Wet Weather Advisory mode & extend main arterial green phases by +10s.")
    if demand_multiplier > 1.3:
        countermeasures.append("Deploy public transit surge buses to reduce private vehicle density along CBD corridors.")
    if closed_roads:
        countermeasures.append(f"Reroute incoming traffic away from closed corridor(s) ({', '.join(closed_roads)}) via Outer Ring Road.")
    if not countermeasures:
        countermeasures.append("Current network flow is optimal. Maintain standard adaptive signal timing.")

    return {
        "baseline": {
            "avg_city_speed_kmh": baseline_avg_speed,
            "congestion_index": baseline_avg_risk,
            "active_bottlenecks_count": sum(1 for r in baseline_risks if r > 60)
        },
        "scenario": {
            "parameters": {
                "rain_severity": rain_severity,
                "demand_multiplier": demand_multiplier,
                "closed_roads": closed_roads,
                "signal_override_sec": signal_override_sec,
                "transit_surge_factor": transit_surge_factor
            },
            "avg_city_speed_kmh": sim_avg_speed,
            "congestion_index": sim_avg_risk,
            "bottlenecks": simulated_bottlenecks,
            "system_impact_score": impact_score,
            "ai_recommended_countermeasures": countermeasures
        }
    }
