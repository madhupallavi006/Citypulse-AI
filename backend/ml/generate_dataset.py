import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_dataset(output_path="data/synthetic_traffic_dataset.csv", num_days=14):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    np.random.seed(42)
    
    road_ids = [f"NH16-{i:02d}" for i in range(1, 11)] + \
               [f"ORR-{i:02d}" for i in range(1, 13)] + \
               [f"CBD-{i:02d}" for i in range(1, 11)] + \
               [f"METRO-{i:02d}" for i in range(1, 10)]
               
    intersections = [f"J{i:02d}" for i in range(1, 21)]
    
    start_date = datetime(2026, 8, 1, 0, 0, 0)
    timestamps = [start_date + timedelta(minutes=15 * i) for i in range(num_days * 24 * 4)]
    
    records = []
    
    for ts in timestamps:
        hour = ts.hour
        day_of_week = ts.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        
        # Base peak hour factor
        if (8 <= hour <= 10 or 17 <= hour <= 20) and not is_weekend:
            base_traffic_factor = np.random.uniform(1.4, 2.0)
        elif (11 <= hour <= 16) and not is_weekend:
            base_traffic_factor = np.random.uniform(0.9, 1.3)
        elif is_weekend and (12 <= hour <= 21):
            base_traffic_factor = np.random.uniform(1.1, 1.5)
        else:
            base_traffic_factor = np.random.uniform(0.3, 0.7)
            
        for road in road_ids:
            intersection = np.random.choice(intersections)
            
            # Weather simulation
            is_rainy = np.random.choice([0, 1], p=[0.85, 0.15])
            rainfall = round(float(np.random.uniform(5.0, 45.0)), 1) if is_rainy else 0.0
            temperature = round(float(np.random.uniform(22.0, 34.0)), 1)
            weather = "Rainy" if is_rainy else "Clear"
            
            # Random disruptions
            accident = int(np.random.choice([0, 1], p=[0.97, 0.03]))
            construction = int(np.random.choice([0, 1], p=[0.95, 0.05]))
            road_closure = int(np.random.choice([0, 1], p=[0.98, 0.02]))
            event = int(np.random.choice([0, 1], p=[0.96, 0.04]))
            signal_failure = int(np.random.choice([0, 1], p=[0.985, 0.015]))
            
            # Vehicle count & density calculations
            base_capacity = 1200 if "NH16" in road or "ORR" in road else 800
            vehicle_count = int(base_capacity * base_traffic_factor * np.random.uniform(0.85, 1.15))
            
            if accident:
                vehicle_count = int(vehicle_count * 1.3)
            
            traffic_density = min(100.0, round(float((vehicle_count / (base_capacity * 1.8)) * 100.0), 1))
            road_occupancy = min(100.0, round(float(traffic_density * np.random.uniform(0.85, 1.05)), 1))
            
            # Speed drop simulation
            free_flow_speed = 70.0 if "NH16" in road else (60.0 if "ORR" in road else 45.0)
            speed_penalty = (traffic_density / 100.0) * 35.0
            
            if is_rainy:
                speed_penalty += np.random.uniform(8.0, 15.0)
            if accident:
                speed_penalty += np.random.uniform(20.0, 30.0)
            if road_closure:
                speed_penalty += np.random.uniform(25.0, 35.0)
            if signal_failure:
                speed_penalty += np.random.uniform(10.0, 20.0)
                
            average_speed = max(8.0, round(float(free_flow_speed - speed_penalty), 1))
            
            # Congestion calculation
            congestion_risk = min(100, int(
                (traffic_density * 0.45) + 
                ((free_flow_speed - average_speed) / free_flow_speed * 40.0) +
                (15 if is_rainy else 0) +
                (20 if accident else 0)
            ))
            
            congestion = 1 if congestion_risk >= 65 else 0
            
            records.append({
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "road_id": road,
                "intersection_id": intersection,
                "vehicle_count": vehicle_count,
                "average_speed": average_speed,
                "road_occupancy": road_occupancy,
                "traffic_density": traffic_density,
                "rainfall": rainfall,
                "temperature": temperature,
                "weather_condition": weather,
                "accident": accident,
                "construction": construction,
                "road_closure": road_closure,
                "event": event,
                "signal_failure": signal_failure,
                "day_of_week": day_of_week,
                "hour": hour,
                "congestion_risk": congestion_risk,
                "congestion": congestion
            })
            
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} synthetic traffic observations saved to {output_path}")
    return df

if __name__ == "__main__":
    generate_synthetic_dataset()
