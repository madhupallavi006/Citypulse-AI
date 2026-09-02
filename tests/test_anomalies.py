from backend.ml.anomaly_detector import anomaly_detector_engine
from backend.services.incident_service import create_simulated_incident, fetch_detected_anomalies, fetch_all_incidents

def test_anomaly_detection_engine():
    telemetry = [
        {
            "road_id": "NH16-01",
            "intersection_id": "J01",
            "average_speed": 12.0,
            "traffic_density": 92.0,
            "road_occupancy": 88.0,
            "vehicle_count": 1800,
            "accident": 1,
            "road_closure": 0
        },
        {
            "road_id": "NH16-02",
            "intersection_id": "J02",
            "average_speed": 55.0,
            "traffic_density": 35.0,
            "road_occupancy": 30.0,
            "vehicle_count": 600,
            "accident": 0,
            "road_closure": 0
        }
    ]
    
    anomalies = anomaly_detector_engine.detect_anomalies(telemetry)
    assert len(anomalies) > 0
    ano = anomalies[0]
    assert ano["road_id"] == "NH16-01"
    assert ano["severity"] == "CRITICAL"

def test_create_simulated_incident():
    res = create_simulated_incident("CBD-02", "Road Construction", "HIGH", 45)
    assert res["road_id"] == "CBD-02"
    assert res["type"] == "Road Construction"
    assert res["status"] == "ACTIVE"

def test_fetch_all_incidents():
    incidents = fetch_all_incidents()
    assert len(incidents) > 0
