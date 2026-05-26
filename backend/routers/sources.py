from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.dependencies import get_db
from backend.models.schemas import SourceResponse
from backend.services.document_service import get_document, list_documents

router = APIRouter()


@router.get("/sources/{doc_id}", response_model=SourceResponse)
async def get_source(doc_id: str, db: AsyncSession = Depends(get_db)):
    doc = await get_document(doc_id, db)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return SourceResponse(
        document_id=doc.id,
        filename=doc.filename,
        mime_type=doc.mime_type,
        upload_time=doc.upload_time,
        chunk_count=doc.chunk_count,
        status=doc.processing_status.value,
    )


@router.get("/sources", response_model=list[SourceResponse])
async def list_sources(db: AsyncSession = Depends(get_db)):
    docs = await list_documents(db)
    return [
        SourceResponse(
            document_id=doc.id,
            filename=doc.filename,
            mime_type=doc.mime_type,
            upload_time=doc.upload_time,
            chunk_count=doc.chunk_count,
            status=doc.processing_status.value,
        )
        for doc in docs
    ]
