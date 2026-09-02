from backend.services.demo_service import trigger_demo_scenario

def test_demo_morning_peak():
    res = trigger_demo_scenario("morning_peak")
    assert res["status"] == "ACTIVATED"
    assert res["scenario_id"] == "morning_peak"
    assert res["metrics"]["traffic_multiplier"] == 1.8

def test_demo_monsoon_disaster():
    res = trigger_demo_scenario("monsoon_disaster")
    assert res["status"] == "ACTIVATED"
    assert res["scenario_id"] == "monsoon_disaster"
    assert res["metrics"]["rain_severity"] == 85.0

def test_demo_emergency_ambulance():
    res = trigger_demo_scenario("emergency_ambulance")
    assert res["status"] == "ACTIVATED"
    assert res["scenario_id"] == "emergency_ambulance"
    assert res["metrics"]["intersections_preempted"] >= 2

def test_demo_stadium_event():
    res = trigger_demo_scenario("stadium_event")
    assert res["status"] == "ACTIVATED"
    assert res["scenario_id"] == "stadium_event"
    assert res["metrics"]["traffic_multiplier"] == 2.5
