from fastapi import APIRouter

from backend.models.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        version="0.1.0",
        services={
            "api": "running",
        },
    )
