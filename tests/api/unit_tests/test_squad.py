import pytest
from httpx import AsyncClient

from tests.api.conftest import Options


@pytest.mark.skipif(
    f'config.getoption("{Options.SQUAD.key}") != "{Options.SQUAD.default_value}"'
)
class TestSquad:
    async def test_get_students_by_squad(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/squad/get_students_by_squad",
            params={"platoon_number": 0, "squad_number": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == {
            "1": {
                "id": 1,
                "name": "Nik",
                "date_of_birth": "2024-02-29T00:00:00",
                "phone": "89012345678",
                "email": "email@mail.com",
                "address": "улица 20",
                "institute": "IKB",
                "direction_of_study": "direction_of_study",
                "group_study": "group_study",
                "platoon_number": 0,
                "squad_number": 1,
                "role": "Студент",
                "telegram_id": 98765,
            },
            "2": {
                "id": 2,
                "name": "TEST_USER",
                "date_of_birth": "2024-02-29T00:00:00",
                "phone": "89012345678",
                "email": "test@email.ru",
                "address": "улица 20",
                "institute": "IKB",
                "direction_of_study": "direction_of_study",
                "group_study": "group_study",
                "platoon_number": 0,
                "squad_number": 1,
                "role": "Студент",
                "telegram_id": 0,
            },
            "3": {
                "id": 3,
                "name": "TEST_USER_PLATOON_COMMANDER",
                "date_of_birth": "2024-02-29T00:00:00",
                "phone": "89012345678",
                "email": "pc_test@email.ru",
                "address": "улица 20",
                "institute": "IKB",
                "direction_of_study": "direction_of_study",
                "group_study": "group_study",
                "platoon_number": 0,
                "squad_number": 1,
                "role": "Командир взвода",
                "telegram_id": 2,
            },
            "4": {
                "id": 4,
                "name": "string",
                "date_of_birth": "2024-02-27T00:00:00",
                "phone": "string",
                "email": "admin@mail.ru",
                "address": "string",
                "institute": "string",
                "direction_of_study": "string",
                "group_study": "string",
                "platoon_number": 0,
                "squad_number": 1,
                "role": "Admin",
                "telegram_id": 777,
            },
        }

        response = await ac.get(
            url="/squad/get_students_by_squad",
            params={"platoon_number": 0, "squad_number": 100},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == {}
