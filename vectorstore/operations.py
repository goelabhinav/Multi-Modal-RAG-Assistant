import uuid

from qdrant_client.models import Filter, FieldCondition, MatchValue, PointStruct

from backend.config import settings
from vectorstore.client import get_qdrant_manager


def upsert_vectors(
    vectors: list[list[float]],
    payloads: list[dict],
    collection_name: str | None = None,
) -> list[str]:
    manager = get_qdrant_manager()
    client = manager.get_client()
    name = collection_name or settings.QDRANT_COLLECTION

    point_ids = []
    points = []
    for vector, payload in zip(vectors, payloads):
        point_id = str(uuid.uuid4())
        point_ids.append(point_id)
        points.append(
            PointStruct(
                id=point_id,
                vector=vector,
                payload=payload,
            )
        )

    client.upsert(collection_name=name, points=points)
    return point_ids


def search_vectors(
    query_vector: list[float],
    top_k: int | None = None,
    doc_filter: str | None = None,
    collection_name: str | None = None,
) -> list[dict]:
    manager = get_qdrant_manager()
    client = manager.get_client()
    name = collection_name or settings.QDRANT_COLLECTION
    k = top_k or settings.RETRIEVAL_TOP_K

    query_filter = None
    if doc_filter:
        query_filter = Filter(
            must=[FieldCondition(key="document_id", match=MatchValue(value=doc_filter))]
        )

    results = client.query_points(
        collection_name=name,
        query=query_vector,
        limit=k,
        query_filter=query_filter,
        with_payload=True,
    )

    return [
        {
            "id": str(hit.id),
            "score": hit.score,
            "text": hit.payload.get("text", ""),
            "document_id": hit.payload.get("document_id", ""),
            "chunk_index": hit.payload.get("chunk_index", 0),
            "metadata": hit.payload.get("metadata", {}),
        }
        for hit in results.points
    ]


def delete_by_document(document_id: str, collection_name: str | None = None):
    manager = get_qdrant_manager()
    client = manager.get_client()
    name = collection_name or settings.QDRANT_COLLECTION

    client.delete(
        collection_name=name,
        points_selector=Filter(
            must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]
        ),
    )
