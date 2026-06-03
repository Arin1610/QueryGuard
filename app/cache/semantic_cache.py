import chromadb
from app.cache.embedder import embedder

SIMILARITY_THRESHOLD = 0.90

class SemanticCache:
    def __init__(self, threshold: float = SIMILARITY_THRESHOLD):
        self.threshold = threshold
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=f"query_cache_{str(threshold).replace('.', '_')}",
            metadata={"hnsw:space": "cosine"}
        )

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
        similarity = 1 - distance  # cosine distance → similarity

        print(f"Similarity: {similarity:.4f} (threshold: {self.threshold})")

        if similarity >= self.threshold:
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