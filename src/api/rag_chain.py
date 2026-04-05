import os
import time
import google.generativeai as genai

from src.retrieval.vector_store import VectorStore


class RAGChain:
    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")

        genai.configure(api_key=api_key)

        # ✅ WORKING model (avoid old/invalid ones)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        self.store = VectorStore()

    def build_prompt(self, question, context_chunks):
        """
        Build prompt with retrieved context
        """
        context_text = ""

        for i, chunk in enumerate(context_chunks):
            context_text += f"\n---\nChunk {i+1}:\n{chunk['text']}\n"

        prompt = f"""
You are an expert automotive assistant.

Use ONLY the provided context to answer the question.
If answer is not present, say "Not found in documents".

Context:
{context_text}

Question:
{question}

Answer clearly:
"""
        return prompt

    def run(self, question: str, top_k: int = 5):
        """
        Full RAG pipeline:
        1. Retrieve
        2. Build prompt
        3. Generate answer
        """

        start_time = time.time()

        try:
            # 🔍 Step 1: Retrieve relevant chunks
            results = self.store.query(question, top_k=top_k)

            if not results:
                return {
                    "answer": "No relevant information found in documents.",
                    "sources": []
                }

            # 🧠 Step 2: Build prompt
            prompt = self.build_prompt(question, results)

            # 🤖 Step 3: Generate answer
            response = self.model.generate_content(prompt)

            answer = response.text

            # 📚 Step 4: Prepare sources
            sources = []
            for r in results:
                sources.append({
                    "text_preview": r["text"][:150],
                    "metadata": r.get("metadata", {})
                })

            return {
                "question": question,
                "answer": answer,
                "sources": sources,
                "time_taken": round(time.time() - start_time, 2)
            }

        except Exception as e:
            return {
                "error": str(e)
            }