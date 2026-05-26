import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.middleware.observability import ObservabilityMiddleware
from backend.middleware.security import APIKeyMiddleware
from backend.models.database import init_db
from backend.routers import health, incidents, query, sources, upload


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure directories exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs("./data/db", exist_ok=True)

    # Initialize database
    await init_db()

    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ObservabilityMiddleware)
app.add_middleware(APIKeyMiddleware)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(query.router, prefix="/api", tags=["query"])
app.include_router(sources.router, prefix="/api", tags=["sources"])
app.include_router(incidents.router, prefix="/api", tags=["incidents"])
