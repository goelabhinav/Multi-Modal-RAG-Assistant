"""Retrieval relevance evaluation.

Evaluates how well the retrieval system returns relevant chunks for a given query.
"""

from backend.services.llm_service import LLMService


class RetrievalEvaluator:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def evaluate_relevance(self, query: str, retrieved_chunks: list[str]) -> float:
        """Use LLM-as-judge to score relevance of retrieved chunks."""
        chunks_text = "\n---\n".join(
            f"Chunk {i + 1}: {chunk}" for i, chunk in enumerate(retrieved_chunks)
        )

        prompt = f"""Rate the overall relevance of these retrieved passages to the query.

Query: {query}

Retrieved Passages:
{chunks_text}

Score the relevance from 0.0 (completely irrelevant) to 1.0 (perfectly relevant).
Consider: Do the passages contain information needed to answer the query?

Respond with ONLY a decimal number between 0.0 and 1.0."""

        result = await self.llm.generate(prompt)
        try:
            score = float(result.strip())
            return max(0.0, min(1.0, score))
        except ValueError:
            return 0.0

    def precision_at_k(
        self, relevant_ids: set[str], retrieved_ids: list[str], k: int
    ) -> float:
        """Standard Precision@K metric."""
        retrieved_k = retrieved_ids[:k]
        relevant_retrieved = set(retrieved_k) & relevant_ids
        return len(relevant_retrieved) / k if k > 0 else 0.0

    def recall_at_k(
        self, relevant_ids: set[str], retrieved_ids: list[str], k: int
    ) -> float:
        """Standard Recall@K metric."""
        retrieved_k = retrieved_ids[:k]
        relevant_retrieved = set(retrieved_k) & relevant_ids
        return len(relevant_retrieved) / len(relevant_ids) if relevant_ids else 0.0
