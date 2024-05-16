import pytest
from httpx import AsyncClient

from tests.api.conftest import Options


@pytest.mark.skipif(
    f'config.getoption("{Options.PROFESSOR.key}") != "{Options.PROFESSOR.default_value}"'
)
class TestSemester:
    async def test_get_semesters(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/professor/get_semesters",
            params={"user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200
        assert response.json() == {"semesters": [1]}

    async def test_set_visit_user(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            url="/professor/set_visit_user",
            json={"date_v": "2024-02-29", "visiting": 1, "user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 201
        assert response.json() == 2

    async def test_set_visit_user_error(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            url="/professor/set_visit_user",
            json={"date_v": "2024-02-29", "visiting": 5, "user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 422

        response = await ac.post(
            url="/professor/set_visit_user",
            json={"date_v": "2024-02-111", "visiting": 1, "user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 422

        response = await ac.post(
            url="/professor/set_visit_user",
            json={"date_v": "2024-13-29", "visiting": 1, "user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 422

        response = await ac.post(
            url="/professor/set_visit_user",
            json={"date_v": "202-12-29", "visiting": 1, "user_id": 1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 422

        response = await ac.post(
            url="/professor/set_visit_user",
            json={"date_v": "2022-12-29", "visiting": 1, "user_id": -1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_get_subject_by_now_semester_error(self, ac: AsyncClient, jwt_token):
        response = await ac.get(
            url="/professor/get_subject_by_now_semester",
            params={"platoon_number": -1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_set_visit_users(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            url="/professor/set_visit_users",
            json=[
                {"date_v": "2024-02-29", "visiting": 1, "user_id": 1},
                {"date_v": "2024-02-29", "visiting": 1, "user_id": 2},
            ],
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 201
        assert response.json() == [2, 3]

    async def test_set_visit_users_error(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            url="/professor/set_visit_users",
            json=[
                {"date_v": "2024-02-29", "visiting": 1, "user_id": -1},
                {"date_v": "2024-02-29", "visiting": 1, "user_id": 2},
            ],
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_set_visit_platoon(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            url="/professor/set_visit_platoon",
            json={"date_v": "2024-05-11", "visiting": 0, "platoon_number": 0},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 201
        assert response.json() == [4, 5, 6, 7]

    async def test_set_visit_platoon_error(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            url="/professor/set_visit_platoon",
            json={"date_v": "2024-05-11", "visiting": 0, "platoon_number": -1},
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404
