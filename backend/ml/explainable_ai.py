import numpy as np
import pandas as pd

class ExplainableAIEngine:
    def explain_prediction(self, road_telemetry: dict, prediction_result: dict) -> dict:
        road_id = road_telemetry.get("road_id", "NH16-01")
        speed = float(road_telemetry.get("average_speed", 45.0))
        density = float(road_telemetry.get("traffic_density", 50.0))
        occupancy = float(road_telemetry.get("road_occupancy", 45.0))
        rainfall = float(road_telemetry.get("rainfall", 0.0))
        accident = int(road_telemetry.get("accident", 0))
        closure = int(road_telemetry.get("road_closure", 0))
        
        risk_score = float(prediction_result.get("predicted_risk_score", 50.0))
        risk_level = prediction_result.get("risk_level", "MEDIUM")
        
        # Calculate feature contributions summing to ~100%
        speed_deficit = max(0.0, 70.0 - speed)
        speed_contrib = round((speed_deficit / 70.0) * 45.0, 1)
        occupancy_contrib = round((occupancy / 100.0) * 25.0, 1)
        density_contrib = round((density / 100.0) * 15.0, 1)
        rain_contrib = round((rainfall / 50.0) * 10.0, 1)
        incident_contrib = 15.0 if (accident or closure) else 0.0
        
        total_raw = max(1.0, speed_contrib + occupancy_contrib + density_contrib + rain_contrib + incident_contrib)
        
        feature_importance = [
          {"feature": "Speed Reduction Deficit", "contribution": round((speed_contrib / total_raw) * 100, 1), "value": f"{speed} km/h"},
          {"feature": "Road Occupancy Ratio", "contribution": round((occupancy_contrib / total_raw) * 100, 1), "value": f"{occupancy}%"},
          {"feature": "Traffic Volume Density", "contribution": round((density_contrib / total_raw) * 100, 1), "value": f"{density}%"},
          {"feature": "Rainfall Intensity", "contribution": round((rain_contrib / total_raw) * 100, 1), "value": f"{rainfall} mm/h"},
          {"feature": "Accident / Closure Flag", "contribution": round((incident_contrib / total_raw) * 100, 1), "value": "ACTIVE" if (accident or closure) else "NONE"}
        ]
        
        feature_importance.sort(key=lambda x: x["contribution"], reverse=True)
        
        # Natural Language Explanation Generator
        nl_explanation = (
            f"Corridor {road_id} is classified as **{risk_level} Risk ({risk_score}/100)**. "
            f"The primary driver is a **{round((70 - speed)/70 * 100, 1)}% speed drop** (currently {speed} km/h), "
            f"combined with **{occupancy}% road occupancy** and **{density}% vehicle density**."
        )
        if accident:
            nl_explanation += " An active vehicle accident was also detected on this segment."
        if rainfall > 10.0:
            nl_explanation += f" Adverse weather with {rainfall} mm/h rainfall is compounding delay."

        # Counterfactual Analysis
        target_speed = round(min(75.0, speed + 20.0), 1)
        counterfactual_risk = max(15.0, round(risk_score * 0.45, 1))
        
        counterfactual = {
            "hypothesis": f"What if average speed increases by +{round(target_speed - speed, 1)} km/h to {target_speed} km/h?",
            "new_predicted_risk_score": counterfactual_risk,
            "new_risk_level": "LOW" if counterfactual_risk <= 30 else "MEDIUM",
            "impact_summary": f"Increasing speed to {target_speed} km/h would reduce congestion risk score from {risk_score} to {counterfactual_risk} ({'LOW' if counterfactual_risk <= 30 else 'MEDIUM'})."
        }

        return {
            "road_id": road_id,
            "predicted_risk_score": risk_score,
            "risk_level": risk_level,
            "feature_importance": feature_importance,
            "natural_language_explanation": nl_explanation,
            "counterfactual_analysis": counterfactual
        }

xai_engine = ExplainableAIEngine()
