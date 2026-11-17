from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.context.shared.infrastructure.persistence.mongo.mongo_config import MongoConfig
from src.context.shared.domain.exceptions import DatabaseConnectionError


class MongoClientFactory:
    """
    Factory that manages lifecycle and pooling for asynchronous MongoDB connections.
    Mirrors MongoClientFactory from Node.js Clean Architecture.
    """

    def __init__(self, config: MongoConfig) -> None:
        self._config = config
        self._client: Optional[AsyncIOMotorClient] = None

    async def get_client(self) -> AsyncIOMotorClient:
        """Returns active AsyncIOMotorClient instance, creating one if not initialized."""
        if self._client is None:
            try:
                self._client = AsyncIOMotorClient(
                    self._config.uri,
                    serverSelectionTimeoutMS=self._config.server_selection_timeout_ms,
                )
            except Exception as e:
                raise DatabaseConnectionError(
                    message=f"Failed to initialize MongoDB client: {str(e)}",
                    info={"uri": self._config.uri, "error": str(e)},
                ) from e
        return self._client

    async def get_database(self, db_name: Optional[str] = None) -> AsyncIOMotorDatabase:
        """Returns the requested database or default configured database."""
        client = await self.get_client()
        target_db = db_name or self._config.database_name
        return client[target_db]

    async def ping(self) -> bool:
        """Pings the MongoDB server to verify connectivity."""
        try:
            client = await self.get_client()
            await client.admin.command("ping")
            return True
        except Exception:
            return False

    async def close(self) -> None:
        """Closes the active MongoDB connection."""
        if self._client is not None:
            self._client.close()
            self._client = None
