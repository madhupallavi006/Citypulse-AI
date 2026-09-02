from backend.simulation.road_graph import city_road_graph
from backend.services.route_service import get_optimized_route

def test_road_graph_structure():
    assert len(city_road_graph.graph.nodes) >= 20
    assert len(city_road_graph.graph.edges) >= 42

def test_edge_weight_updates():
    city_road_graph.update_edge_weights()
    for u, v, data in city_road_graph.graph.edges(data=True):
        assert "smart_weight" in data
        assert "normal_weight" in data
        assert data["smart_weight"] > 0.0

def test_dijkstra_routing():
    route = city_road_graph.find_route_dijkstra(start_node="J01", end_node="J08", mode="smart")
    assert route is not None
    assert "nodes" in route
    assert "corridors" in route
    assert route["eta_mins"] > 0.0

def test_route_service_comparison():
    res = get_optimized_route(origin_node="J01", destination_node="J08")
    assert "normal_route" in res
    assert "recommended_route" in res
    assert res["recommended_route"]["time_saved_mins"] >= 0.0
