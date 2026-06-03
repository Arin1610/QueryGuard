from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from collections import defaultdict
import time

from app.cache.semantic_cache import cache
from app.llm.groq_client import call_llm
from app.db.telemetry import log_query

router = APIRouter()

conversation_store = defaultdict(list)

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

@router.post("/chat/completions/{session_id}", response_model=ChatResponse)
async def chat(session_id: str, request: ChatRequest):
    query = request.messages[-1].content
    start = time.time()

    # Load conversation history
    history = conversation_store[session_id]
    history.append({"role": "user", "content": query})

    # Check cache first
    cached = cache.get(query)
    if cached:
        latency = (time.time() - start) * 1000
        history.append({"role": "assistant", "content": cached["response"]})
        conversation_store[session_id] = history[-10:]
        log_query(query, cached["response"], "HIT", latency, 0, 0, cached["similarity"])
        return ChatResponse(
            response=cached["response"],
            cache_status="HIT",
            latency_ms=round(latency, 2)
        )

    # Cache miss — call Groq with full history
    llm_result = call_llm(history)
    latency = (time.time() - start) * 1000

    # Save to cache and history
    cache.set(query, llm_result["content"])
    history.append({"role": "assistant", "content": llm_result["content"]})
    conversation_store[session_id] = history[-10:]

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