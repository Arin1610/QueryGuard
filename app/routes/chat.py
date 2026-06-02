from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

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
    return ChatResponse(
        response="QueryGuard is alive.",
        cache_status="MISS",
        latency_ms=0.0
    )