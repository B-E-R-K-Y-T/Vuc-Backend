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


def exception_handler(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> JSONResponse:
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


class TokenGenerator:
    alphabet = string.ascii_letters + string.digits

    @classmethod
    def generate_new_token(cls, token_len: int = app_settings.TOKEN_LENGTH) -> str:
        token = [random.choice(cls.alphabet) for _ in range(token_len)]

        return ''.join(token)


def convert_schema_to_dict(schema: BaseModel) -> dict:
    """
    Конвертирует схемы в словари таким образом, чтобы поле Enum'ки переопределялось тем значением,
    которое было установлено в классе.

    Пример:
    class SquadRange(Enum):
        one = 1
        two = 2
        three = 3


    class Platoon(BaseModel):
        squad_num: SquadRange
        platoon_id: int


    При запросе с телом: {'squad_num': 3, 'platoon_id': 1}
    Имеем:

    @router.post("/")
    async def f(platoon: Platoon):
        dict(platoon) # {'squad_num': SquadRange, 'platoon_id': 1}
        convert_schema_to_dict(platoon) # {'squad_num': 3, 'platoon_id': 1}
    """
    schema_dict = dict(schema)
    res = {}

    for key, value in schema_dict.items():
        if isinstance(value, Enum):
            res[key] = value.value
        else:
            res[key] = value

    return res
