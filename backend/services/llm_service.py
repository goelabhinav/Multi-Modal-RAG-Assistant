import base64
import logging

from langchain_ollama import ChatOllama

from backend.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(
        self,
        model: str | None = None,
        vision_model: str | None = None,
        base_url: str | None = None,
    ):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model_name = model or settings.OLLAMA_MODEL
        self.vision_model_name = vision_model or settings.OLLAMA_VISION_MODEL

        self.llm = ChatOllama(
            model=self.model_name,
            base_url=self.base_url,
            temperature=0.1,
        )

    async def generate(self, prompt: str) -> str:
        response = await self.llm.ainvoke(prompt)
        return response.content

    async def generate_with_context(self, question: str, context: str) -> str:
        prompt = f"""Based on the following context, answer the question.
If the answer cannot be found in the context, say so clearly.
Always cite which parts of the context support your answer.

Context:
{context}

Question: {question}

Answer:"""
        return await self.generate(prompt)

    async def analyze_image(self, image_path: str, prompt: str) -> str:
        vision_llm = ChatOllama(
            model=self.vision_model_name,
            base_url=self.base_url,
            temperature=0.1,
        )

        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        from langchain_core.messages import HumanMessage

        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}},
            ]
        )

        response = await vision_llm.ainvoke([message])
        return response.content

    async def classify_query(self, query: str) -> str:
        prompt = f"""Classify the following query into one of these categories:
- "screenshot": about UI screenshots, visual errors, UI failures
- "log": about logs, stack traces, error messages, CI/CD output
- "incident": about incidents, outages, historical issues, correlations
- "general": general questions about documents

Query: {query}

Respond with ONLY the category name, nothing else."""

        result = await self.generate(prompt)
        result = result.strip().lower().strip('"')
        if result not in ("screenshot", "log", "incident", "general"):
            return "general"
        return result


# Singleton
_llm_service: LLMService | None = None


def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
