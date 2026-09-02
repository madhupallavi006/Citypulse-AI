import math
import networkx as nx
from backend.database.database import get_db_connection
from backend.services.traffic_service import get_latest_telemetry
from backend.ml.predict import predict_telemetry_risk

# 20 Intersections with Latitude / Longitude
INTERSECTION_NODES = {
    "J01": {"name": "Vani Vihar Square", "lat": 20.2971, "lng": 85.8245},
    "J02": {"name": "Acharya Vihar Junction", "lat": 20.3010, "lng": 85.8290},
    "J03": {"name": "Jaydev Vihar Cross", "lat": 20.3071, "lng": 85.8345},
    "J04": {"name": "Master Canteen Square", "lat": 20.2680, "lng": 85.8400},
    "J05": {"name": "Rajmahal Square", "lat": 20.2600, "lng": 85.8350},
    "J06": {"name": "Khandagiri Square", "lat": 20.2500, "lng": 85.8000},
    "J07": {"name": "Patia Square", "lat": 20.3500, "lng": 85.8180},
    "J08": {"name": "KIIT Square", "lat": 20.3580, "lng": 85.8150},
    "J09": {"name": "CRPF Square", "lat": 20.2880, "lng": 85.8120},
    "J10": {"name": "Fire Station Square", "lat": 20.2780, "lng": 85.8050},
    "J11": {"name": "Rasalgarh Square", "lat": 20.2850, "lng": 85.8600},
    "J12": {"name": "Kalpana Square", "lat": 20.2520, "lng": 85.8450},
    "J13": {"name": "Airport Square", "lat": 20.2580, "lng": 85.8180},
    "J14": {"name": "AG Square", "lat": 20.2700, "lng": 85.8300},
    "J15": {"name": "Governor House Square", "lat": 20.2760, "lng": 85.8250},
    "J16": {"name": "Power House Square", "lat": 20.2920, "lng": 85.8200},
    "J17": {"name": "Kalinga Stadium Junction", "lat": 20.3000, "lng": 85.8180},
    "J18": {"name": "Sailashree Vihar Cross", "lat": 20.3350, "lng": 85.8120},
    "J19": {"name": "Infocity Junction", "lat": 20.3450, "lng": 85.8080},
    "J20": {"name": "Chandrasekharpur Square", "lat": 20.3200, "lng": 85.8200},
}

class RoadNetworkGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self._initialize_base_graph()

    def _initialize_base_graph(self):
        # Add Nodes
        for node_id, data in INTERSECTION_NODES.items():
            self.graph.add_node(node_id, name=data["name"], lat=data["lat"], lng=data["lng"])
            
        # Define 42 unique directed corridor edges across the 20 intersection nodes
        edges_definition = [
            # 10 NH16 Corridors
            ("J01", "J02", "NH16-01", "NH16 Express Corridor #01", 12.5, 80.0),
            ("J02", "J03", "NH16-02", "NH16 Express Corridor #02", 12.5, 80.0),
            ("J03", "J17", "NH16-03", "NH16 Express Corridor #03", 12.5, 80.0),
            ("J17", "J20", "NH16-04", "NH16 Express Corridor #04", 12.5, 80.0),
            ("J20", "J07", "NH16-05", "NH16 Express Corridor #05", 12.5, 80.0),
            ("J07", "J08", "NH16-06", "NH16 Express Corridor #06", 12.5, 80.0),
            ("J08", "J18", "NH16-07", "NH16 Express Corridor #07", 12.5, 80.0),
            ("J18", "J19", "NH16-08", "NH16 Express Corridor #08", 12.5, 80.0),
            ("J19", "J11", "NH16-09", "NH16 Express Corridor #09", 12.5, 80.0),
            ("J11", "J04", "NH16-10", "NH16 Express Corridor #10", 12.5, 80.0),

            # 12 ORR Corridors
            ("J01", "J06", "ORR-01", "Outer Ring Link #01", 9.0, 65.0),
            ("J06", "J10", "ORR-02", "Outer Ring Link #02", 9.0, 65.0),
            ("J10", "J13", "ORR-03", "Outer Ring Link #03", 9.0, 65.0),
            ("J13", "J05", "ORR-04", "Outer Ring Link #04", 9.0, 65.0),
            ("J05", "J12", "ORR-05", "Outer Ring Link #05", 9.0, 65.0),
            ("J12", "J11", "ORR-06", "Outer Ring Link #06", 9.0, 65.0),
            ("J11", "J02", "ORR-07", "Outer Ring Link #07", 9.0, 65.0),
            ("J02", "J16", "ORR-08", "Outer Ring Link #08", 9.0, 65.0),
            ("J16", "J09", "ORR-09", "Outer Ring Link #09", 9.0, 65.0),
            ("J09", "J15", "ORR-10", "Outer Ring Link #10", 9.0, 65.0),
            ("J15", "J14", "ORR-11", "Outer Ring Link #11", 9.0, 65.0),
            ("J14", "J01", "ORR-12", "Outer Ring Link #12", 9.0, 65.0),

            # 10 CBD Corridors
            ("J04", "J05", "CBD-01", "CBD Boulevard #01", 5.2, 50.0),
            ("J05", "J14", "CBD-02", "CBD Boulevard #02", 5.2, 50.0),
            ("J14", "J15", "CBD-03", "CBD Boulevard #03", 5.2, 50.0),
            ("J15", "J16", "CBD-04", "CBD Boulevard #04", 5.2, 50.0),
            ("J16", "J03", "CBD-05", "CBD Boulevard #05", 5.2, 50.0),
            ("J03", "J01", "CBD-06", "CBD Boulevard #06", 5.2, 50.0),
            ("J04", "J12", "CBD-07", "CBD Boulevard #07", 5.2, 50.0),
            ("J12", "J13", "CBD-08", "CBD Boulevard #08", 5.2, 50.0),
            ("J13", "J09", "CBD-09", "CBD Boulevard #09", 5.2, 50.0),
            ("J09", "J10", "CBD-10", "CBD Boulevard #10", 5.2, 50.0),

            # 10 Metro Corridors
            ("J06", "J13", "METRO-01", "Metro Avenue #01", 7.8, 55.0),
            ("J10", "J09", "METRO-02", "Metro Avenue #02", 7.8, 55.0),
            ("J09", "J16", "METRO-03", "Metro Avenue #03", 7.8, 55.0),
            ("J16", "J17", "METRO-04", "Metro Avenue #04", 7.8, 55.0),
            ("J17", "J02", "METRO-05", "Metro Avenue #05", 7.8, 55.0),
            ("J18", "J07", "METRO-06", "Metro Avenue #06", 7.8, 55.0),
            ("J19", "J08", "METRO-07", "Metro Avenue #07", 7.8, 55.0),
            ("J08", "J17", "METRO-08", "Metro Avenue #08", 7.8, 55.0),
            ("J15", "J04", "METRO-09", "Metro Avenue #09", 7.8, 55.0),
            ("J14", "J12", "METRO-10", "Metro Avenue #10", 7.8, 55.0),
        ]

        for u, v, road_id, name, length_km, speed_limit in edges_definition:
            self.graph.add_edge(u, v, road_id=road_id, name=name, length_km=length_km, speed_limit=speed_limit)

    def update_edge_weights(self, telemetry_list: list = None):
        if telemetry_list is None:
            telemetry_list = get_latest_telemetry()
            
        ml_predictions = predict_telemetry_risk(telemetry_list)
        pred_dict = {p["road_id"]: p for p in ml_predictions}
        
        for u, v, data in self.graph.edges(data=True):
            road_id = data["road_id"]
            length_km = data["length_km"]
            speed_limit = data["speed_limit"]
            
            telemetry_item = pred_dict.get(road_id, {})
            avg_speed = float(telemetry_item.get("average_speed", speed_limit))
            risk_score = float(telemetry_item.get("predicted_risk_score", 30))
            
            # Physical base ETA (minutes)
            base_eta_mins = (length_km / (max(8.0, avg_speed) / 60.0))
            
            # Normal route weight (only considers current speed)
            normal_weight = base_eta_mins
            
            # CityPulse predicted-congestion-aware weight
            # Includes future risk score penalty + disruption penalty
            congestion_multiplier = 1.0 + ((risk_score / 100.0) ** 1.8)
            smart_weight = base_eta_mins * congestion_multiplier
            
            self.graph[u][v]["normal_weight"] = normal_weight
            self.graph[u][v]["smart_weight"] = smart_weight
            self.graph[u][v]["current_speed"] = avg_speed
            self.graph[u][v]["risk_score"] = risk_score

    def find_route_dijkstra(self, start_node: str = "J01", end_node: str = "J08", mode: str = "smart"):
        self.update_edge_weights()
        weight_key = "smart_weight" if mode == "smart" else "normal_weight"
        
        try:
            path = nx.dijkstra_path(self.graph, start_node, end_node, weight=weight_key)
            total_weight = nx.dijkstra_path_length(self.graph, start_node, end_node, weight=weight_key)
            
            road_sequence = []
            total_distance_km = 0.0
            max_risk = 0
            
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                edge = self.graph[u][v]
                road_sequence.append(edge["road_id"])
                total_distance_km += edge["length_km"]
                max_risk = max(max_risk, int(edge.get("risk_score", 20)))
                
            return {
                "nodes": path,
                "corridors": road_sequence,
                "eta_mins": round(float(total_weight), 1),
                "distance_km": round(float(total_distance_km), 1),
                "max_risk_score": max_risk
            }
        except nx.NetworkXNoPath:
            return None

city_road_graph = RoadNetworkGraph()
