from typing import Optional
from src.app.config import Settings, get_settings
from src.context.health.application.health_use_case import HealthUseCase
from src.context.health.infrastructure.health_repository import HealthRepository
from src.context.shared.infrastructure.logger.app_logger import AppLogger
from src.context.shared.infrastructure.persistence.mongo.mongo_client_factory import MongoClientFactory
from src.context.shared.infrastructure.persistence.mongo.mongo_config import MongoConfig
from src.context.shared.infrastructure.persistence.redis.redis_client_factory import RedisClientFactory
from src.context.shared.infrastructure.persistence.redis.redis_config import RedisConfig


class Container:
    """
    Dependency Injection Container.
    Orchestrates infrastructure factories, repositories, adapters, and application use cases.
    """

    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()

        # Shared
        self.logger = AppLogger()

        # Mongo Infrastructure (lazy connection via factory)
        self.mongo_config = MongoConfig(
            uri=self.settings.MONGO_URI,
            database_name=self.settings.MONGO_DB_NAME,
        )
        self.mongo_factory = MongoClientFactory(self.mongo_config)

        # Redis Infrastructure (lazy connection via factory)
        self.redis_config = RedisConfig(
            host=self.settings.REDIS_HOST,
            port=self.settings.REDIS_PORT,
            db=self.settings.REDIS_DB,
            password=self.settings.REDIS_PASSWORD,
            ssl=self.settings.REDIS_SSL,
        )
        self.redis_factory = RedisClientFactory(self.redis_config)

        # Health Bounded Context
        self.health_repository = HealthRepository(
            mongo_factory=self.mongo_factory,
            version=self.settings.VERSION,
            app_name=self.settings.APP_NAME,
        )
        self.health_use_case = HealthUseCase(self.health_repository)


_container_instance: Optional[Container] = None


def get_container() -> Container:
    """Provides singleton access to DI container."""
    global _container_instance
    if _container_instance is None:
        _container_instance = Container()
    return _container_instance
