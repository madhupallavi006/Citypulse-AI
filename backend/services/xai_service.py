from backend.services.traffic_service import get_latest_telemetry
from backend.ml.predict import predict_telemetry_risk
from backend.ml.explainable_ai import xai_engine

def explain_corridor_risk(road_id: str = "NH16-01"):
    telemetry_list = get_latest_telemetry()
    target_telemetry = next((r for r in telemetry_list if r["road_id"] == road_id), None)
    
    if not target_telemetry:
        target_telemetry = {
            "road_id": road_id,
            "average_speed": 22.5,
            "traffic_density": 85.0,
            "road_occupancy": 78.0,
            "vehicle_count": 1450,
            "rainfall": 12.0,
            "accident": 0,
            "road_closure": 0
        }

    preds = predict_telemetry_risk([target_telemetry])
    prediction_result = preds[0] if preds else {"predicted_risk_score": 68.0, "risk_level": "HIGH"}
    
    explanation = xai_engine.explain_prediction(target_telemetry, prediction_result)
    return explanation
