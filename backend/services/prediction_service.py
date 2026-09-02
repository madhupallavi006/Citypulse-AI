from backend.services.traffic_service import get_latest_telemetry
from backend.ml.predict import predict_telemetry_risk

def fetch_ml_predictions():
    telemetry = get_latest_telemetry()
    ml_output = predict_telemetry_risk(telemetry)
    
    predictions = []
    for item in ml_output:
        if item["risk_level"] in ["HIGH", "CRITICAL"] or item["predicted_risk_score"] >= 50:
            main_cause = "High vehicle density + Speed degradation"
            if item["predicted_risk_score"] >= 80:
                main_cause = "Severe bottleneck + Environmental/Incident disruption"
                
            predictions.append({
                "road_id": item["road_id"],
                "current_status": f"{item['risk_level']} Congestion Risk",
                "predicted_risk": item["predicted_risk_score"],
                "prediction_horizon_mins": 20,
                "confidence": item["predicted_probability"],
                "main_cause": main_cause,
                "recommended_action": f"Reroute incoming traffic away from {item['road_id']}"
            })
            
    # Sort by risk score descending
    predictions.sort(key=lambda x: x["predicted_risk"], reverse=True)
    return predictions
