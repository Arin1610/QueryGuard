from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import time

from app.cache.semantic_cache import cache
from app.llm.groq_client import call_llm
from app.db.telemetry import log_query

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "llama-3.1-8b-instant"
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str
    cache_status: str
    latency_ms: float

@router.post("/chat/completions", response_model=ChatResponse)
async def chat(request: ChatRequest):
    query = request.messages[-1].content
    start = time.time()

    # Check cache first
    cached = cache.get(query)
    if cached:
        latency = (time.time() - start) * 1000
        log_query(
            query, cached["response"], "HIT",
            latency, 0, 0, cached["similarity"]
        )
        return ChatResponse(
            response=cached["response"],
            cache_status="HIT",
            latency_ms=round(latency, 2)
        )

    # Cache miss — call Groq
    llm_result = call_llm([m.dict() for m in request.messages])
    latency = (time.time() - start) * 1000

    # Save to cache for future
    cache.set(query, llm_result["content"])

    # Log to DB
    log_query(
        query, llm_result["content"], "MISS",
        latency, llm_result["prompt_tokens"],
        llm_result["completion_tokens"], 0.0
    )

    return ChatResponse(
        response=llm_result["content"],
        cache_status="MISS",
        latency_ms=round(latency, 2)
    )