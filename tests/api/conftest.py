import pytest
from httpx import AsyncClient


def pytest_addoption(parser):
    parser.addoption(
        "--user",
        default="true",
        choices=("true", "false"),
    )


@pytest.fixture(scope='session')
async def jwt_token(ac: AsyncClient):
    response = await ac.post(
        url="/auth/register",
        json={
            "email": "admin@mail.ru",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "name": "string",
            "date_of_birth": "2024-02-27T20:01:46.326Z",
            "phone": "string",
            "address": "string",
            "institute": "string",
            "direction_of_study": "string",
            "group_study": "string",
            "platoon_number": 0,
            "squad_number": 1,
            "role": "Admin",
            "telegram_id": 777,
        },
    )

    assert response.status_code == 201

    response = await ac.post(
        "/auth/jwt/login",
        data={
            "grant_type": None,
            "username": "admin@mail.ru",
            "password": "string",
            "scope": "",
            "client_id": None,
            "client_secret": None,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json",
        },
    )

    assert response.status_code == 204

    return response.cookies["bonds"]
