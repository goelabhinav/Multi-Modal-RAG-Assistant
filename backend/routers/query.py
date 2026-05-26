from fastapi import APIRouter

from backend.models.schemas import Citation, QueryRequest, QueryResponse
from rag.pipeline import get_rag_pipeline

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_assistant(request: QueryRequest):
    pipeline = get_rag_pipeline()

    doc_filter = None
    if request.filters and "document_id" in request.filters:
        doc_filter = request.filters["document_id"]

    result = await pipeline.query(request.query, doc_filter=doc_filter)

    return QueryResponse(
        answer=result.answer,
        citations=[
            Citation(
                document_id=c["document_id"],
                chunk_index=c["chunk_index"],
                text=c["text"],
                score=c["score"],
            )
            for c in result.citations
        ],
        confidence_score=result.confidence_score,
        sources=result.sources,
        latency_ms=result.latency_ms,
    )
