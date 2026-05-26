import logging

from agents.state import AgentState
from agents.tools.retrieval_tool import retrieve_relevant_chunks
from backend.services.llm_service import get_llm_service
from rag.prompt_templates import SCREENSHOT_ANALYSIS_PROMPT

logger = logging.getLogger(__name__)


async def screenshot_analyzer_node(state: AgentState) -> dict:
    """Analyzes uploaded screenshots using OCR output and vision context."""
    llm = get_llm_service()
    query = state["query"]

    # Get relevant screenshot-related chunks
    chunks = retrieve_relevant_chunks(query, top_k=5)
    image_chunks = [
        c for c in chunks if c.get("metadata", {}).get("source_type") in ("image/png", "image/jpeg")
    ]

    # Fall back to all chunks if no image-specific ones
    relevant_chunks = image_chunks if image_chunks else chunks

    content = "\n\n".join(c["text"] for c in relevant_chunks)

    prompt = SCREENSHOT_ANALYSIS_PROMPT.format(content=content)
    analysis = await llm.generate(prompt)

    analysis_results = state.get("analysis_results", {})
    analysis_results["screenshot"] = {
        "analysis": analysis,
        "chunks_used": len(relevant_chunks),
    }

    return {
        "analysis_results": analysis_results,
        "documents": relevant_chunks,
    }
