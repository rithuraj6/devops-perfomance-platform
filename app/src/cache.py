import redis

from .config import settings


redis_client = redis.Redis.from_url(
    settings.redis_url,
    decode_responses=True,
)


def get_cache(key: str):
    return redis_client.get(key)


def set_cache(key: str, value: str, ttl: int = 60):
    redis_client.set(
        key,
        value,
        ex=ttl,
    )


def delete_cache(key: str):
    redis_client.delete(key)
