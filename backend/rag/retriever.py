import os
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from backend.rag.ingest_sops import RAG_INDEX_PATH, build_rag_index

class RAGRetriever:
    def __init__(self):
        self.index_data = None
        self._load_index()

    def _load_index(self):
        if not os.path.exists(RAG_INDEX_PATH):
            self.index_data = build_rag_index()
        else:
            self.index_data = joblib.load(RAG_INDEX_PATH)

    def retrieve(self, query: str, top_k: int = 3) -> list:
        if not self.index_data:
            self._load_index()
            
        vectorizer = self.index_data["vectorizer"]
        tfidf_matrix = self.index_data["tfidf_matrix"]
        documents = self.index_data["documents"]
        
        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        
        top_indices = similarities.argsort()[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            doc = documents[idx]
            results.append({
                "id": doc["id"],
                "title": doc["title"],
                "category": doc["category"],
                "content": doc["content"],
                "relevance_score": round(score, 3)
            })
            
        return results

sop_retriever = RAGRetriever()
