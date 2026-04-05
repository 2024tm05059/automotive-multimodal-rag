from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import time
import os
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


from src.ingestion.ingest import ingest_pdf
from src.retrieval.vector_store import VectorStore
from pydantic import BaseModel

class IngestResponse(BaseModel):
    filename: str
    text_chunks: int
    image_chunks: int
    total_chunks: int

router = APIRouter()
vector_store = VectorStore()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


start_time = time.time()


@router.get("/health")
def health():
    return {
        "status": "running",
        "documents_indexed": len(vector_store.texts),
        "uptime": round(time.time() - start_time, 2)
    }

@router.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = ingest_pdf(file_path)

    vector_store.add(chunks)

    text_n = sum(1 for c in chunks if c["type"] == "text")
    image_n = sum(1 for c in chunks if c["type"] == "image")

    return {
        "filename": file.filename,
        "text_chunks": text_n,
        "image_chunks": image_n,
        "total_chunks": len(chunks)
    }


@router.post("/query")
def query(q: str):
    try:
        store = VectorStore()
        results = store.search(q)

        if not results:
            return {"answer": "No relevant data found", "sources": []}

        #  NO GEMINI — JUST RETURN CONTENT
        answer = "\n\n".join([r["content"] for r in results[:3]])

        return {
            "answer": answer,
            "sources": [
                {
                    "page": r.get("page", 0),
                    "type": r.get("chunk_type", "text")
                }
                for r in results
            ]
        }

    except Exception as e:
        return {"error": str(e)}