from typing import Any, Dict
from src.context.health.domain.health_contract import HealthContract


class HealthUseCase:
    """Use case to query current health and dependencies readiness."""

    def __init__(self, health_contract: HealthContract) -> None:
        self._health_contract = health_contract

    async def execute(self) -> Dict[str, Any]:
        return await self._health_contract.get()
