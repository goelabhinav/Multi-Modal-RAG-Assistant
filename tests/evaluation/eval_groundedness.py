"""Groundedness evaluation.

Evaluates whether a response is factually grounded in the provided source documents.
"""

from backend.services.llm_service import LLMService


class GroundednessEvaluator:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def evaluate(
        self, query: str, response: str, context_chunks: list[str]
    ) -> dict:
        """Evaluate groundedness of a response given context."""
        context = "\n---\n".join(context_chunks)

        prompt = f"""Evaluate how well the following response is grounded in the provided context.

Query: {query}
Context: {context}
Response: {response}

Score the following on a scale of 0.0 to 1.0:

1. Relevance: Does the response address the query?
2. Faithfulness: Are all claims in the response supported by the context?
3. Completeness: Does the response cover the key information from the context?

Respond with ONLY three decimal numbers, one per line:
relevance_score
faithfulness_score
completeness_score"""

        result = await self.llm.generate(prompt)
        try:
            lines = [line.strip() for line in result.strip().split("\n") if line.strip()]
            scores = [max(0.0, min(1.0, float(s))) for s in lines[:3]]
            while len(scores) < 3:
                scores.append(0.0)
            return {
                "relevance": scores[0],
                "faithfulness": scores[1],
                "completeness": scores[2],
                "overall": sum(scores) / len(scores),
            }
        except (ValueError, IndexError):
            return {
                "relevance": 0.0,
                "faithfulness": 0.0,
                "completeness": 0.0,
                "overall": 0.0,
                "error": "Failed to parse scores",
            }
