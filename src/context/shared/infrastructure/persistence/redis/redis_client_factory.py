from typing import Optional
import redis.asyncio as aioredis
from src.context.shared.infrastructure.persistence.redis.redis_config import RedisConfig
from src.context.shared.domain.exceptions import DatabaseConnectionError


class RedisClientFactory:
    """
    Factory for managing asynchronous Redis client lifecycle and connection pooling.
    Mirrors Redis factory patterns from Clean Architecture.
    """

    def __init__(self, config: RedisConfig) -> None:
        self._config = config
        self._client: Optional[aioredis.Redis] = None

    async def get_client(self) -> aioredis.Redis:
        """Returns the active Redis async client instance, initializing connection pool if necessary."""
        if self._client is None:
            try:
                self._client = aioredis.Redis(
                    host=self._config.host,
                    port=self._config.port,
                    db=self._config.db,
                    password=self._config.password,
                    ssl=self._config.ssl,
                    socket_timeout=self._config.socket_timeout,
                    decode_responses=True,
                )
            except Exception as e:
                raise DatabaseConnectionError(
                    message=f"Failed to connect to Redis: {str(e)}",
                    info={"host": self._config.host, "port": self._config.port, "error": str(e)},
                ) from e
        return self._client

    async def ping(self) -> bool:
        """Checks Redis server availability."""
        try:
            client = await self.get_client()
            return await client.ping()
        except Exception:
            return False

    async def close(self) -> None:
        """Closes the Redis connection pool."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
