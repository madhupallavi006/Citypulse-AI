import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

class TrafficAnomalyDetector:
    def __init__(self, contamination=0.08):
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=42,
            n_estimators=100
        )
        self.is_fitted = False

    def fit_on_dataset(self, df: pd.DataFrame):
        features = df[['average_speed', 'traffic_density', 'road_occupancy', 'vehicle_count']]
        self.model.fit(features)
        self.is_fitted = True

    def detect_anomalies(self, telemetry_list: list) -> list:
        if not telemetry_list:
            return []
            
        df = pd.DataFrame(telemetry_list)
        features = df[['average_speed', 'traffic_density', 'road_occupancy', 'vehicle_count']]
        
        if not self.is_fitted:
            self.model.fit(features)
            self.is_fitted = True
            
        scores = self.model.decision_function(features)
        predictions = self.model.predict(features) # -1 for anomaly, 1 for normal
        
        anomalies = []
        for idx, pred in enumerate(predictions):
            if pred == -1 or df.iloc[idx]['accident'] == 1 or df.iloc[idx]['road_closure'] == 1:
                row = df.iloc[idx]
                score = round(float(scores[idx]), 3)
                
                # Determine specific anomaly classification
                avg_speed = row['average_speed']
                density = row['traffic_density']
                occupancy = row['road_occupancy']
                
                if row['accident'] == 1:
                    anomaly_type = "Accident-like Pattern"
                    severity = "CRITICAL"
                    recommendation = "Dispatch immediate traffic emergency unit & flag corridor."
                elif row['road_closure'] == 1:
                    anomaly_type = "Road Blockage / Closure"
                    severity = "HIGH"
                    recommendation = "Reroute incoming traffic via adjacent corridors."
                elif avg_speed < 20.0 and density > 75.0:
                    anomaly_type = "Sudden Speed Drop & Bottleneck"
                    severity = "HIGH" if score < -0.15 else "MEDIUM"
                    recommendation = "Investigate possible obstacle or signal disruption."
                elif occupancy > 85.0:
                    anomaly_type = "Abnormal Road Occupancy Spike"
                    severity = "HIGH"
                    recommendation = "Adjust signal timing at connected intersections."
                else:
                    anomaly_type = "Sudden Traffic Density Surge"
                    severity = "MEDIUM"
                    recommendation = "Monitor corridor flow for bottleneck formation."

                anomalies.append({
                    "id": f"ANO-{(idx + 1):03d}",
                    "road_id": row['road_id'],
                    "intersection_id": row.get('intersection_id', 'J01'),
                    "anomaly_type": anomaly_type,
                    "severity": severity,
                    "anomaly_score": score,
                    "current_speed": avg_speed,
                    "traffic_density": density,
                    "recommended_investigation": recommendation
                })
                
        return anomalies

anomaly_detector_engine = TrafficAnomalyDetector()
