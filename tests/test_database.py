import os
import sqlite3
from backend.database.database import get_db_connection, init_db

def test_database_initialization():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify roads table
    cursor.execute("SELECT COUNT(*) as count FROM roads")
    road_count = cursor.fetchone()["count"]
    assert road_count >= 42
    
    # Verify tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row["name"] for row in cursor.fetchall()]
    assert "roads" in tables
    assert "intersections" in tables
    assert "traffic_observations" in tables
    assert "incidents" in tables
    
    conn.close()

def test_traffic_observation_insertion():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO traffic_observations (
        timestamp, road_id, intersection_id, vehicle_count, average_speed,
        road_occupancy, traffic_density, rainfall, weather_condition,
        accident, construction, road_closure, event, signal_failure,
        congestion_risk, risk_level
    ) VALUES ('2026-09-02 19:00:00', 'NH16-01', 'J01', 1200, 32.5, 65.0, 70.0, 0.0, 'Clear', 0, 0, 0, 0, 0, 75, 'HIGH')
    """)
    conn.commit()
    
    cursor.execute("SELECT * FROM traffic_observations WHERE road_id = 'NH16-01' ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    assert row["congestion_risk"] == 75
    assert row["risk_level"] == "HIGH"
    
    conn.close()
