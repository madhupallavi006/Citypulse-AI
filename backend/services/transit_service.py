def fetch_bus_transit_priorities():
    return [
        {
            "bus_id": "BUS-102",
            "route_name": "Route 102 (Airport -> KIIT Campus)",
            "current_location": "AG Square (J14)",
            "delay_mins": 8.5,
            "upcoming_intersections": ["J14", "J15", "J16"],
            "recommended_action": "Extend Green Signal by +12 seconds at J15 & J16",
            "estimated_delay_reduction_mins": 5.0,
            "status": "PRIORITY_RECOMMENDED"
        },
        {
            "bus_id": "BUS-204",
            "route_name": "Route 204 (CBD Metro Express)",
            "current_location": "Master Canteen (J04)",
            "delay_mins": 5.2,
            "upcoming_intersections": ["J04", "J05"],
            "recommended_action": "Truncate Red Signal Phase by -8 seconds at J05",
            "estimated_delay_reduction_mins": 3.5,
            "status": "PRIORITY_RECOMMENDED"
        }
    ]
