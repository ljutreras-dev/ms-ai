import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert "x-process-time" in response.headers
    data = response.json()
    assert data["status"] == "UP"
    assert "service" in data
    assert "version" in data
