from fastapi import FastAPI
from src.app.routes.health.health_router import health_router


def register_routes(app: FastAPI, prefix: str = "/api/v1") -> None:
    """
    Registers all bounded context routers into the FastAPI application.
    Mirrors registerRoutes from Node.js Clean Architecture template.
    """
    # Health checks at root level
    app.include_router(health_router)

    # Register additional bounded context routes under `prefix` (e.g. /api/v1) here:
    # app.include_router(example_router, prefix=prefix)
