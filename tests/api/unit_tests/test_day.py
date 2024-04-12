import pytest
from httpx import AsyncClient

from tests.api.conftest import Options


@pytest.mark.skipif(
    f'config.getoption("{Options.DAY.key}") != "{Options.DAY.default_value}"'
)
class TestDays:
    async def test_set_days(self, ac: AsyncClient, jwt_token):
        response = await ac.post(
            url="/days/set_days",
            json=[
                {"date": "2024-04-12", "weekday": 0, "semester": 0, "holiday": True},
                {"date": "2024-04-13", "weekday": 0, "semester": 0, "holiday": True},
            ],
            cookies={"bonds": jwt_token},
        )

        assert response.status_code == 201
        assert response.json() == [2, 3]
