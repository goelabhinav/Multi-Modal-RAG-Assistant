import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.config import settings


class Base(DeclarativeBase):
    pass


class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    file_size = Column(Integer)
    upload_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    processing_status = Column(Enum(ProcessingStatus), default=ProcessingStatus.PENDING)
    chunk_count = Column(Integer, default=0)
    file_path = Column(String)
    error_message = Column(Text, nullable=True)


class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(String, primary_key=True)
    query_text = Column(Text)
    response_text = Column(Text)
    confidence_score = Column(Float)
    latency_ms = Column(Float)
    token_count = Column(Integer)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sources_used = Column(Text)  # JSON array of doc_ids


engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
