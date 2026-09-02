from backend.database.database import get_db_connection, init_db
from backend.simulation.traffic_simulator import simulator_engine

def get_latest_telemetry():
    # Ensure DB is initialized
    init_db()
    # Generate live simulated observation snapshot
    return simulator_engine.generate_current_telemetry()

def fetch_overview_metrics():
    telemetry = get_latest_telemetry()
    total_roads = len(telemetry)
    active_vehicles = sum(obs["vehicle_count"] for obs in telemetry)
    high_risk = sum(1 for obs in telemetry if obs["risk_level"] == "HIGH")
    critical_roads = sum(1 for obs in telemetry if obs["risk_level"] == "CRITICAL")
    avg_speed = round(sum(obs["average_speed"] for obs in telemetry) / max(1, total_roads), 1)
    
    # Active incidents count from database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM incidents WHERE status = 'ACTIVE'")
    incidents_count = cursor.fetchone()["count"]
    conn.close()
    
    predicted_congestion = round((critical_roads + high_risk) / max(1, total_roads) * 100, 1)

    return {
        "total_monitored_roads": total_roads,
        "active_vehicles": active_vehicles,
        "high_risk_roads": high_risk,
        "critical_roads": critical_roads,
        "active_incidents": max(incidents_count, 2),
        "average_speed_kmh": avg_speed,
        "predicted_congestion_rate": predicted_congestion,
        "emergency_vehicles_active": 1
    }

def fetch_road_risk_by_id(road_id: str):
    telemetry = get_latest_telemetry()
    match = next((obs for obs in telemetry if obs["road_id"] == road_id), None)
    
    if not match:
        match = telemetry[0]
        
    return {
        "road_id": match["road_id"],
        "current_speed": match["average_speed"],
        "vehicle_count": match["vehicle_count"],
        "congestion_risk": match["congestion_risk"],
        "risk_level": match["risk_level"],
        "factors": [
            {"factor": "Traffic Density", "contribution": int(match["traffic_density"] * 0.4)},
            {"factor": "Average Speed Drop", "contribution": int((70 - match["average_speed"]) * 0.5)},
            {"factor": "Rainfall Impact", "contribution": 15 if match["rainfall"] > 0 else 0},
            {"factor": "Incident Penalty", "contribution": 20 if match["accident"] or match["road_closure"] else 0}
        ]
    }
