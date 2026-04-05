from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="Automotive Multimodal RAG")

app.include_router(router)