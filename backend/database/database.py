import sqlite3
import os

DB_PATH = os.getenv("SQLITE_DB_PATH", "./data/citypulse.db")

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Roads Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roads (
        road_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        speed_limit_kmh REAL NOT NULL,
        length_km REAL NOT NULL,
        start_lat REAL NOT NULL,
        start_lng REAL NOT NULL,
        end_lat REAL NOT NULL,
        end_lng REAL NOT NULL
    )
    """)

    # Intersections Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS intersections (
        intersection_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        lat REAL NOT NULL,
        lng REAL NOT NULL,
        signal_status TEXT DEFAULT 'GREEN'
    )
    """)

    # Traffic Observations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS traffic_observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        road_id TEXT NOT NULL,
        intersection_id TEXT NOT NULL,
        vehicle_count INTEGER NOT NULL,
        average_speed REAL NOT NULL,
        road_occupancy REAL NOT NULL,
        traffic_density REAL NOT NULL,
        rainfall REAL NOT NULL,
        weather_condition TEXT NOT NULL,
        accident INTEGER DEFAULT 0,
        construction INTEGER DEFAULT 0,
        road_closure INTEGER DEFAULT 0,
        event INTEGER DEFAULT 0,
        signal_failure INTEGER DEFAULT 0,
        congestion_risk INTEGER NOT NULL,
        risk_level TEXT NOT NULL,
        FOREIGN KEY (road_id) REFERENCES roads (road_id)
    )
    """)

    # Incidents Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id TEXT PRIMARY KEY,
        road_id TEXT NOT NULL,
        type TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        description TEXT
    )
    """)

    conn.commit()

    # Seed Initial Roads if Empty
    cursor.execute("SELECT COUNT(*) as count FROM roads")
    if cursor.fetchone()["count"] == 0:
        seed_roads(cursor)
        conn.commit()

    conn.close()

def seed_roads(cursor):
    roads_data = []
    
    # 10 NH16 Corridors
    for i in range(1, 11):
        roads_data.append((
            f"NH16-{i:02d}", f"NH16 Express Corridor #{i}", 80.0, 12.5,
            20.2971 + (i * 0.01), 85.8245 + (i * 0.01),
            20.3071 + (i * 0.01), 85.8345 + (i * 0.01)
        ))
        
    # 12 Outer Ring Road (ORR) Corridors
    for i in range(1, 13):
        roads_data.append((
            f"ORR-{i:02d}", f"Outer Ring Link #{i}", 65.0, 9.0,
            20.2500 + (i * 0.012), 85.8000 + (i * 0.008),
            20.2600 + (i * 0.012), 85.8100 + (i * 0.008)
        ))
        
    # 10 Central Business District (CBD) Corridors
    for i in range(1, 11):
        roads_data.append((
            f"CBD-{i:02d}", f"CBD Downtown Boulevard #{i}", 50.0, 5.2,
            20.2800 + (i * 0.005), 85.8400 + (i * 0.005),
            20.2850 + (i * 0.005), 85.8450 + (i * 0.005)
        ))
        
    # 10 Metro Arterial Corridors
    for i in range(1, 11):
        roads_data.append((
            f"METRO-{i:02d}", f"Metro Transit Avenue #{i}", 55.0, 7.8,
            20.3100 + (i * 0.007), 85.8150 + (i * 0.006),
            20.3170 + (i * 0.007), 85.8210 + (i * 0.006)
        ))

    cursor.executemany("""
    INSERT INTO roads (road_id, name, speed_limit_kmh, length_km, start_lat, start_lng, end_lat, end_lng)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, roads_data)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
