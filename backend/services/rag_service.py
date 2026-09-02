from backend.rag.retriever import sop_retriever

def retrieve_relevant_sops(query: str, top_k: int = 3):
    results = sop_retriever.retrieve(query=query, top_k=top_k)
    return results
