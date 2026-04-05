from sentence_transformers import SentenceTransformer
from src.retrieval.vector_store import search
from src.models.llm import generate_answer

model = SentenceTransformer('all-MiniLM-L6-v2')

def query_rag(question):
    query_embedding = model.encode([question])
    results = search(query_embedding)

    return generate_answer(question, results)