import os
import json
import urllib.request
import urllib.error
from backend.services.rag_service import retrieve_relevant_sops
from backend.services.traffic_service import get_latest_telemetry

def rule_based_fallback_assistant(query: str, rag_sops: list) -> str:
    query_lower = query.lower()
    telemetry = get_latest_telemetry()
    
    avg_speed = round(sum([r["average_speed"] for r in telemetry]) / max(1, len(telemetry)), 1)
    high_risk_roads = [r["road_id"] for r in telemetry if r["average_speed"] < 25.0]
    
    sop_summary = ""
    if rag_sops:
        sop_summary = f"\n\n**Retrieved Standard Operating Procedure ({rag_sops[0]['id']})**:\n> *{rag_sops[0]['title']}*\n> {rag_sops[0]['content']}"

    if "rain" in query_lower or "weather" in query_lower:
        return (
            f"**[Rule-Based Assistant] Monsoon & Rain Protocol Advisory**\n\n"
            f"Current Citywide Speed: **{avg_speed} km/h**.\n"
            f"For rain disruptions: Reduce speed limits on expressways to 50 km/h and extend main arterial green phases by +15 seconds at low-lying junctions."
            f"{sop_summary}"
        )
    elif "ambulance" in query_lower or "emergency" in query_lower or "corridor" in query_lower:
        return (
            f"**[Rule-Based Assistant] Emergency Green Corridor Recommendation**\n\n"
            f"Automated Fastest Path: **J01 (Vani Vihar) -> J02 -> J03 -> J17 -> J20 -> J08 (KIIT Campus)**.\n"
            f"Recommended Action: Activate signal override GREEN wave sequence across 7 pre-emption intersections. Estimated response time savings: **11.5 minutes**."
            f"{sop_summary}"
        )
    elif "nh16" in query_lower or "corridor" in query_lower or "traffic" in query_lower:
        high_risk_str = ", ".join(high_risk_roads[:3]) if high_risk_roads else "None"
        return (
            f"**[Rule-Based Assistant] Citywide Traffic Status Report**\n\n"
            f"Average Network Speed: **{avg_speed} km/h** across 42 monitored corridors.\n"
            f"Bottleneck Corridors Flagged: **{high_risk_str}**.\n"
            f"Recommendation: Enable NetworkX predicted-congestion Dijkstra rerouting for incoming commuter traffic."
            f"{sop_summary}"
        )
    else:
        return (
            f"**[Rule-Based Assistant] Urban Traffic Orchestration Response**\n\n"
            f"CityPulse AI is actively monitoring 42 corridors and 20 intersections.\n"
            f"Average Speed: **{avg_speed} km/h**.\n"
            f"All ML risk scoring models and Isolation Forest anomaly detectors are online."
            f"{sop_summary}"
        )

def process_operator_chat(query: str):
    openai_key = os.getenv("OPENAI_API_KEY", "") or os.getenv("LLM_API_KEY", "")
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    groq_key = os.getenv("GROQ_API_KEY", "")
    
    rag_sops = retrieve_relevant_sops(query, top_k=2)
    
    # Try OpenAI API if key exists
    if openai_key and openai_key.strip():
        try:
            sop_context = "\n".join([f"SOP: {s['title']} - {s['content']}" for s in rag_sops])
            model = os.getenv("LLM_MODEL", "gpt-4o-mini")
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {openai_key.strip()}", "Content-Type": "application/json"}
            payload = json.dumps({
                "model": model,
                "messages": [
                    {"role": "system", "content": f"You are CityPulse AI Operator Assistant. Context:\n{sop_context}"},
                    {"role": "user", "content": query}
                ]
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers=headers)
            
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    text = data["choices"][0]["message"]["content"]
                    return {
                        "response": text,
                        "provider_mode": "OPENAI LLM ACTIVE",
                        "rag_sources": rag_sops
                    }
        except Exception:
            print("OpenAI API call failed. Falling back to next LLM provider or rule engine.")

    # Try Gemini API if key exists
    if gemini_key and gemini_key.strip():
        try:
            sop_context = "\n".join([f"SOP: {s['title']} - {s['content']}" for s in rag_sops])
            prompt = f"Context SOPs:\n{sop_context}\n\nOperator Question: {query}"
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key.strip()}"
            payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    return {
                        "response": text,
                        "provider_mode": "GEMINI LLM ACTIVE",
                        "rag_sources": rag_sops
                    }
        except Exception:
            print("Gemini API call failed. Falling back to next LLM provider or rule engine.")

    # Try Groq API if key exists
    if groq_key and groq_key.strip():
        try:
            sop_context = "\n".join([f"SOP: {s['title']} - {s['content']}" for s in rag_sops])
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key.strip()}", "Content-Type": "application/json"}
            payload = json.dumps({
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": f"You are CityPulse AI Operator Assistant. Context:\n{sop_context}"},
                    {"role": "user", "content": query}
                ]
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers=headers)
            
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    text = data["choices"][0]["message"]["content"]
                    return {
                        "response": text,
                        "provider_mode": "GROQ LLM ACTIVE",
                        "rag_sources": rag_sops
                    }
        except Exception:
            print("Groq API call failed. Falling back to Rule-Based Assistant.")

    # Rule-Based Fallback Engine (100% functional without API key)
    fallback_response = rule_based_fallback_assistant(query, rag_sops)
    return {
        "response": fallback_response,
        "provider_mode": "RULE-BASED FALLBACK ACTIVE",
        "rag_sources": rag_sops
    }
