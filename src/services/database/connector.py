from typing import AsyncGenerator

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
