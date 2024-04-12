from datetime import datetime, date

import pytest
from httpx import AsyncClient
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Attend
from tests.api.conftest import Options


@pytest.mark.skipif(
    f'config.getoption("{Options.USER.key}") != "{Options.USER.default_value}"'
)
class TestUser:
    async def test_get_user_role(
        self, ac: AsyncClient, tst_async_session: AsyncSession, jwt_token
    ):
        query = select(User).where(User.role == "Admin")
        user = await tst_async_session.scalar(query)
        user_id = user.convert_to_dict()["id"]
        response = await ac.get(
            "/users/get_user_role",
            params={"user_id": user_id},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == "Admin"

    async def test_get_user_role_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            "/users/get_user_role", params={"user_id": -1}, cookies={"bonds": jwt_token}
        )

        assert response.status_code == 404

    async def test_get_user(
        self, ac: AsyncClient, tst_async_session: AsyncSession, jwt_token
    ):
        query = select(User).where(User.email == "test@email.ru")
        user = await tst_async_session.scalar(query)
        token = user.convert_to_dict()["token"]
        user_id = user.convert_to_dict()["id"]

        response = await ac.get(
            "/users/get_self", params={"user_id": user_id}, cookies={"bonds": jwt_token}
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": user_id,
            "email": "test@email.ru",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "name": "TEST_USER",
            "token": token,
        }

    async def test_get_user_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            "/users/get_user", params={"user_id": -10}, cookies={"bonds": jwt_token}
        )

        assert response.status_code == 404

    async def test_get_user_by_tg(
        self, ac: AsyncClient, tst_async_session: AsyncSession, jwt_token
    ):
        query = select(User).where(User.email == "test@email.ru")
        user = await tst_async_session.scalar(query)
        token = user.convert_to_dict()["token"]
        user_id = user.convert_to_dict()["id"]
        telegram_id = user.convert_to_dict()["telegram_id"]

        response = await ac.get(
            "/users/get_user_by_tg",
            params={"telegram_id": telegram_id},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": user_id,
            "email": "test@email.ru",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "name": "TEST_USER",
            "token": token,
        }

    async def test_get_user_by_tg_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            "/users/get_user_by_tg",
            params={"telegram_id": -10},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_set_attrs_to_user(self, ac: AsyncClient, jwt_token):
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
            },
        }
        response = await ac.patch(
            url="/users/set_user_attr", json=new_attrs, cookies={"bonds": jwt_token}
        )

        assert response.status_code == 204

    async def test_set_attrs_to_user_error(self, ac: AsyncClient, jwt_token):
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
            },
        }
        response = await ac.patch(
            url="/users/set_user_attr", json=new_attrs, cookies={"bonds": jwt_token}
        )

        assert response.status_code == 422

    async def test_set_user_mail(self, ac: AsyncClient, jwt_token):
        response = await ac.patch(
            url="/users/set_user_mail",
            json={"id": 1, "email": "user@example.com"},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 204

    @pytest.mark.parametrize(
        ["id", "email", "result"],
        [
            (1, "-------------", 422),
            (1, "user@example.com", 400),
        ],
    )
    async def test_set_user_mail_error(
        self, ac: AsyncClient, jwt_token, id, email, result
    ):
        response = await ac.patch(
            url="/users/set_user_mail",
            json={"id": id, "email": email},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == result

    @pytest.mark.skip("Временно вырезано")
    async def test_set_user_telegram_id(self, ac: AsyncClient, jwt_token):
        """
        Временно вырезано
        """
        response = await ac.post(
            url="/users/set_user_telegram_id",
            json={"id": 1, "telegram_id": 818 + 818},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 204

    @pytest.mark.skip("Временно вырезано")
    async def test_set_user_telegram_id_error(self, ac: AsyncClient, jwt_token):
        """
        Временно вырезано
        """
        response = await ac.post(
            url="/users/set_user_telegram_id",
            json={"id": 1, "telegram_id": "-"},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 422

        response = await ac.post(
            url="/users/set_user_telegram_id",
            json={"id": 1, "telegram_id": 818 + 818},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 400

    async def test_get_id_from_tg(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_id_from_tg",
            params={"telegram_id": 98765},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == 1

    async def test_get_id_from_email(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_id_from_email",
            params={"email": "test@email.ru"},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == 2

    async def test_get_attendance_status_user(
        self, ac: AsyncClient, tst_async_session: AsyncSession, jwt_token
    ):
        stmt = insert(Attend).values(
            user_id=1,
            semester=1,
            date_v=datetime.strptime("2024-12-12", "%Y-%m-%d"),
            confirmed=True,
            visiting=1,
        )

        await tst_async_session.execute(stmt)
        await tst_async_session.commit()

        response = await ac.get(
            url="/users/get_attendance_status_user",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == {
            "1": {
                "user_id": 1,
                "date_v": "2023-12-22",
                "visiting": 1,
                "semester": 1,
                "confirmed": True,
                "id": 1,
            },
            "2": {
                "user_id": 1,
                "date_v": "2024-02-29",
                "visiting": 1,
                "semester": 0,
                "confirmed": False,
                "id": 2,
            },
            "3": {
                "user_id": 1,
                "date_v": "2024-12-12",
                "visiting": 1,
                "semester": 1,
                "confirmed": True,
                "id": 3,
            },
        }

    async def test_get_attendance_status_user_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_attendance_status_user",
            params={"user_id": -1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_get_self(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_user",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Nik",
            "date_of_birth": "2024-02-29T00:00:00",
            "phone": "89012345678",
            "email": "user@example.com",
            "address": "улица 20",
            "institute": "IKB",
            "direction_of_study": "direction_of_study",
            "group_study": "group_study",
            "platoon_number": 0,
            "squad_number": 1,
            "role": "Студент",
            "telegram_id": 98765,
        }

    async def test_get_self_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_self",
            params={"user_id": -1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_get_marks(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_marks",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == {
            "1": {
                "id": 1,
                "user_id": 1,
                "mark": 1,
                "mark_date": "2023-12-22",
                "subj_id": 1,
                "theme": "theme",
            },
            "2": {
                "id": 2,
                "user_id": 1,
                "mark": 1,
                "mark_date": f"{date.today()}",
                "subj_id": 1,
                "theme": "Test theme",
            },
        }

    async def test_get_marks_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_marks",
            params={"user_id": -1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    @pytest.mark.parametrize(
        ["user_id", "semester", "status_code", "json_result"],
        [
            (
                1,
                1,
                200,
                {
                    "1": {
                        "id": 1,
                        "user_id": 1,
                        "mark": 1,
                        "mark_date": "2023-12-22",
                        "subj_id": 1,
                        "theme": "theme",
                    },
                    "2": {
                        "id": 2,
                        "user_id": 1,
                        "mark": 1,
                        "mark_date": str(date.today()),
                        "subj_id": 1,
                        "theme": "Test theme",
                    },
                },
            ),
            (1, 0, 200, {}),
        ],
    )
    async def test_get_marks_by_semester(
        self, ac: AsyncClient, jwt_token, user_id, semester, status_code, json_result
    ):
        response = await ac.get(
            url="/users/get_marks_by_semester",
            params={"user_id": user_id, "semester": semester},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == status_code
        assert response.json() == json_result

    async def test_get_marks_by_semester_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_marks_by_semester",
            params={"user_id": -1, "semester": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_get_squad_user(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_squad_user",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == 1

    async def test_get_squad_user_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_squad_user",
            params={"user_id": -1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_get_platoon_user(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_platoon_user",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == 0

    async def test_get_platoon_user_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_platoon_user",
            params={"user_id": -1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_get_user_group_study(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_user_group_study",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == "group_study"

    async def test_get_user_direction_of_study(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_user_direction_of_study",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == "direction_of_study"

    async def test_get_user_address(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_user_address",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == "улица 20"

    async def test_get_user_institute(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_user_institute",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == "IKB"

    async def test_get_user_date_of_birth(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_user_date_of_birth",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == "2024-02-29"

    async def test_get_user_phone(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_user_phone",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == "89012345678"

    async def test_get_user_name(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_user_name",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == "Nik"

    async def test_get_students_list(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/users/get_students_list", cookies={"bonds": jwt_token}
        )

        assert response.status_code == 200
        assert response.json() == {
            "2": {
                "id": 2,
                "name": "TEST_USER",
                "role": "Студент",
                "platoon_number": 0,
                "squad_number": 1,
                "group_study": "group_study",
            },
            "3": {
                "id": 3,
                "name": "TEST_USER_PLATOON_COMMANDER",
                "role": "Командир взвода",
                "platoon_number": 0,
                "squad_number": 1,
                "group_study": "group_study",
            },
            "115": {
                "id": 115,
                "name": "test",
                "role": "Студент",
                "platoon_number": 818,
                "squad_number": 1,
                "group_study": "BDSM-13-37",
            },
            "1": {
                "id": 1,
                "name": "Nik",
                "role": "Студент",
                "platoon_number": 0,
                "squad_number": 1,
                "group_study": "group_study",
            },
        }
