import asyncio
from functools import wraps
from typing import AsyncGenerator, Callable

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import app_settings


class _Base(DeclarativeBase):
    type_annotation_map = {
        str: String().with_variant(String(255), "postgresql")
    }

    def convert_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return (f'ORM Table: \n{self.__class__.__name__}(\n'
                f'{''.join(f'\t{k}={v};\n' for k, v in self.convert_to_dict().items())})')


BaseTable = _Base

engine = create_async_engine(url=str(app_settings.DATABASE_DSN),
                             echo=True,
                             pool_size=5,
                             max_overflow=10)
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


def session_init(func: Callable) -> Callable:
    """
    Декоратор для неявной инициализации сессии, для подключения к бд в функции, через аргумент

    Пример:

    @session_init
    async def platoon_is_exist(platoon_number: int, session: AsyncSession):
        ...

    # Не надо явно открывать сессию при вызове.
    await platoon_is_exist(115)
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = await anext(get_async_session())

        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs, session=session)
        else:
            return func(*args, **kwargs, session=session)

    return wrapper
