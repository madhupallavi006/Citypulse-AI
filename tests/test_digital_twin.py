from backend.services.digital_twin_service import run_what_if_simulation
from backend.simulation.traffic_simulator import simulator_engine

def test_digital_twin_scenario():
    res = run_what_if_simulation(
        rain_severity=50.0,
        demand_multiplier=1.5,
        closed_roads=["NH16-03"],
        signal_override_sec=10,
        transit_surge_factor=1.2
    )
    
    assert "baseline" in res
    assert "scenario" in res
    
    scenario = res["scenario"]
    assert scenario["avg_city_speed_kmh"] > 0
    assert scenario["system_impact_score"] >= 0
    assert len(scenario["ai_recommended_countermeasures"]) > 0

def test_simulator_override_state():
    simulator_engine.set_rain_mode(True)
    assert simulator_engine.rain_mode is True
    
    simulator_engine.set_traffic_multiplier(2.0)
    assert simulator_engine.traffic_multiplier == 2.0
    
    simulator_engine.set_rain_mode(False)
    simulator_engine.set_traffic_multiplier(1.0)
