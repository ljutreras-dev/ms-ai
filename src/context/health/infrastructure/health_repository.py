import time
from typing import Any, Dict
from src.context.health.domain.health_contract import HealthContract
from src.context.shared.infrastructure.persistence.mongo.mongo_client_factory import MongoClientFactory
from src.context.shared.infrastructure.persistence.mongo.mongo_repository import MongoRepository


class HealthRepository(MongoRepository, HealthContract):
    """
    Health infrastructure repository mirroring HealthRepository from the Node.js Clean Architecture.
    """

    def __init__(
        self,
        mongo_factory: MongoClientFactory,
        version: str = "1.0.0",
        app_name: str = "backend-template-python",
    ) -> None:
        super().__init__(client_factory=mongo_factory, database_name="template")
        self._version = version
        self._app_name = app_name
        self._start_time = time.time()

    async def get(self) -> Dict[str, Any]:
        return {
            "status": "UP",
            "service": self._app_name,
            "version": self._version,
            "uptime_seconds": round(time.time() - self._start_time, 2),
        }
