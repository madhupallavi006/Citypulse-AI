from backend.ml.explainable_ai import xai_engine
from backend.services.xai_service import explain_corridor_risk

def test_explainable_ai_engine():
    telemetry = {
        "road_id": "NH16-03",
        "average_speed": 18.0,
        "traffic_density": 88.0,
        "road_occupancy": 82.0,
        "vehicle_count": 1600,
        "rainfall": 15.0,
        "accident": 1,
        "road_closure": 0
    }
    prediction = {"predicted_risk_score": 82.0, "risk_level": "CRITICAL"}
    
    explanation = xai_engine.explain_prediction(telemetry, prediction)
    assert explanation["road_id"] == "NH16-03"
    assert len(explanation["feature_importance"]) == 5
    assert "natural_language_explanation" in explanation
    assert "counterfactual_analysis" in explanation
    assert explanation["counterfactual_analysis"]["new_predicted_risk_score"] < 82.0

def test_explain_corridor_risk_service():
    res = explain_corridor_risk("NH16-01")
    assert "road_id" in res
    assert "feature_importance" in res
    assert res["road_id"] == "NH16-01"
