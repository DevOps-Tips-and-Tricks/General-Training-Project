import redis

from app.config import settings


def get_redis():
    """Dependency to get a Redis connection."""
    client = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True,
    )
    try:
        yield client
    finally:
        client.close()
