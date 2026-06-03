from sqlalchemy.orm import sessionmaker
from app.db.models import engine, QueryLog

SessionLocal = sessionmaker(bind=engine)

def log_query(
    query: str,
    response: str,
    cache_status: str,
    latency_ms: float,
    prompt_tokens: int,
    completion_tokens: int,
    similarity_score: float
):
    db = SessionLocal()
    try:
        log = QueryLog(
            query_text=query,
            response_text=response,
            cache_status=cache_status,
            latency_ms=latency_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            similarity_score=similarity_score
        )
        db.add(log)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Telemetry error: {e}")
    finally:
        db.close()