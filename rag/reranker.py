import logging

from sentence_transformers import CrossEncoder

from backend.config import settings

logger = logging.getLogger(__name__)


class Reranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        candidates: list[dict],
        top_k: int | None = None,
    ) -> list[dict]:
        k = top_k or settings.RERANK_TOP_K

        if not candidates:
            return []

        pairs = [(query, c["text"]) for c in candidates]
        scores = self.model.predict(pairs)

        for i, score in enumerate(scores):
            candidates[i]["rerank_score"] = float(score)

        ranked = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
        return ranked[:k]


# Singleton
_reranker: Reranker | None = None


def get_reranker() -> Reranker:
    global _reranker
    if _reranker is None:
        _reranker = Reranker()
    return _reranker
