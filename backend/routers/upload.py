from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.dependencies import get_db
from backend.models.schemas import UploadResponse
from backend.services.document_service import upload_document

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    content = await file.read()

    result = await upload_document(file.filename, content, db)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])

    return UploadResponse(
        document_id=result["document_id"],
        filename=result["filename"],
        mime_type=result["mime_type"],
        status="completed",
        message=f"Document processed successfully. Extracted {result['text_length']} characters.",
    )
