from sentence_transformers import SentenceTransformer
from src.retrieval.vector_store import store_embeddings

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks):
    texts = []
    metadata = []

    for chunk in chunks:
        text = f"[{chunk['type'].upper()}] {chunk['content']}"
        texts.append(text)
        metadata.append(chunk)

    embeddings = model.encode(texts)
    store_embeddings(embeddings, texts, metadata)