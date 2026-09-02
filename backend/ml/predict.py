import os
import joblib
import pandas as pd
import numpy as np

MODEL_PATH = "models/congestion_model.joblib"
_model_artifact = None

def get_model_artifact():
    global _model_artifact
    if _model_artifact is None:
        if os.path.exists(MODEL_PATH):
            _model_artifact = joblib.load(MODEL_PATH)
        else:
            _model_artifact = None
    return _model_artifact

def predict_telemetry_risk(telemetry_list: list) -> list:
    artifact = get_model_artifact()
    
    predictions = []
    
    for item in telemetry_list:
        road_id = item.get("road_id", "NH16-01")
        avg_speed = float(item.get("average_speed", 30.0))
        density = float(item.get("traffic_density", 50.0))
        occupancy = float(item.get("road_occupancy", 50.0))
        vehicle_count = int(item.get("vehicle_count", 1000))
        rainfall = float(item.get("rainfall", 0.0))
        accident = int(item.get("accident", 0))
        construction = int(item.get("construction", 0))
        road_closure = int(item.get("road_closure", 0))
        event = int(item.get("event", 0))
        signal_failure = int(item.get("signal_failure", 0))
        
        baseline_speed = 70.0 if "NH16" in road_id else (60.0 if "ORR" in road_id else 45.0)
        speed_ratio = np.clip(avg_speed / baseline_speed, 0.0, 1.5)
        
        feature_dict = {
            'vehicle_count': vehicle_count,
            'average_speed': avg_speed,
            'road_occupancy': occupancy,
            'traffic_density': density,
            'rainfall': rainfall,
            'accident': accident,
            'construction': construction,
            'road_closure': road_closure,
            'event': event,
            'signal_failure': signal_failure,
            'day_of_week': 2, # Default current weekday
            'hour': 18,       # Default peak hour
            'is_weekend': 0,
            'speed_ratio': speed_ratio
        }
        
        if artifact and "model" in artifact:
            feature_df = pd.DataFrame([feature_dict])[artifact["feature_columns"]]
            prob = float(artifact["model"].predict_proba(feature_df)[0][1])
            risk_score = min(100, max(0, int(prob * 100)))
        else:
            # Fallback heuristic calculation if model file not yet serialized
            risk_score = min(100, max(0, int(
                (density * 0.45) + 
                (((baseline_speed - avg_speed) / baseline_speed) * 45) +
                (15 if rainfall > 0 else 0) +
                (20 if accident or road_closure else 0)
            )))
            prob = float(risk_score / 100.0)

        if risk_score <= 30:
            risk_level = "LOW"
        elif risk_score <= 60:
            risk_level = "MEDIUM"
        elif risk_score <= 80:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
            
        predictions.append({
            "road_id": road_id,
            "average_speed": avg_speed,
            "traffic_density": density,
            "vehicle_count": vehicle_count,
            "predicted_risk_score": risk_score,
            "risk_level": risk_level,
            "predicted_probability": round(prob, 3),
            "prediction_horizon_mins": 20,
            "model_used": artifact["model_name"] if artifact else "Heuristic ML Fallback"
        })
        
    return predictions
