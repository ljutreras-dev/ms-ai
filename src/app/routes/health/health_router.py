from typing import Any, Dict
from fastapi import APIRouter, Depends
from src.app.dependency_injection.container import Container, get_container

health_router = APIRouter(tags=["Health"])


@health_router.get(
    "/health",
    summary="Health Check",
    description="Verifies the operational status of the service, MongoDB and Redis connections.",
    response_model=Dict[str, Any],
)
async def get_health(container: Container = Depends(get_container)) -> Dict[str, Any]:
    return await container.health_use_case.execute()
