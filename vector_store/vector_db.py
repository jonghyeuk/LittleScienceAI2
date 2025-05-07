# 🔹 vector_store/vector_db.py

import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.get_or_create_collection("isef_papers")

def build_vector_index():
    df = pd.read_excel("data/isef_titles.xlsx")
    titles = df["논문제목"].dropna().tolist()
    embeddings = model.encode(titles)
    for i, title in enumerate(titles):
        collection.add(documents=[title], embeddings=[embeddings[i]], ids=[f"paper_{i}"])

def search_similar_titles(query: str) -> list[str]:
    q_embed = model.encode([query])[0]
    results = collection.query(query_embeddings=[q_embed], n_results=5)
    return results["documents"][0]
