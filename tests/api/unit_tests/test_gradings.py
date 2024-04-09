import pytest
from httpx import AsyncClient

from tests.api.conftest import Options


@pytest.mark.skipif(
    f'config.getoption("{Options.GRADING.key}") != "{Options.GRADING.default_value}"'
)
class TestGradings:
    async def test_set_grading_theme(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            url="/gradings/set_grading_theme",
            params={
                "platoon_number": 0,
                "theme_of_lesson": "Test theme",
                "subj_id": 1,
            },
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 201

    async def test_set_grading_theme_error(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            url="/gradings/set_grading_theme",
            params={
                "platoon_number": -1,
                "theme_of_lesson": "Test theme",
                "subj_id": 1,
            },
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

    async def test_edit_grading(self, ac: AsyncClient, jwt_token):
        response = await ac.patch(
            url="/gradings/edit_grading",
            params={
                "grading_id": 1,
                "mark": 3,
            },
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 200

    async def test_edit_grading_error(self, ac: AsyncClient, jwt_token):
        response = await ac.patch(
            url="/gradings/edit_grading",
            params={
                "grading_id": -1,
                "mark": 1,
            },
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

        response = await ac.patch(
            url="/gradings/edit_grading",
            params={
                "grading_id": 1,
                "mark": 0,
            },
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 400

        response = await ac.patch(
            url="/gradings/edit_grading",
            params={
                "grading_id": 1,
                "mark": 6,
            },
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 400

    async def test_update_gradings(self, ac: AsyncClient, jwt_token):
        response = await ac.patch(
            url="/gradings/update_gradings",
            json=[
                {
                    "id": 1,
                    "mark": 1,
                },
                {
                    "id": 2,
                    "mark": 1,
                },
            ],
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 201

    async def test_update_gradings_error(self, ac: AsyncClient, jwt_token):
        response = await ac.patch(
            url="/gradings/update_gradings",
            json=[
                {
                    "id": -1,
                    "mark": 1,
                },
                {
                    "id": 2,
                    "mark": 1,
                },
            ],
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

        response = await ac.patch(
            url="/gradings/update_gradings",
            json=[
                {
                    "id": 1,
                    "mark": 1,
                },
                {
                    "id": 2,
                    "mark": 0,
                },
            ],
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 400
