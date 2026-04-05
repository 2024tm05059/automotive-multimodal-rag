from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

class VectorStore:
    def __init__(self):
        self.index = None
        self.texts = []

    def add(self, chunks):
        embeddings = model.encode([c["content"] for c in chunks])

        if self.index is None:
            self.index = faiss.IndexFlatL2(len(embeddings[0]))

        self.index.add(np.array(embeddings))
        self.texts.extend(chunks)

    def search(self, query, k=3):
        q_emb = model.encode([query])
        D, I = self.index.search(np.array(q_emb), k)

        return [self.texts[i] for i in I[0]]