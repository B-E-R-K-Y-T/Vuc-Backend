import inspect
import time
from inspect import Signature
from functools import wraps
from typing import Awaitable, Callable

from fastapi.params import Depends

from config import app_settings
from services.cache.containers import Container
from services.util import sync_async_call


class CacheCollector:
    def __init__(self, container: Container):
        self.__container: Container = container
        self.__keys: dict = {}

    @staticmethod
    def get_key(func: Callable | Awaitable, args: tuple, kwargs: dict, signature: dict) -> str:
        key: str = func.__name__

        for kwarg, value in kwargs.items():
            if kwarg == "request":
                continue

            if kwarg == "response":
                continue

            if kwarg in signature:
                print(kwarg, type(value), hash(value))
                key += f'/{kwarg}={value}'

        for arg in args:
            key += f'/{arg}'

        return key

    @staticmethod
    def get_signature(func: Callable | Awaitable) -> Signature:
        return inspect.signature(func)

    @staticmethod
    def filter_depends(signature: Signature) -> dict:
        parameters = signature.parameters
        res = {}

        for name, param in parameters.items():
            if isinstance(param.default, Depends):
                continue

            res[name] = param

        return res

    def cache(self, expire: int = app_settings.CACHE_TIME_DEFAULT) -> Callable | Awaitable:
        def decorator(func: Callable | Awaitable) -> Callable | Awaitable:
            signature = self.filter_depends(self.get_signature(func))

            @wraps(func)
            async def wrapper(*args, **kwargs):
                if not app_settings.CACHE_ON:
                    return await sync_async_call(func, *args, **kwargs)

                key = self.get_key(func, args, kwargs, signature)
                cached_value = await self.__container.get_value(key)
                now = time.time()

                if cached_value is not None:
                    date_, value = cached_value

                    if now - date_ > expire:
                        result = await sync_async_call(func, *args, **kwargs)

                        await self.__container.set_value(key, [now, result])
                    else:
                        result = value
                else:
                    result = await sync_async_call(func, *args, **kwargs)

                    await self.__container.set_value(key, [now, result])

                return result

            return wrapper

        return decorator
