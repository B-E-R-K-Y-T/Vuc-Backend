import asyncio
from functools import wraps
from typing import AsyncGenerator, Callable

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import app_settings

Base = declarative_base()

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
    Декоратор для неявной инициализации сессии к бд в функции через аргумент
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = await anext(get_async_session())

        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs, session=session)
        else:
            return func(*args, **kwargs, session=session)

    return wrapper
