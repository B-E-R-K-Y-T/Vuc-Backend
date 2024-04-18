"""
Сначала надо поднять тестовую базу данных.

Команда: docker run --rm --name db-vuc-test -p 8180:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=vuc_test_db -d postgres:15
"""

import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

import models  # noqa
from services.database.connector import get_async_session
from config import app_settings
from src import BaseTable
from main import app

# DATABASE
DATABASE_URL_TEST = str(app_settings.TEST_DATABASE_DSN)

metadata = BaseTable.metadata
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(autouse=True, scope="session")
async def tst_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
        await conn.execute(
            text("INSERT INTO platoon (vus, platoon_number, semester)VALUES(0,0,0);")
        )
        await conn.execute(
            text("INSERT INTO platoon (vus, platoon_number, semester)VALUES(0,1,0);")
        )

        await conn.execute(
            text(
                "INSERT INTO public.user (name, phone, date_of_birth, address, institute, direction_of_study,"
                "platoon_number, squad_number, role, telegram_id, token, group_study, email, registered_at, "
                "is_active, is_superuser, is_verified, hashed_password)"
                "VALUES('Nik', '89012345678', '2024-02-29T15:07:16.345'::date, 'улица 20', 'IKB',"
                "'direction_of_study', 0, 1, 'Студент', 98765, 'token', 'group_study',"
                "'email@mail.com', '2024-02-29T15:07:16.345'::date, 't', 'f', 'f', 'hashed_password');"
            )
        )

        await conn.execute(
            text(
                "INSERT INTO public.user (name, phone, date_of_birth, address, institute, direction_of_study,"
                "platoon_number, squad_number, role, telegram_id, token, group_study, email, registered_at, "
                "is_active, is_superuser, is_verified, hashed_password)"
                "VALUES('TEST_USER', '89012345678', '2024-02-29T15:07:16.345'::date, 'улица 20', 'IKB',"
                "'direction_of_study', 0, 1, 'Студент', 0, 'token', 'group_study',"
                "'test@email.ru', '2024-02-29T15:07:16.345'::date, 't', 'f', 'f', 'hashed_password');"
            )
        )

        await conn.execute(
            text(
                "INSERT INTO public.user (name, phone, date_of_birth, address, institute, direction_of_study,"
                "platoon_number, squad_number, role, telegram_id, token, group_study, email, registered_at, "
                "is_active, is_superuser, is_verified, hashed_password)"
                "VALUES('TEST_USER_PLATOON_COMMANDER', '89012345678', '2024-02-29T15:07:16.345'::date, "
                "'улица 20', 'IKB',"
                "'direction_of_study', 0, 1, 'Командир взвода', 2, 'token', 'group_study',"
                "'pc_test@email.ru', '2024-02-29T15:07:16.345'::date, 't', 'f', 'f', 'hashed_password');"
            )
        )

        await conn.execute(
            text(
                "INSERT INTO admins (name, email, password)VALUES('Tim','mail@mail.ru','123');"
            )
        )
        await conn.execute(
            text(
                "INSERT INTO day (date, weekday, semester, holiday)VALUES('12-22-2023'::date, 0, 0, 'f');"
            )
        )
        await conn.execute(
            text(
                "INSERT INTO attend (user_id, date_v, visiting, semester, confirmed)"
                "VALUES(1,'12-22-2023'::date, 1, 1, 't');"
            )
        )
        await conn.execute(
            text(
                "INSERT INTO subject (platoon_id, semester, admin_id, name)"
                "VALUES(0, 1, 1, 'subject');"
            )
        )
        await conn.execute(
            text(
                "INSERT INTO grading (subj_id, user_id, mark, mark_date, theme)"
                "VALUES(1, 1, 1, '12-22-2023'::date, 'theme');"
            )
        )
        await conn.execute(
            text(
                "INSERT INTO message_queue (telegram_id, message)"
                "VALUES(98765, 'message');"
            )
        )
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
