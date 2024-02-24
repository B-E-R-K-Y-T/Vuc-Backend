import asyncio
import random
import string
from enum import Enum
from http import HTTPStatus
from functools import wraps
from typing import Callable

from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config import app_settings
from exceptions import MainVucException
from services.logger import LOGGER


def exception_handler(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        except MainVucException as e:
            LOGGER.err(f'{e=}, {e.__class__=}', exc_info=True)
            return JSONResponse(status_code=e.status, content=str(e))
        except Exception as e:
            LOGGER.err(f'{e=}, {e.__class__=}', exc_info=True)
            return JSONResponse(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content='Internal Server Error')

    return wrapper


class TokenWorker:
    alphabet = string.ascii_letters + string.digits

    @classmethod
    def generate_new_token(cls, token_len: int = app_settings.TOKEN_LENGTH):
        token = [random.choice(cls.alphabet) for _ in range(token_len)]

        return ''.join(token)


def convert_schema_to_dict(schema: BaseModel) -> dict:
    schema_dict = dict(schema)
    res = {}

    for key, value in schema_dict.items():
        if isinstance(value, Enum):
            res[key] = value.value
        else:
            res[key] = value

    return res
