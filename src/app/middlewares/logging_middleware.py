import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.context.shared.infrastructure.logger.app_logger import AppLogger

logger = AppLogger()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    HTTP middleware logging incoming request path, method, status code, and latency.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        client_host = request.client.host if request.client else "unknown"

        logger.info(f"--> [{request.method}] {request.url.path} from {client_host}")

        try:
            response = await call_next(request)
            process_time = round((time.time() - start_time) * 1000, 2)
            logger.info(
                f"<-- [{request.method}] {request.url.path} - Status: {response.status_code} ({process_time}ms)"
            )
            response.headers["X-Process-Time"] = f"{process_time}ms"
            return response
        except Exception:
            process_time = round((time.time() - start_time) * 1000, 2)
            logger.error(
                f"<-- [{request.method}] {request.url.path} - FAILED ({process_time}ms)"
            )
            raise
