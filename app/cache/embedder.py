from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self):
        self._model = None

    def _load_model(self):
        if self._model is None:
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
        return self._model

    def embed(self, text: str) -> list:
        model = self._load_model()
        return model.encode(text).tolist()

embedder = Embedder()