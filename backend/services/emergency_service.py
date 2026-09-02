from backend.simulation.road_graph import city_road_graph, INTERSECTION_NODES

active_emergency_corridor = {
    "vehicle_id": "AMB-911",
    "vehicle_type": "Ambulance",
    "origin": "Apollo General Hospital (J01)",
    "origin_node": "J01",
    "destination": "City Trauma Center (J08)",
    "destination_node": "J08",
    "recommended_route": "NH16-01 -> NH16-02 -> NH16-03 -> NH16-04 -> NH16-05 -> NH16-06",
    "intersections": [
        {"intersection_id": "J01", "name": "Vani Vihar Square", "signal_state": "GREEN_OVERRIDE", "sequence": 1},
        {"intersection_id": "J02", "name": "Acharya Vihar Junction", "signal_state": "GREEN_OVERRIDE", "sequence": 2},
        {"intersection_id": "J03", "name": "Jaydev Vihar Cross", "signal_state": "GREEN_OVERRIDE", "sequence": 3},
        {"intersection_id": "J17", "name": "Kalinga Stadium Junction", "signal_state": "GREEN_OVERRIDE", "sequence": 4},
        {"intersection_id": "J20", "name": "Chandrasekharpur Square", "signal_state": "GREEN_OVERRIDE", "sequence": 5},
        {"intersection_id": "J07", "name": "Patia Square", "signal_state": "GREEN_OVERRIDE", "sequence": 6},
        {"intersection_id": "J08", "name": "KIIT Square", "signal_state": "GREEN_OVERRIDE", "sequence": 7}
    ],
    "estimated_eta_mins": 7.5,
    "time_saved_mins": 11.5,
    "status": "ACTIVE_SIMULATED_CORRIDOR"
}

def get_active_emergency_corridor():
    return active_emergency_corridor

def create_emergency_green_corridor(vehicle_type: str, origin_node: str = "J01", destination_node: str = "J08"):
    global active_emergency_corridor
    
    # Calculate emergency path using smart congestion routing
    route = city_road_graph.find_route_dijkstra(origin_node, destination_node, mode="smart")
    
    if not route:
        nodes_seq = [origin_node, destination_node]
        corridors_seq = [f"{origin_node}-{destination_node}"]
        eta = 10.0
        distance = 8.5
    else:
        nodes_seq = route["nodes"]
        corridors_seq = route["corridors"]
        eta = route["eta_mins"]
        distance = route["distance_km"]

    # Build intersection signal pre-emption sequence
    intersections = []
    for idx, node in enumerate(nodes_seq):
        node_info = INTERSECTION_NODES.get(node, {"name": f"Intersection {node}"})
        intersections.append({
            "intersection_id": node,
            "name": node_info["name"],
            "signal_state": "GREEN_OVERRIDE",
            "sequence": idx + 1
        })
        
    origin_name = INTERSECTION_NODES.get(origin_node, {}).get("name", origin_node)
    dest_name = INTERSECTION_NODES.get(destination_node, {}).get("name", destination_node)
    
    # Standard emergency response time is ~2.2x without green corridor
    normal_eta = round(eta * 2.2, 1)
    time_saved = max(3.0, round(normal_eta - eta, 1))

    active_emergency_corridor = {
        "vehicle_id": f"EMG-{hash(vehicle_type + origin_node + destination_node) % 1000:03d}",
        "vehicle_type": vehicle_type,
        "origin": f"{origin_name} ({origin_node})",
        "origin_node": origin_node,
        "destination": f"{dest_name} ({destination_node})",
        "destination_node": destination_node,
        "recommended_route": " -> ".join(corridors_seq),
        "intersections": intersections,
        "estimated_eta_mins": round(eta, 1),
        "time_saved_mins": time_saved,
        "status": "ACTIVE_SIMULATED_CORRIDOR"
    }
    
    return active_emergency_corridor
