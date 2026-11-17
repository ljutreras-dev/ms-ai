import os
import sys
import pytest
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app.config import Settings
from src.app.dependency_injection.container import Container, get_container
from src.app.server import create_app


class DummyHealthRepo:
    async def get(self):
        return {
            "status": "UP",
            "service": "backend-template-python-test",
            "version": "1.0.0",
            "uptime_seconds": 1.0,
            "dependencies": {"mongodb": "UP", "redis": "UP"},
        }


@pytest.fixture
def test_container():
    settings = Settings(
        APP_NAME="test-backend",
    )
    container = Container(settings)

    # In-memory test repository to avoid remote network calls during testing
    container.health_repository = DummyHealthRepo()  # type: ignore[assignment]
    container.health_use_case._health_contract = container.health_repository

    return container


@pytest.fixture
def app(test_container):
    app_instance = create_app(test_container.settings)
    app_instance.dependency_overrides[get_container] = lambda: test_container
    return app_instance


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
