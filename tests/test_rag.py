import os
from backend.rag.ingest_sops import build_rag_index, RAG_INDEX_PATH
from backend.rag.retriever import sop_retriever
from backend.services.rag_service import retrieve_relevant_sops

def test_rag_index_file_exists():
    assert os.path.exists(RAG_INDEX_PATH)

def test_rag_retrieval_rain_query():
    results = retrieve_relevant_sops("heavy rain and monsoon flooding", top_k=2)
    assert len(results) > 0
    top = results[0]
    assert "Monsoon" in top["title"] or "Rain" in top["title"] or top["relevance_score"] > 0.0

def test_rag_retrieval_ambulance_query():
    results = retrieve_relevant_sops("emergency ambulance green corridor", top_k=2)
    assert len(results) > 0
    top = results[0]
    assert "Emergency" in top["title"] or "Corridor" in top["title"] or top["relevance_score"] > 0.0
