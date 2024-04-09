import pytest
from httpx import AsyncClient


class Option:
    def __init__(self, key: str, default_value: str):
        self.__key = key
        self.__default_value = default_value

    @property
    def default_value(self):
        return self.__default_value

    @property
    def key(self):
        return self.__key


class Options:
    USER = Option("--user", "true")
    USER_REG = Option("--user_reg", "true")
    PLATOON = Option("--platoon", "true")
    SUBJECT = Option("--subject", "true")
    GRADING = Option("--grading", "true")
    PROFESSOR = Option("--professor", "true")
    SQUAD = Option("--squad", "true")
    ATTEND = Option("--attend", "true")


def pytest_addoption(parser):
    options = [
        Options.GRADING,
        Options.PLATOON,
        Options.SUBJECT,
        Options.USER_REG,
        Options.USER,
        Options.PROFESSOR,
        Options.SQUAD,
        Options.ATTEND,
    ]

    for option in options:
        parser.addoption(
            option.key,
            default=option.default_value,
            choices=(option.default_value, "false"),
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

    # Входим в систему
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

    jwt_token_ = response.cookies["bonds"]

    #  Получаем токен, прогоняем тесты
    yield jwt_token_

    # Выходим из системы после тестов
    response = await ac.post(url="/auth/jwt/logout", cookies={"bonds": jwt_token_})

    assert response.status_code == 204


@pytest.fixture(scope='session')
async def create_platoon_commander(ac: AsyncClient):
    response = await ac.post(
        url="/auth/register",
        json={
            "email": "p_c@mail.ru",
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
            "role": "Командир взвода",
            "telegram_id": 999,
        },
    )

    assert response.status_code == 201
