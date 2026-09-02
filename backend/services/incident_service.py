from datetime import datetime
from backend.database.database import get_db_connection, init_db
from backend.simulation.traffic_simulator import simulator_engine
from backend.ml.anomaly_detector import anomaly_detector_engine
from backend.services.traffic_service import get_latest_telemetry

def fetch_all_incidents():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    incidents = []
    for r in rows:
        incidents.append({
            "id": r["id"],
            "road_id": r["road_id"],
            "type": r["type"],
            "severity": r["severity"],
            "status": r["status"],
            "reported_time": r["created_at"],
            "description": r["description"] or f"Simulated {r['type']} incident on corridor {r['road_id']}"
        })
        
    # Seed default active incidents if empty
    if not incidents:
        incidents = [
            {
                "id": "INC-101",
                "road_id": "NH16-01",
                "type": "Vehicle Breakdown",
                "severity": "HIGH",
                "status": "ACTIVE",
                "reported_time": "18:30",
                "estimated_clearance_mins": 25,
                "description": "Commercial truck breakdown restricting right lane."
            },
            {
                "id": "INC-102",
                "road_id": "ORR-03",
                "type": "Rainwater Logging",
                "severity": "CRITICAL",
                "status": "ACTIVE",
                "reported_time": "18:40",
                "estimated_clearance_mins": 45,
                "description": "Localized water logging causing speed reduction."
            }
        ]
    return incidents

def create_simulated_incident(road_id: str, incident_type: str, severity: str, duration_mins: int = 30):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    inc_id = f"INC-{int(datetime.now().timestamp()) % 10000}"
    created_at = datetime.now().strftime("%H:%M")
    
    cursor.execute("""
    INSERT INTO incidents (id, road_id, type, severity, status, created_at, description)
    VALUES (?, ?, ?, ?, 'ACTIVE', ?, ?)
    """, (inc_id, road_id, incident_type, severity, created_at, f"Simulated {incident_type} ({severity})"))
    conn.commit()
    conn.close()
    
    # Inject override into simulation engine
    simulator_engine.add_incident_override(road_id, incident_type, severity)
    
    return {
        "incident_id": inc_id,
        "road_id": road_id,
        "type": incident_type,
        "severity": severity,
        "status": "ACTIVE",
        "reported_time": created_at,
        "duration_mins": duration_mins
    }

def fetch_detected_anomalies():
    telemetry = get_latest_telemetry()
    anomalies = anomaly_detector_engine.detect_anomalies(telemetry)
    return anomalies
