import os
import pandas as pd
from backend.ml.feature_engineering import prepare_train_test_data, FEATURE_COLUMNS
from backend.ml.evaluate_model import evaluate_saved_model
from backend.ml.predict import predict_telemetry_risk
from backend.services.prediction_service import fetch_ml_predictions

def test_feature_engineering():
    X, y = prepare_train_test_data()
    assert len(X) > 1000
    assert len(y) == len(X)
    for col in FEATURE_COLUMNS:
        assert col in X.columns

def test_model_artifact_exists():
    assert os.path.exists("models/congestion_model.joblib")

def test_evaluate_saved_model():
    metrics = evaluate_saved_model()
    assert metrics is not None
    assert "accuracy" in metrics
    assert metrics["accuracy"] > 0.90

def test_predict_telemetry_risk():
    sample_telemetry = [{
        "road_id": "NH16-01",
        "average_speed": 18.5,
        "traffic_density": 88.0,
        "road_occupancy": 85.0,
        "vehicle_count": 1600,
        "rainfall": 15.0,
        "accident": 1,
        "construction": 0,
        "road_closure": 0,
        "event": 0,
        "signal_failure": 0
    }]
    
    predictions = predict_telemetry_risk(sample_telemetry)
    assert len(predictions) == 1
    pred = predictions[0]
    assert pred["road_id"] == "NH16-01"
    assert pred["predicted_risk_score"] > 60
    assert pred["risk_level"] in ["HIGH", "CRITICAL"]
    assert "model_used" in pred

def test_fetch_ml_predictions_service():
    predictions = fetch_ml_predictions()
    assert isinstance(predictions, list)
    if len(predictions) > 0:
        top = predictions[0]
        assert "predicted_risk" in top
        assert "confidence" in top
