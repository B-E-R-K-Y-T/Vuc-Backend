import asyncio
import random
import string
from enum import Enum
from typing import Callable, Any, Awaitable, Sequence

from pydantic import BaseModel

from config import app_settings


class TokenGenerator:
    alphabet = string.ascii_letters + string.digits

    @classmethod
    def generate_new_token(cls, token_len: int = app_settings.TOKEN_LENGTH) -> str:
        token = [random.choice(cls.alphabet) for _ in range(token_len)]

        return "".join(token)


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


async def sync_async_call(func: Callable | Awaitable, *args: Any, **kwargs: Any) -> Any:
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        return func(*args, **kwargs)


async def result_item_builder(data: dict, schema: BaseModel, key_field: str = "id") -> dict:
    """
    Использовать только на списках сущностей, чтобы сделать их ID индексами в коллекции

    Конвертирует результат из вида: {key_field: 1, "k1": 2, "k2": 3}

    В следующий вид: {1: {"k1": 2, "k2": 3}}
    """
    transformed_data: dict = {}
    key = data.get(key_field)

    transformed_data[key] = schema.model_validate(data, from_attributes=True)

    return transformed_data


async def result_collection_builder(items: Sequence, schema: BaseModel, key_field: str = "id") -> dict:
    """
    Применяет result_item_builder к коллекции
    """
    result = {}

    for item in items:
        result.update(
            await result_item_builder(
                item.convert_to_dict(),
                schema=schema,
                key_field=key_field
            )
        )

    return result
