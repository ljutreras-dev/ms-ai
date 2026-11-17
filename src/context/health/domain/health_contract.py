from abc import ABC, abstractmethod
from typing import Any, Dict


class HealthContract(ABC):
    """Domain contract for system health check status."""

    @abstractmethod
    async def get(self) -> Dict[str, Any]:
        """Returns health information including MongoDB, Redis and system status."""
        pass
