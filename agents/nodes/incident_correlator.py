import logging

from agents.state import AgentState
from agents.tools.retrieval_tool import retrieve_relevant_chunks
from backend.services.llm_service import get_llm_service

logger = logging.getLogger(__name__)


async def incident_correlator_node(state: AgentState) -> dict:
    """Correlates current query with historical incidents and related documents."""
    llm = get_llm_service()
    query = state["query"]

    chunks = retrieve_relevant_chunks(query, top_k=10)

    content = "\n\n".join(
        f"[Doc: {c['document_id']}, Chunk: {c['chunk_index']}]\n{c['text']}"
        for c in chunks
    )

    prompt = f"""Analyze the following documents and identify correlations between incidents.

Documents:
{content}

Query: {query}

Identify:
1. Related incidents across documents
2. Common patterns or recurring issues
3. Timeline of events if applicable
4. Affected components or systems

Correlation Analysis:"""

    analysis = await llm.generate(prompt)

    analysis_results = state.get("analysis_results", {})
    analysis_results["incident_correlation"] = {
        "analysis": analysis,
        "documents_analyzed": len(chunks),
    }

    return {
        "analysis_results": analysis_results,
        "documents": chunks,
    }
