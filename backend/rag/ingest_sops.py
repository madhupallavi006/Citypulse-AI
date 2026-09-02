import os
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

SOP_FILE_PATH = os.path.join("data", "traffic_sops.json")
RAG_INDEX_PATH = os.path.join("models", "rag_index.joblib")

def build_rag_index():
    print("Loading traffic SOPs knowledge corpus...")
    if not os.path.exists(SOP_FILE_PATH):
        raise FileNotFoundError(f"SOP corpus not found at {SOP_FILE_PATH}")
        
    with open(SOP_FILE_PATH, "r", encoding="utf-8") as f:
        documents = json.load(f)
        
    texts = [f"{doc['title']} - {doc['category']}: {doc['content']}" for doc in documents]
    
    print(f"Indexing {len(documents)} SOP documents into TF-IDF vector space...")
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    os.makedirs(os.path.dirname(RAG_INDEX_PATH), exist_ok=True)
    
    index_data = {
        "documents": documents,
        "vectorizer": vectorizer,
        "tfidf_matrix": tfidf_matrix
    }
    
    joblib.dump(index_data, RAG_INDEX_PATH)
    print(f"RAG index successfully built and saved to {RAG_INDEX_PATH}")
    return index_data

if __name__ == "__main__":
    build_rag_index()
