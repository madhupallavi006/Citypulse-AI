from backend.services.llm_service import process_operator_chat, rule_based_fallback_assistant

def test_rule_based_fallback_assistant_rain():
    res = rule_based_fallback_assistant("heavy rain in downtown zone", [])
    assert "Monsoon" in res or "Speed" in res
    assert "Rule-Based" in res

def test_process_operator_chat_without_api_keys():
    res = process_operator_chat("Recommend green corridor for ambulance at Vani Vihar Square")
    assert "response" in res
    assert "provider_mode" in res
    assert res["provider_mode"] in ["RULE-BASED FALLBACK ACTIVE", "GEMINI LLM ACTIVE", "GROQ LLM ACTIVE"]
    assert len(res["rag_sources"]) > 0
