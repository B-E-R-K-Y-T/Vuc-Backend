import asyncio
import random
import string
from http import HTTPStatus
from functools import wraps
from typing import Callable

from fastapi.responses import JSONResponse

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
    def generate_new_token(cls):
        token = [random.choice(cls.alphabet) for _ in range(app_settings.TOKEN_LENGTH)]

        return ''.join(token)
