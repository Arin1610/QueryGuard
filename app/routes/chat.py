from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import time

from app.cache.semantic_cache import cache

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "llama3-8b-8192"
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
        return ChatResponse(
            response=cached["response"],
            cache_status="HIT",
            latency_ms=round(latency, 2)
        )

    # Cache miss — LLM call coming Day 3
    return ChatResponse(
        response="[LLM call coming Day 3]",
        cache_status="MISS",
        latency_ms=round((time.time() - start) * 1000, 2)
    )