from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from src.app.config import Settings, get_settings
from src.app.dependency_injection.container import get_container
from src.app.middlewares.error_handler import (
    base_error_handler,
    generic_exception_handler,
    validation_error_handler,
)
from src.app.middlewares.logging_middleware import RequestLoggingMiddleware
from src.app.routes.index import register_routes
from src.context.shared.domain.base_error import BaseError


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan manager.
    Initializes application resources and cleans up active connections on shutdown.
    """
    container = get_container()
    container.logger.info("Application startup completed successfully.")
    yield

    # Teardown active connections if any were opened
    container.logger.info("Gracefully closing database connections...")
    await container.mongo_factory.close()
    await container.redis_factory.close()
    container.logger.info("Application shutdown complete.")


def create_app(settings: Optional[Settings] = None) -> FastAPI:
    """
    Application factory mirroring the Server class pattern from Node.js Clean Architecture.
    """
    current_settings = settings or get_settings()

    app = FastAPI(
        title=current_settings.APP_NAME,
        description=(
            "Clean Architecture / DDD Python backend template built with FastAPI and UV."
        ),
        version=current_settings.VERSION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # 1. CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Request Logging Middleware
    app.add_middleware(RequestLoggingMiddleware)

    # 3. Exception Handlers (mirrors ErrorHandlerResponse)
    app.add_exception_handler(BaseError, base_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, generic_exception_handler)

    # 4. Register Routes
    register_routes(app, prefix=current_settings.API_V1_PREFIX)

    return app
