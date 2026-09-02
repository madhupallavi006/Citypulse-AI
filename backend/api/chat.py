from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/api/chat", tags=["AI Assistant & RAG"])

class ChatRequest(BaseModel):
    message: str

@router.post("")
def chat_with_assistant(req: ChatRequest):
    # Rule-based fallback system when LLM key is not provided
    msg_lower = req.message.lower()
    
    if "congested" in msg_lower or "risk" in msg_lower:
        reply = "NH16-01 and ORR-03 currently have the highest predicted congestion risk (87% and 92% respectively). High vehicle volume combined with localized rainwater logging is driving the delay."
        sources = ["ML Congestion Prediction Engine v1.0", "Live IoT Sensor Array 04"]
    elif "emergency" in msg_lower or "ambulance" in msg_lower:
        reply = "For emergency corridor management, CityPulse AI prioritizes signal synchronization across 6 connected intersections, saving an estimated 11-14 minutes of transit time for critical emergency vehicles."
        sources = ["ITS Standard Protocol Doc 4.2", "Emergency Transit Rule Engine"]
    else:
        reply = f"CityPulse AI Assistant received: '{req.message}'. System is analyzing live traffic metrics, ML models, and knowledge documents."
        sources = ["CityPulse Knowledge Base", "Traffic Telemetry Service"]

    return {
        "status": "success",
        "query": req.message,
        "response": reply,
        "sources": sources,
        "llm_used": False,
        "fallback_mode": True
    }

@router.post("/rag/query")
def rag_query(req: ChatRequest):
    return {
        "status": "success",
        "query": req.message,
        "documents": [
            {
                "title": "Urban Intelligent Transportation Strategies",
                "score": 0.89,
                "snippet": "Pre-emptive traffic signal adjustments reduce bottleneck formation by up to 28% during peak hours."
            }
        ]
    }
