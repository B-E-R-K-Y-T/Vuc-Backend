import pytest
from httpx import AsyncClient

from tests.api.conftest import Options


@pytest.mark.skipif(
    f'config.getoption("{Options.USER_REG.key}") != "{Options.USER_REG.default_value}"'
)
class TestUserRegistration:
    async def test_register_user(self, ac: AsyncClient):
        response = await ac.post(
            url="/auth/register",
            json={
                "email": "user818@example.com",
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
                "telegram_id": 818,
            },
        )

        assert response.status_code == 201

    @pytest.mark.parametrize(
        ("email", "telegram_id", "result", "platoon_number"),
        [
            ("user817@example.com", 817, 201, 1),
            ("user816@example.com", 816, 400, 1),
        ],
    )
    async def test_register_user_commander_platoon(
        self, ac: AsyncClient, email, telegram_id, result, platoon_number
    ):
        response = await ac.post(
            "/auth/register",
            json={
                "email": email,
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
                "platoon_number": platoon_number,
                "squad_number": 1,
                "role": "Командир взвода",
                "telegram_id": telegram_id,
            },
        )

        assert response.status_code == result

    async def test_register_user_commander_squad(self, ac: AsyncClient):
        response = await ac.post(
            "/auth/register",
            json={
                "email": "user816@example.com",
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
                "role": "Командир отделения",
                "telegram_id": 816,
            },
        )

        assert response.status_code == 201
