from backend.services.emergency_service import get_active_emergency_corridor, create_emergency_green_corridor
from backend.services.transit_service import fetch_bus_transit_priorities

def test_get_active_emergency_corridor():
    corridor = get_active_emergency_corridor()
    assert corridor is not None
    assert "vehicle_id" in corridor
    assert "estimated_eta_mins" in corridor

def test_create_emergency_green_corridor():
    new_corridor = create_emergency_green_corridor("Fire Truck", "J04", "J12")
    assert new_corridor["vehicle_type"] == "Fire Truck"
    assert new_corridor["origin_node"] == "J04"
    assert new_corridor["destination_node"] == "J12"
    assert len(new_corridor["intersections"]) >= 2
    assert new_corridor["time_saved_mins"] > 0.0

def test_fetch_bus_transit_priorities():
    priorities = fetch_bus_transit_priorities()
    assert len(priorities) > 0
    bus = priorities[0]
    assert "bus_id" in bus
    assert "delay_mins" in bus
    assert "recommended_action" in bus
