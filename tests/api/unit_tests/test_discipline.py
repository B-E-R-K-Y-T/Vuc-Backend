import pytest
from httpx import AsyncClient

from tests.api.conftest import Options


@pytest.mark.skipif(
    f'config.getoption("{Options.DISCIPLINE.key}") != "{Options.DISCIPLINE.default_value}"'
)
class TestDiscipline:
    async def test_set_discipline(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            url="/disciplines/set_discipline",
            json={
                "date": "2024-04-18",
                "user_id": 1,
                "type": "encouragement",
                "comment": "string"
            },
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 201
        assert response.json() == 1

        response = await ac.post(
            url="/disciplines/set_discipline",
            json={
                "date": "2024-04-19",
                "user_id": 1,
                "type": "penalty",
                "comment": "string"
            },
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 201
        assert response.json() == 2

    async def test_set_discipline_error(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            url="/disciplines/set_discipline",
            json={
                "date": "2024-04-18",
                "user_id": -1,
                "type": "encouragement",
                "comment": "string"
            },
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 404

        response = await ac.post(
            url="/disciplines/set_discipline",
            json={
                "date": "2024-04-20",
                "user_id": 1,
                "type": "-----",
                "comment": "string"
            },
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 422
