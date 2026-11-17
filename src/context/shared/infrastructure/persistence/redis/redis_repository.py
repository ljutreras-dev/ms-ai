import json
from typing import Any, Optional
from src.context.shared.infrastructure.persistence.redis.redis_client_factory import RedisClientFactory


class RedisRepository:
    """
    Base generic Redis repository providing async helpers for key-value, caching,
    and expiring entries.
    """

    def __init__(self, client_factory: RedisClientFactory) -> None:
        self._client_factory = client_factory

    async def get(self, key: str) -> Optional[str]:
        client = await self._client_factory.get_client()
        return await client.get(key)

    async def get_json(self, key: str) -> Optional[Any]:
        value = await self.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> None:
        client = await self._client_factory.get_client()
        if ttl_seconds is not None:
            await client.setex(key, ttl_seconds, value)
        else:
            await client.set(key, value)

    async def set_json(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        encoded = json.dumps(value)
        await self.set(key, encoded, ttl_seconds)

    async def delete(self, key: str) -> bool:
        client = await self._client_factory.get_client()
        count = await client.delete(key)
        return count > 0

    async def exists(self, key: str) -> bool:
        client = await self._client_factory.get_client()
        return bool(await client.exists(key))
