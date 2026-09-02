from backend.simulation.road_graph import city_road_graph

def get_optimized_route(origin_node: str = "J01", destination_node: str = "J08"):
    # Normal route (ignoring ML predicted risk)
    normal_res = city_road_graph.find_route_dijkstra(origin_node, destination_node, mode="normal")
    
    # CityPulse Congestion-Aware Route (incorporating ML predictions)
    smart_res = city_road_graph.find_route_dijkstra(origin_node, destination_node, mode="smart")
    
    if not normal_res or not smart_res:
        return {
            "origin": origin_node,
            "destination": destination_node,
            "error": "No valid graph path found between nodes."
        }

    normal_eta = normal_res["eta_mins"]
    smart_eta = smart_res["eta_mins"]
    time_saved = max(0, round(normal_eta - smart_eta, 1))

    return {
        "origin": origin_node,
        "destination": destination_node,
        "normal_route": {
            "name": "Standard Shortest Path",
            "corridors": normal_res["corridors"],
            "eta_mins": normal_eta,
            "distance_km": normal_res["distance_km"],
            "max_risk_score": normal_res["max_risk_score"],
            "risk_level": "HIGH" if normal_res["max_risk_score"] > 60 else "MEDIUM"
        },
        "recommended_route": {
            "name": "CityPulse Predicted-Congestion Optimized Route",
            "corridors": smart_res["corridors"],
            "eta_mins": smart_eta,
            "distance_km": smart_res["distance_km"],
            "max_risk_score": smart_res["max_risk_score"],
            "risk_level": "LOW" if smart_res["max_risk_score"] <= 30 else "MEDIUM",
            "time_saved_mins": time_saved
        }
    }
