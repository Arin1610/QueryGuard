import chromadb
from app.cache.embedder import embedder

SIMILARITY_THRESHOLD = 0.92

class SemanticCache:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("query_cache")

    def get(self, query: str):
        """Check cache. Return cached response if similar query exists."""
        embedding = embedder.embed(query)
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=1
        )

        if not results["distances"][0]:
            return None

        distance = results["distances"][0][0]
        similarity = 1 - distance

        if similarity >= SIMILARITY_THRESHOLD:
            return {
                "response": results["documents"][0][0],
                "similarity": similarity
            }
        return None

    def set(self, query: str, response: str):
        """Store a new query-response pair in cache."""
        embedding = embedder.embed(query)
        self.collection.add(
            embeddings=[embedding],
            documents=[response],
            ids=[str(hash(query))]
        )

cache = SemanticCache()