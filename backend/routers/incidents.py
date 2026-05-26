import time

from fastapi import APIRouter

from agents.graph import get_agent_graph
from backend.models.schemas import QueryRequest, QueryResponse, Citation

router = APIRouter()


@router.post("/incidents/analyze", response_model=QueryResponse)
async def analyze_incident(request: QueryRequest):
    """Route query through the multi-agent system for deep analysis."""
    graph = get_agent_graph()
    start = time.perf_counter()

    initial_state = {
        "messages": [],
        "query": request.query,
        "query_type": "",
        "documents": [],
        "analysis_results": {},
        "final_response": "",
        "citations": [],
        "confidence_score": 0.0,
        "metadata": {},
    }

    result = await graph.ainvoke(initial_state)

    latency = (time.perf_counter() - start) * 1000

    return QueryResponse(
        answer=result.get("final_response", "No response generated."),
        citations=[
            Citation(
                document_id=c["document_id"],
                chunk_index=c["chunk_index"],
                text=c["text"],
                score=c["score"],
            )
            for c in result.get("citations", [])
        ],
        confidence_score=result.get("confidence_score", 0.0),
        sources=result.get("documents", []),
        latency_ms=latency,
    )
