from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from backend.config import settings

# Paths that don't require API key auth
PUBLIC_PATHS = {"/api/health", "/docs", "/openapi.json", "/redoc"}


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if not settings.REQUIRE_API_KEY:
            return await call_next(request)

        # Skip auth for public paths
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key != settings.API_KEY:
            raise HTTPException(status_code=401, detail="Invalid or missing API key")

        return await call_next(request)
