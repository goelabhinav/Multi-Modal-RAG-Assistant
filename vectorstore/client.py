from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from backend.config import settings


class QdrantManager:
    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
    ):
        self.host = host or settings.QDRANT_HOST
        self.port = port or settings.QDRANT_PORT
        self.client = QdrantClient(host=self.host, port=self.port)

    def ensure_collection(self, name: str | None = None):
        collection_name = name or settings.QDRANT_COLLECTION
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE,
                ),
            )

    def get_client(self) -> QdrantClient:
        return self.client


# Singleton instance
_qdrant_manager: QdrantManager | None = None


def get_qdrant_manager() -> QdrantManager:
    global _qdrant_manager
    if _qdrant_manager is None:
        _qdrant_manager = QdrantManager()
        _qdrant_manager.ensure_collection()
    return _qdrant_manager
