from sentence_transformers import SentenceTransformer

from backend.config import settings


class EmbeddingService:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = SentenceTransformer(self.model_name)
        self.dimension = settings.EMBEDDING_DIMENSION

    def embed_text(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts).tolist()


# Singleton instance
_embedding_service: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
