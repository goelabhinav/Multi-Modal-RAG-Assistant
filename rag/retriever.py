from backend.config import settings
from embeddings.embedding_service import get_embedding_service
from vectorstore.operations import search_vectors


class Retriever:
    def __init__(self):
        self.embedding_service = get_embedding_service()

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        doc_filter: str | None = None,
    ) -> list[dict]:
        k = top_k or settings.RETRIEVAL_TOP_K
        query_vector = self.embedding_service.embed_text(query)
        results = search_vectors(query_vector, top_k=k, doc_filter=doc_filter)
        return results


# Singleton
_retriever: Retriever | None = None


def get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever
