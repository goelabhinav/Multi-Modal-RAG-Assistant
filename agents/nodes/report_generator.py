import logging

from agents.state import AgentState
from backend.services.llm_service import get_llm_service

logger = logging.getLogger(__name__)


async def report_generator_node(state: AgentState) -> dict:
    """Generates the final response with citations from all agent analyses."""
    llm = get_llm_service()
    query = state["query"]
    analysis_results = state.get("analysis_results", {})
    documents = state.get("documents", [])

    # Compile all analysis
    analysis_parts = []
    for agent_name, result in analysis_results.items():
        if isinstance(result, dict) and "analysis" in result:
            analysis_parts.append(f"## {agent_name}\n{result['analysis']}")

    analysis_text = "\n\n".join(analysis_parts)

    # Compile source references
    source_refs = []
    for doc in documents:
        source_refs.append(f"- [Source: {doc['document_id']}, chunk {doc['chunk_index']}]")
    sources_text = "\n".join(source_refs) if source_refs else "No specific sources referenced."

    prompt = f"""Compile a clear, well-structured response based on the following analysis.

Query: {query}

Analysis Results:
{analysis_text}

Available Sources:
{sources_text}

Write a comprehensive but concise response that:
1. Directly answers the user's question
2. References specific sources using [Source: doc_id, chunk N] format
3. Highlights key findings
4. Provides actionable recommendations if applicable

Response:"""

    response = await llm.generate(prompt)

    # Build citations from documents
    citations = [
        {
            "document_id": doc["document_id"],
            "chunk_index": doc["chunk_index"],
            "text": doc["text"][:200],
            "score": doc.get("rerank_score", doc.get("score", 0)),
        }
        for doc in documents
    ]

    # Estimate confidence from analysis depth
    num_analyses = len(analysis_parts)
    confidence = min(0.3 + (num_analyses * 0.15), 1.0)

    return {
        "final_response": response,
        "citations": citations,
        "confidence_score": confidence,
    }
