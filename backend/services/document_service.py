import logging
import os
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.models.database import Document, ProcessingStatus
from embeddings.embedding_service import get_embedding_service
from ingestion.pipeline import ingest_document
from ingestion.validators import validate_file
from rag.chunking import get_chunking_service
from vectorstore.operations import upsert_vectors

logger = logging.getLogger(__name__)


async def upload_document(
    filename: str,
    file_content: bytes,
    db: AsyncSession,
) -> dict:
    # Validate file
    validation = validate_file(filename, len(file_content))
    if not validation.valid:
        return {"success": False, "error": validation.error}

    doc_id = str(uuid.uuid4())

    # Save file to disk
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}_{filename}")
    with open(file_path, "wb") as f:
        f.write(file_content)

    # Create database record
    document = Document(
        id=doc_id,
        filename=filename,
        mime_type=validation.mime_type,
        file_size=len(file_content),
        upload_time=datetime.now(timezone.utc),
        processing_status=ProcessingStatus.PROCESSING,
        file_path=file_path,
    )
    db.add(document)
    await db.commit()

    # Parse the document
    result = ingest_document(file_path, validation.mime_type)

    if not result.success:
        document.processing_status = ProcessingStatus.FAILED
        document.error_message = result.error
        await db.commit()
        return {
            "success": False,
            "error": result.error,
            "document_id": doc_id,
        }

    # Chunk the document
    chunking_service = get_chunking_service()
    chunks = chunking_service.chunk_text(
        result.text,
        metadata={
            "document_id": doc_id,
            "filename": filename,
            "source_type": result.source_type,
        },
    )

    # Generate embeddings and store in vector DB
    try:
        embedding_service = get_embedding_service()
        texts = [chunk["text"] for chunk in chunks]
        vectors = embedding_service.embed_batch(texts)

        payloads = [
            {
                "text": chunk["text"],
                "document_id": doc_id,
                "chunk_index": chunk["chunk_index"],
                "metadata": chunk["metadata"],
            }
            for chunk in chunks
        ]

        upsert_vectors(vectors, payloads)
        document.chunk_count = len(chunks)
    except Exception as e:
        logger.exception("Failed to embed/store vectors for %s", doc_id)
        document.processing_status = ProcessingStatus.FAILED
        document.error_message = f"Embedding failed: {e}"
        await db.commit()
        return {"success": False, "error": str(e), "document_id": doc_id}

    document.processing_status = ProcessingStatus.COMPLETED
    await db.commit()

    return {
        "success": True,
        "document_id": doc_id,
        "filename": filename,
        "mime_type": validation.mime_type,
        "text_length": len(result.text),
        "chunk_count": len(chunks),
        "metadata": result.metadata,
    }


async def get_document(doc_id: str, db: AsyncSession) -> Document | None:
    result = await db.execute(select(Document).where(Document.id == doc_id))
    return result.scalar_one_or_none()


async def list_documents(db: AsyncSession) -> list[Document]:
    result = await db.execute(select(Document).order_by(Document.upload_time.desc()))
    return list(result.scalars().all())
