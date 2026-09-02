import random
import time
from datetime import datetime
from backend.database.database import get_db_connection

class TrafficSimulator:
    def __init__(self):
        self.rain_mode = False
        self.traffic_multiplier = 1.0
        self.active_incidents = {}

    def set_rain_mode(self, active: bool):
        self.rain_mode = active

    def set_traffic_multiplier(self, multiplier: float):
        self.traffic_multiplier = max(0.5, min(3.0, multiplier))

    def add_incident_override(self, road_id: str, incident_type: str, severity: str):
        self.active_incidents[road_id] = {
            "type": incident_type,
            "severity": severity,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def generate_current_telemetry(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT road_id, name, speed_limit_kmh FROM roads")
        roads = cursor.fetchall()
        
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hour = datetime.now().hour
        
        # Peak hour dynamics
        is_peak = (8 <= hour <= 10 or 17 <= hour <= 20)
        base_density = random.uniform(55, 75) if is_peak else random.uniform(25, 45)
        
        observations = []
        
        for road in roads:
            road_id = road["road_id"]
            speed_limit = road["speed_limit_kmh"]
            
            density = min(98.0, max(10.0, (base_density * self.traffic_multiplier) + random.uniform(-10, 10)))
            occupancy = min(99.0, max(8.0, density * random.uniform(0.85, 1.05)))
            vehicle_count = int(density * 18.5)
            
            rainfall = random.uniform(12.0, 35.0) if self.rain_mode else 0.0
            weather = "Rainy" if self.rain_mode else "Clear"
            
            has_incident = road_id in self.active_incidents
            accident = 1 if has_incident and self.active_incidents[road_id]["type"] == "Accident" else 0
            closure = 1 if has_incident and self.active_incidents[road_id]["type"] == "Road Closure" else 0
            
            # Calculate speed based on density, rain, and incidents
            speed_drop = (density / 100.0) * (speed_limit * 0.5)
            if self.rain_mode:
                speed_drop += random.uniform(8, 14)
            if has_incident:
                speed_drop += random.uniform(20, 35)
                
            avg_speed = max(8.0, round(speed_limit - speed_drop, 1))
            
            # Congestion Risk Score 0-100
            risk_score = min(100, max(5, int(
                (density * 0.45) + 
                (((speed_limit - avg_speed) / speed_limit) * 45) +
                (12 if self.rain_mode else 0) +
                (20 if has_incident else 0)
            )))
            
            if risk_score <= 30:
                risk_level = "LOW"
            elif risk_score <= 60:
                risk_level = "MEDIUM"
            elif risk_score <= 80:
                risk_level = "HIGH"
            else:
                risk_level = "CRITICAL"

            obs = {
                "timestamp": now_str,
                "road_id": road_id,
                "intersection_id": f"J{(hash(road_id) % 20) + 1:02d}",
                "vehicle_count": vehicle_count,
                "average_speed": avg_speed,
                "road_occupancy": round(occupancy, 1),
                "traffic_density": round(density, 1),
                "rainfall": round(rainfall, 1),
                "weather_condition": weather,
                "accident": accident,
                "construction": 0,
                "road_closure": closure,
                "event": 0,
                "signal_failure": 0,
                "congestion_risk": risk_score,
                "risk_level": risk_level
            }
            observations.append(obs)
            
            # Persist to SQLite
            cursor.execute("""
            INSERT INTO traffic_observations (
                timestamp, road_id, intersection_id, vehicle_count, average_speed,
                road_occupancy, traffic_density, rainfall, weather_condition,
                accident, construction, road_closure, event, signal_failure,
                congestion_risk, risk_level
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                obs["timestamp"], obs["road_id"], obs["intersection_id"],
                obs["vehicle_count"], obs["average_speed"], obs["road_occupancy"],
                obs["traffic_density"], obs["rainfall"], obs["weather_condition"],
                obs["accident"], obs["construction"], obs["road_closure"],
                obs["event"], obs["signal_failure"], obs["congestion_risk"],
                obs["risk_level"]
            ))

        conn.commit()
        conn.close()
        return observations

# Singleton instance
simulator_engine = TrafficSimulator()
