"""Hallucination detection evaluation.

Checks if the LLM response is grounded in the provided context.
"""

import json

from backend.services.llm_service import LLMService


class HallucinationDetector:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def detect(
        self, response: str, context_chunks: list[str]
    ) -> dict:
        """Detect hallucinated claims not supported by context."""
        context = "\n---\n".join(context_chunks)

        prompt = f"""Analyze the following response and determine which claims are supported by the context.

Context:
{context}

Response:
{response}

For each claim in the response, determine if it is:
- GROUNDED: Directly supported by the context
- HALLUCINATED: Not supported by or contradicts the context

Return a JSON object with:
{{
  "grounded_claims": ["list of grounded claims"],
  "hallucinated_claims": ["list of hallucinated claims"],
  "groundedness_score": 0.0 to 1.0
}}

Respond with ONLY valid JSON."""

        result = await self.llm.generate(prompt)
        try:
            parsed = json.loads(result)
            return {
                "grounded_claims": parsed.get("grounded_claims", []),
                "hallucinated_claims": parsed.get("hallucinated_claims", []),
                "groundedness_score": float(parsed.get("groundedness_score", 0)),
            }
        except (json.JSONDecodeError, ValueError):
            return {
                "grounded_claims": [],
                "hallucinated_claims": [],
                "groundedness_score": 0.0,
                "error": "Failed to parse LLM output",
            }
