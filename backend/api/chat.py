from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.llm_service import process_operator_chat

router = APIRouter(prefix="/api/chat", tags=["AI Operator Assistant"])

class ChatRequest(BaseModel):
    message: str

@router.post("")
def chat_with_operator_assistant(req: ChatRequest):
    result = process_operator_chat(req.message)
    return {
        "status": "success",
        "reply": result["response"],
        "response": result["response"],
        "provider_mode": result["provider_mode"],
        "rag_sources": result["rag_sources"]
    }
