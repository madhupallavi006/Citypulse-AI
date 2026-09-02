from backend.simulation.traffic_simulator import simulator_engine
from backend.services.traffic_service import fetch_overview_metrics

def test_traffic_simulator_telemetry():
    telemetry = simulator_engine.generate_current_telemetry()
    assert len(telemetry) >= 42
    
    sample_obs = telemetry[0]
    assert "road_id" in sample_obs
    assert "average_speed" in sample_obs
    assert "congestion_risk" in sample_obs
    assert 0 <= sample_obs["congestion_risk"] <= 100
    assert sample_obs["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

def test_simulator_rain_mode():
    simulator_engine.set_rain_mode(True)
    telemetry = simulator_engine.generate_current_telemetry()
    rainy_obs = [obs for obs in telemetry if obs["rainfall"] > 0]
    assert len(rainy_obs) > 0
    simulator_engine.set_rain_mode(False)

def test_traffic_service_overview():
    metrics = fetch_overview_metrics()
    assert metrics["total_monitored_roads"] >= 42
    assert metrics["active_vehicles"] > 0
    assert metrics["average_speed_kmh"] > 0
