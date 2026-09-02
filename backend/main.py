import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.api.traffic import router as traffic_router
from backend.api.incidents import router as incidents_router
from backend.api.routes import router as routes_router
from backend.api.emergency import router as emergency_router
from backend.api.simulation import router as simulation_router
from backend.api.chat import router as chat_router
from backend.api.agents import router as agents_router

load_dotenv()

app = FastAPI(
    title="CityPulse AI Backend",
    description="A Predictive Urban Traffic Orchestration Platform API",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(traffic_router)
app.include_router(incidents_router)
app.include_router(routes_router)
app.include_router(emergency_router)
app.include_router(simulation_router)
app.include_router(chat_router)
app.include_router(agents_router)

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "system": "CityPulse AI Platform Backend",
        "version": "1.0.0",
        "mode": "Active Multi-Agent Orchestration"
    }

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.main:app", host=host, port=port, reload=True)
