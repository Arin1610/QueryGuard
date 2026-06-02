from fastapi import FastAPI
from app.routes.chat import router

app = FastAPI(
    title="QueryGuard",
    description="Semantic Caching Gateway for LLM APIs",
    version="1.0.0"
)

app.include_router(router, prefix="/v1")

@app.get("/health")
def health():
    return {"status": "ok", "service": "QueryGuard"}