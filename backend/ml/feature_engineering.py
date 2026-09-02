import pandas as pd
import numpy as np

FEATURE_COLUMNS = [
    'vehicle_count', 'average_speed', 'road_occupancy', 'traffic_density',
    'rainfall', 'accident', 'construction', 'road_closure', 'event',
    'signal_failure', 'day_of_week', 'hour', 'is_weekend', 'speed_ratio'
]

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Feature 1: Weekend Indicator
    df['is_weekend'] = df['day_of_week'].apply(lambda d: 1 if d >= 5 else 0)
    
    # Feature 2: Speed ratio vs baseline speed limit
    # Determine free flow baseline per corridor
    def get_baseline_speed(road_id):
        if "NH16" in str(road_id):
            return 70.0
        elif "ORR" in str(road_id):
            return 60.0
        return 45.0
        
    df['baseline_speed'] = df['road_id'].apply(get_baseline_speed)
    df['speed_ratio'] = np.clip(df['average_speed'] / df['baseline_speed'], 0.0, 1.5)
    
    return df

def prepare_train_test_data(csv_path="data/synthetic_traffic_dataset.csv"):
    df = pd.read_csv(csv_path)
    df = engineer_features(df)
    
    X = df[FEATURE_COLUMNS]
    y = df['congestion']
    
    return X, y
