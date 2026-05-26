import logging

from agents.state import AgentState
from agents.tools.retrieval_tool import retrieve_relevant_chunks
from backend.services.llm_service import get_llm_service
from rag.prompt_templates import LOG_ANALYSIS_PROMPT

logger = logging.getLogger(__name__)


async def log_analyzer_node(state: AgentState) -> dict:
    """Analyzes log files for errors, patterns, and stack traces."""
    llm = get_llm_service()
    query = state["query"]

    chunks = retrieve_relevant_chunks(query, top_k=5)
    log_chunks = [
        c
        for c in chunks
        if c.get("metadata", {}).get("source_type") in ("text/plain", "log")
    ]

    relevant_chunks = log_chunks if log_chunks else chunks

    content = "\n\n".join(c["text"] for c in relevant_chunks)

    prompt = LOG_ANALYSIS_PROMPT.format(content=content)
    analysis = await llm.generate(prompt)

    analysis_results = state.get("analysis_results", {})
    analysis_results["log"] = {
        "analysis": analysis,
        "chunks_used": len(relevant_chunks),
    }

    return {
        "analysis_results": analysis_results,
        "documents": relevant_chunks,
    }
