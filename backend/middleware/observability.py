import logging
import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from backend.config import settings

# Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer() if settings.DEBUG else structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(
        logging.getLevelName(settings.LOG_LEVEL)
    ),
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())[:8]
        start = time.perf_counter()

        structlog.contextvars.bind_contextvars(request_id=request_id)

        logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
        )

        response = await call_next(request)

        latency_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            latency_ms=round(latency_ms, 2),
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Latency-Ms"] = str(round(latency_ms, 2))

        structlog.contextvars.unbind_contextvars("request_id")

        return response
