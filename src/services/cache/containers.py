import pickle
from abc import ABC, abstractmethod

from redis import asyncio as aioredis

from config import app_settings


class Container(ABC):
    @abstractmethod
    async def set_value(self, key: str, value):
        raise NotImplementedError

    @abstractmethod
    async def get_value(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def del_value(self, key: str):
        raise NotImplementedError


class RedisContainer(Container):
    def __init__(self) -> None:
        self.redis = aioredis.from_url(
            f"redis://{app_settings.REDIS_HOST}:{app_settings.REDIS_PORT}"
        )

    async def set_value(self, key: str, value):
        serialized = pickle.dumps(value)

        await self.redis.set(key, serialized)

    async def get_value(self, key: str):
        value = await self.redis.get(key)

        if value is None:
            return None

        return pickle.loads(value)

    async def del_value(self, key: str):
        await self.redis.delete(key)
