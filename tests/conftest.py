import fakeredis
import pytest
from fastapi.testclient import TestClient

from app.database import get_redis
from app.main import app


@pytest.fixture()
def client():
    """
    Fixture to create a test client and mock the Redis database.
    """
    # Initialize a fake Redis server in memory
    fake_redis = fakeredis.FakeRedis(decode_responses=True)

    # Define the override function
    def override_get_redis():
        try:
            yield fake_redis
        finally:
            fake_redis.close()

    # Apply the override to the FastAPI app
    app.dependency_overrides[get_redis] = override_get_redis

    # Yield the TestClient
    with TestClient(app) as test_client:
        yield test_client

    # Clean up overrides after the test finishes
    app.dependency_overrides.clear()
