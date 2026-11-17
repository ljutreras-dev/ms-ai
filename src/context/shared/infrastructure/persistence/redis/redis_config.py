from dataclasses import dataclass
from typing import Optional


@dataclass
class RedisConfig:
    """Configuration parameters for Redis connection."""

    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    ssl: bool = False
    socket_timeout: float = 5.0
