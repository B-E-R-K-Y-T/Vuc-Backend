from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Platoon
from tests.api.conftest import Options


@pytest.mark.skipif(
    f'config.getoption("{Options.PLATOON.key}") != "{Options.PLATOON.default_value}"'
)
class TestPlatoon:
    async def test_create_platoon(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            "/platoons/create",
            json={"platoon_number": 818, "vus": 818, "semester": 818},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 201
        assert response.json() == {"platoon_number": 818}

    async def test_get_platoon(
        self, ac: AsyncClient, tst_async_session: AsyncSession, jwt_token
    ):
        stmt = insert(User).values(
            name="test",
            phone="123456789",
            date_of_birth=datetime.strptime("2024-03-21T00:00:00", "%Y-%m-%dT%H:%M:%S"),
            address="TEST",
            institute="TEST",
            direction_of_study="TEST",
            platoon_number=818,
            squad_number=1,
            role="Студент",
            telegram_id=115,
            token="TOK",
            group_study="BDSM-13-37",
            email="MAIL12345S@test.com",
            registered_at=datetime.strptime("2024-03-21T00:00:00", "%Y-%m-%dT%H:%M:%S"),
            is_active=True,
            is_superuser=False,
            is_verified=False,
            hashed_password="adqe2",
            id=115,
        )

        await tst_async_session.execute(stmt)
        await tst_async_session.commit()

        response = await ac.get(
            "/platoons/get_platoon",
            params={"platoon_number": 818},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == {
            "squad_count": 1,
            "students": {
                "115": {
                    "id": 115,
                    "name": "test",
                    "date_of_birth": "2024-03-21T00:00:00",
                    "phone": "123456789",
                    "email": "MAIL12345S@test.com",
                    "address": "TEST",
                    "institute": "TEST",
                    "direction_of_study": "TEST",
                    "group_study": "BDSM-13-37",
                    "platoon_number": 818,
                    "squad_number": 1,
                    "role": "Студент",
                    "telegram_id": 115,
                }
            },
        }

    async def test_get_platoons(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/platoons/get_platoons", cookies={"bonds": jwt_token}
        )

        assert response.status_code == 200
        assert response.json() == {
            "1": {"commander": None, "vus": 0, "semester": 0},
            "818": {"commander": None, "vus": 818, "semester": 818},
        }

    async def test_get_platoon_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            "/platoons/get_platoon",
            params={"platoon_number": -10},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_get_platoon_commander(
        self, ac: AsyncClient, tst_async_session: AsyncSession, jwt_token
    ):
        response = await ac.get(
            "/platoons/get_platoon_commander",
            params={"platoon_number": 0},
            cookies={"bonds": jwt_token},
        )

        query = select(User).where(User.telegram_id == 2)

        user: User = await tst_async_session.scalar(query)

        user: dict = user.convert_to_dict()

        assert response.status_code == 200
        assert response.json() == {
            "id": user["id"],
            "email": "pc_test@email.ru",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "name": "TEST_USER_PLATOON_COMMANDER",
            "token": user["token"],
        }

    async def test_get_platoon_commander_error(
        self, ac: AsyncClient, tst_async_session: AsyncSession, jwt_token
    ):
        response = await ac.get(
            "/platoons/get_platoon_commander",
            params={"platoon_number": -10},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_get_count_squad_in_platoon(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            "/platoons/get_count_squad_in_platoon",
            params={"platoon_number": 0},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == 1

    async def test_get_count_squad_in_platoon_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            "/platoons/get_count_squad_in_platoon",
            params={"platoon_number": -10},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404
