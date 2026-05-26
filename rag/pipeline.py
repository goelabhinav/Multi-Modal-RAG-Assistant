import logging
import time
from dataclasses import dataclass, field

from backend.services.llm_service import get_llm_service
from rag.prompt_templates import QUERY_PROMPT
from rag.reranker import get_reranker
from rag.retriever import get_retriever

logger = logging.getLogger(__name__)


@dataclass
class RAGResponse:
    answer: str
    citations: list[dict] = field(default_factory=list)
    confidence_score: float = 0.0
    sources: list[dict] = field(default_factory=list)
    latency_ms: float = 0.0


class RAGPipeline:
    def __init__(self):
        self.retriever = get_retriever()
        self.reranker = get_reranker()
        self.llm = get_llm_service()

    async def query(
        self,
        question: str,
        doc_filter: str | None = None,
    ) -> RAGResponse:
        start = time.perf_counter()

        # 1. Retrieve candidates
        candidates = self.retriever.retrieve(question, doc_filter=doc_filter)

        if not candidates:
            return RAGResponse(
                answer="No relevant documents found. Please upload documents first.",
                latency_ms=(time.perf_counter() - start) * 1000,
            )

        # 2. Rerank
        reranked = self.reranker.rerank(question, candidates)

        # 3. Build context
        context = self._build_context(reranked)

        # 4. Generate answer
        prompt = QUERY_PROMPT.format(context=context, question=question)
        answer = await self.llm.generate(prompt)

        # 5. Build citations
        citations = [
            {
                "document_id": chunk["document_id"],
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"][:200],
                "score": chunk.get("rerank_score", chunk.get("score", 0)),
            }
            for chunk in reranked
        ]

        # 6. Compute confidence from rerank scores
        confidence = self._compute_confidence(reranked)

        latency = (time.perf_counter() - start) * 1000

        return RAGResponse(
            answer=answer,
            citations=citations,
            confidence_score=confidence,
            sources=reranked,
            latency_ms=latency,
        )

    def _build_context(self, chunks: list[dict]) -> str:
        parts = []
        for chunk in chunks:
            source = f"[Source: {chunk['document_id']}, chunk {chunk['chunk_index']}]"
            parts.append(f"{source}\n{chunk['text']}")
        return "\n\n---\n\n".join(parts)

    def _compute_confidence(self, chunks: list[dict]) -> float:
        if not chunks:
            return 0.0
        scores = [c.get("rerank_score", c.get("score", 0)) for c in chunks]
        # Normalize: rerank scores can be negative, map to 0-1
        max_score = max(scores)
        if max_score <= 0:
            return 0.1
        return min(round(max_score / 10.0, 2), 1.0)


# Singleton
_pipeline: RAGPipeline | None = None


def get_rag_pipeline() -> RAGPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = RAGPipeline()
    return _pipeline
