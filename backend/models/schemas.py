from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# --- Upload ---
class UploadResponse(BaseModel):
    document_id: str
    filename: str
    mime_type: str
    status: str
    message: str


# --- Query ---
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    filters: Optional[dict] = None


class Citation(BaseModel):
    document_id: str
    chunk_index: int
    text: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation] = []
    confidence_score: float = 0.0
    sources: list[dict] = []
    latency_ms: float = 0.0


# --- Sources ---
class SourceResponse(BaseModel):
    document_id: str
    filename: str
    mime_type: str
    upload_time: datetime
    chunk_count: int
    status: str


# --- Incidents ---
class IncidentSummary(BaseModel):
    summary: str
    related_documents: list[str] = []
    root_causes: list[str] = []
    recommendations: list[str] = []


# --- Health ---
class HealthResponse(BaseModel):
    status: str
    version: str
    services: dict[str, str] = {}
