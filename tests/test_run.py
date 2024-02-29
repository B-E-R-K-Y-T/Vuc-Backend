"""
Хоть какие-то тесты лучше, чем никакие
"""

from httpx import AsyncClient
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Subject

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

    # Намеренная ошибка.
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


async def test_get_user_role(ac: AsyncClient, tst_async_session: AsyncSession):
    query = (
        select(User).
        where(User.role == 'Admin')
    )
    user = await tst_async_session.scalar(query)
    user_id = user.convert_to_dict()['id']
    response = await ac.get("/users/get_user_role",
                            params={"user_id": user_id},
                            cookies={'bonds': jwt_token}
                            )

    assert response.status_code == 200
    assert response.json() == {
        "role": "Admin"
    }


async def test_get_user_role_error(ac: AsyncClient):
    response = await ac.get("/users/get_user_role",
                            params={"user_id": -1},
                            cookies={'bonds': jwt_token}
                            )

    assert response.status_code == 404


async def test_get_user(ac: AsyncClient, tst_async_session: AsyncSession):
    query = (
        select(User).
        where(User.role == 'Admin')
    )
    user = await tst_async_session.scalar(query)
    token = user.convert_to_dict()['token']
    user_id = user.convert_to_dict()['id']

    response = await ac.get("/users/get_user",
                            params={"user_id": user_id},
                            cookies={'bonds': jwt_token}
                            )

    assert response.status_code == 200
    assert response.json() == {
        "id": user_id,
        "email": "user818@example.com",
        "is_active": true,
        "is_superuser": false,
        "is_verified": false,
        "name": "string",
        "token": token
    }


async def test_get_user_error(ac: AsyncClient):
    response = await ac.get("/users/get_user",
                            params={"user_id": -10},
                            cookies={'bonds': jwt_token}
                            )

    assert response.status_code == 404


async def test_get_user_by_tg(ac: AsyncClient, tst_async_session: AsyncSession):
    query = (
        select(User).
        where(User.role == 'Admin')
    )
    user = await tst_async_session.scalar(query)
    token = user.convert_to_dict()['token']
    user_id = user.convert_to_dict()['id']
    telegram_id = user.convert_to_dict()['telegram_id']

    response = await ac.get("/users/get_user_by_tg",
                            params={"telegram_id": telegram_id},
                            cookies={'bonds': jwt_token}
                            )

    assert response.status_code == 200
    assert response.json() == {
        "id": user_id,
        "email": "user818@example.com",
        "is_active": true,
        "is_superuser": false,
        "is_verified": false,
        "name": "string",
        "token": token
    }


async def test_get_user_by_tg_error(ac: AsyncClient):
    response = await ac.get("/users/get_user_by_tg",
                            params={"telegram_id": -10},
                            cookies={'bonds': jwt_token}
                            )

    assert response.status_code == 404


async def test_set_attrs_to_user(ac: AsyncClient):
    new_attrs = {
        "id": 0,
        "data": {
            "name": "TEST",
            "email": "<EMAIL>",
            "password": "<PASSWORD>",
            "phone": "123456789",
            "dob": "1999-12-31",
            "address": "123 Main Street",
            "institute": "Test Institute",
            "group_study": "Test Group Study",
            "squad_number": 1,
            "platoon_number": 818,
            "direction_of_study": "Test Direction Of Study",
        }
    }
    response = await ac.post(
        url="/users/set_user_attr",
        json=new_attrs,
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 204


async def test_set_attrs_to_user_error(ac: AsyncClient):
    new_attrs = {
        "id": 0,
        "data": {
            "name": 1,
            "email": 123,
            "password": [],
            "phone": [],
            "dob": "1999-12-31asdq23easd",
            "address": [],
            "institute": [],
            "group_study": [],
            "squad_number": [],
            "platoon_number": [],
            "direction_of_study": [],
        }
    }
    response = await ac.post(
        url="/users/set_user_attr",
        json=new_attrs,
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 422


async def test_set_user_mail(ac: AsyncClient):
    response = await ac.post(
        url="/users/set_user_mail",
        json={
            "id": 1,
            "email": "user@example.com"
        },
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 204


async def test_set_user_mail_error(ac: AsyncClient):
    response = await ac.post(
        url="/users/set_user_mail",
        json={
            "id": 1,
            "email": "-------------"
        },
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 422

    response = await ac.post(
        url="/users/set_user_mail",
        json={
            "id": 1,
            "email": "user@example.com"
        },
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 400


async def _test_set_user_telegram_id(ac: AsyncClient):
    """
    Временно вырезано
    """
    response = await ac.post(
        url="/users/set_user_telegram_id",
        json={
            "id": 1,
            "telegram_id": 818 + 818
        },
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 204


async def _test_set_user_telegram_id_error(ac: AsyncClient):
    """
    Временно вырезано
    """
    response = await ac.post(
        url="/users/set_user_telegram_id",
        json={
            "id": 1,
            "telegram_id": "-"
        },
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 422

    response = await ac.post(
        url="/users/set_user_telegram_id",
        json={
            "id": 1,
            "telegram_id": 818 + 818
        },
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 400


async def test_get_subjects(ac: AsyncClient, tst_async_session: AsyncSession):
    for i in range(3):
        stmt = (
            insert(
                Subject
            ).values(
                name=f"Test Subject_{i}",
                admin_id=0,
                platoon_id=0,
                semester=1,
            )
        )
        await tst_async_session.execute(stmt)
        await tst_async_session.commit()

    response = await ac.get(
        url="/professor/get_subjects",
        params={"platoon_number": 0, "semester": 1},
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'platoon_id': 0, 'semester': 1, 'admin_id': 1, 'name': 'subject'},
        {'id': 2, 'platoon_id': 0, 'semester': 1, 'admin_id': 0, 'name': 'Test Subject_0'},
        {'id': 3, 'platoon_id': 0, 'semester': 1, 'admin_id': 0, 'name': 'Test Subject_1'},
        {'id': 4, 'platoon_id': 0, 'semester': 1, 'admin_id': 0, 'name': 'Test Subject_2'}
    ]


async def test_get_subjects_error(ac: AsyncClient):
    response = await ac.get(
        url="/professor/get_subjects",
        params={"platoon_number": 352, "semester": 1},
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 404


async def test_get_semesters(ac: AsyncClient):
    response = await ac.get(
        url="/professor/get_semesters",
        params={"user_id": 1},
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 200
    assert response.json() == {'semesters': [1]}


async def test_logout_user(ac: AsyncClient):
    response = await ac.post(
        url="/auth/jwt/logout",
        cookies={'bonds': jwt_token}
    )

    assert response.status_code == 204
