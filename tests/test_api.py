from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["system"] == "CityPulse AI Platform Backend"

def test_traffic_overview_endpoint():
    response = client.get("/api/traffic/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_monitored_roads" in data
    assert "critical_roads" in data

def test_incidents_endpoint():
    response = client.get("/api/incidents")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["incidents"]) > 0

def test_chat_endpoint():
    response = client.post("/api/chat", json={"message": "Which roads are congested?"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["response"]) > 0
