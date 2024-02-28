import pytest  # noqa
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User

# Чтобы можно было просто скопировать тело ответа и запроса из Swagger и ничо не менять
true = True
false = False
null = None

jwt_token = None


async def test_register_user(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "user818@example.com",
        "password": "string",
        "is_active": true,
        "is_superuser": false,
        "is_verified": false,
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
        "telegram_id": 818
    })

    assert response.status_code == 201


async def test_register_user_commander_platoon(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "user817@example.com",
        "password": "string",
        "is_active": true,
        "is_superuser": false,
        "is_verified": false,
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
        "telegram_id": 817
    })

    assert response.status_code == 201

    response = await ac.post("/auth/register", json={
        "email": "user816@example.com",
        "password": "string",
        "is_active": true,
        "is_superuser": false,
        "is_verified": false,
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
        "telegram_id": 816
    })

    assert response.status_code == 400


async def test_register_user_commander_squad(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "user816@example.com",
        "password": "string",
        "is_active": true,
        "is_superuser": false,
        "is_verified": false,
        "name": "string",
        "date_of_birth": "2024-02-27T20:01:46.326Z",
        "phone": "string",
        "address": "string",
        "institute": "string",
        "direction_of_study": "string",
        "group_study": "string",
        "platoon_number": 0,
        "squad_number": 1,
        "role": "Командир отделения",
        "telegram_id": 816
    })

    assert response.status_code == 201


async def test_login_user(ac: AsyncClient):
    global jwt_token

    response = await ac.post("/auth/jwt/login",
                             data={'grant_type': null,
                                   'username': 'user818@example.com',
                                   'password': 'string',
                                   'scope': '',
                                   'client_id': null,
                                   'client_secret': null},
                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                      'accept': 'application/json'
                                      }
                             )

    jwt_token = response.cookies['bonds']

    assert response.status_code == 204


async def test_create_platoon(ac: AsyncClient):
    response = await ac.post("/platoons/create",
                             json={
                                 "platoon_number": 818,
                                 "vus": 818,
                                 "semester": 818
                             },
                             cookies={'bonds': jwt_token}
                             )

    assert response.status_code == 201
    assert response.json() == {
        "platoon_number": 818
    }


async def test_get_platoon(ac: AsyncClient):
    response = await ac.get("/platoons/get_platoon",
                            params={"platoon_number": 0},
                            cookies={'bonds': jwt_token}
                            )

    assert response.status_code == 200
    assert response.json() == [
        {
            'email': 'user818@example.com',
            'password': None,
            'is_active': True,
            'is_superuser': False,
            'is_verified': False,
            'name': 'string',
            'date_of_birth': '2024-02-27T00:00:00',
            'phone': 'string',
            'address': 'string',
            'institute': 'string',
            'direction_of_study': 'string',
            'group_study': 'string',
            'platoon_number': 0,
            'squad_number': 1,
            'role': 'Admin',
            'telegram_id': 818
        },
        {
            'email': 'user817@example.com',
            'password': None,
            'is_active': True,
            'is_superuser': False,
            'is_verified': False,
            'name': 'string',
            'date_of_birth': '2024-02-27T00:00:00',
            'phone': 'string',
            'address': 'string',
            'institute': 'string',
            'direction_of_study': 'string',
            'group_study': 'string',
            'platoon_number': 0,
            'squad_number': 1,
            'role': 'Командир взвода',
            'telegram_id': 817
        },
    ]


async def test_get_platoons(ac: AsyncClient):
    response = await ac.get(
        url="/platoons/get_platoons",
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "0": {
                "vus": 0,
                "semester": 0
            },
            "818": {
                "vus": 818,
                "semester": 818
            }
        }
    }


async def test_get_platoon(ac: AsyncClient):
    response = await ac.get("/platoons/get_platoon",
                            params={"platoon_number": -10},
                            cookies={'bonds': jwt_token}
                            )

    assert response.status_code == 404


async def test_get_platoon_commander(ac: AsyncClient, tst_async_session: AsyncSession):
    response = await ac.get("/platoons/get_platoon_commander",
                            params={"platoon_number": 0},
                            cookies={'bonds': jwt_token}
                            )

    query = select(User).where(User.telegram_id == 817)

    user: User = await tst_async_session.scalar(query)

    user: dict = user.convert_to_dict()

    assert response.status_code == 200
    assert response.json() == {
        "id": user['id'],
        "email": "user817@example.com",
        "is_active": true,
        "is_superuser": false,
        "is_verified": false,
        "name": "string",
        "token": user['token']
    }


async def test_get_platoon_commander_error(ac: AsyncClient, tst_async_session: AsyncSession):
    response = await ac.get("/platoons/get_platoon_commander",
                            params={"platoon_number": -10},
                            cookies={'bonds': jwt_token}
                            )

    assert response.status_code == 404


async def test_get_count_squad_in_platoon(ac: AsyncClient):
    response = await ac.get("/platoons/get_count_squad_in_platoon",
                            params={"platoon_number": 0},
                            cookies={'bonds': jwt_token}
                            )

    assert response.status_code == 200
    assert response.json() == {
        "count_squad": 1
    }


async def test_get_count_squad_in_platoon_error(ac: AsyncClient):
    response = await ac.get("/platoons/get_count_squad_in_platoon",
                            params={"platoon_number": -10},
                            cookies={'bonds': jwt_token}
                            )

    assert response.status_code == 404


async def test_logout_user(ac: AsyncClient):
    response = await ac.post("/auth/jwt/logout",
                             cookies={'bonds': jwt_token}
                             )

    assert response.status_code == 204
